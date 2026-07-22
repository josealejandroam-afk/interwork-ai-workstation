from __future__ import annotations

import json
from pathlib import Path

from .backup_manager import backup_files
from .errors import ExecutorError, ExecutionError
from .git_manager import git, make_local_commit, require_safe_branch, starting_commit, unstage_paths
from .markdown_editor import apply_updates
from .policy_engine import detect_naming_conflicts, enforce_task_policy, ensure_no_secrets, policy_evidence, scan_for_secrets
from .path_guard import revalidate_project_file
from .project_locator import locate_project
from .path_guard import resolve_project
from .report_generator import write_report
from .rollback import rollback_command
from .task_loader import load_task
from .validator import validate
from .runtime_guard import revalidate_runtime_path, safe_runtime_path, validate_task_id
from .runtime_state import ProjectLock, begin_attempt, fail_attempt, finish_attempt, move_to_recovery


def _restore(original: dict[Path, bytes], project: Path | None = None) -> None:
    for path, data in original.items():
        revalidate_project_file(project, path, must_exist=True)
        path.write_bytes(data)
    if project is not None:
        for name in ("PROJECT_CARD.md", "OPEN_LOOPS.md", "NOTES.md", "DRAFTS.md"):
            path = project / name
            if path.exists() and path not in original:
                revalidate_project_file(project, path, must_exist=True)
                path.unlink()


def _write_failure(runtime: Path, task_id: str, step: str, error: Exception, attempt: int = 0) -> tuple[Path, dict]:
    validate_task_id(task_id)
    reports = safe_runtime_path(runtime, "reports", task_id)
    reports.mkdir(parents=True, exist_ok=True)
    detail = str(error)
    if scan_for_secrets(detail):
        detail = "Potential secret detected. Details were suppressed."
    payload = {
        "task_id": task_id, "status": "failed", "failed_step": step, "attempt": attempt,
        "error": detail, "recovery": "Review the task and policy error; no external action was taken.",
    }
    serialized = json.dumps(payload, indent=2) + "\n"
    ensure_no_secrets(serialized, "error report")
    suffix = f"attempt-{attempt}" if attempt else "rejected"
    path = safe_runtime_path(runtime, "reports", task_id, f"{suffix}-error.json")
    path = revalidate_runtime_path(runtime, path)
    if not path.exists():
        path.write_text(serialized, encoding="utf-8")
    return path, payload


def _write_committed_recovery(runtime: Path, data: dict, error: Exception, running: Path | None) -> Path:
    detail = str(error)
    if scan_for_secrets(detail):
        detail = "Sensitive error details were suppressed."
    payload = {
        "task_id": data["task_id"], "status": "committed_needs_recovery",
        "commit_sha": data["ending_commit"], "error": detail,
        "recovery": f"python -m local_executor recover-finalization {data['task_id']} --repo <repo> --runtime <runtime>",
        "completion_data": data,
    }
    serialized = json.dumps(payload, indent=2) + "\n"
    ensure_no_secrets(serialized, "recovery record")
    return move_to_recovery(runtime, data["task_id"], running, payload)


def execute(task_path: Path, repo: Path, runtime: Path, *, commit: bool = True, retry: bool = False) -> dict:
    step = "load task"
    phase = "validated"
    task_id = "invalid-task"
    original_bytes: dict[Path, bytes] = {}
    project: Path | None = None
    changed_rel: list[str] = []
    committed = False
    data: dict = {}
    attempt = 0
    running: Path | None = None
    lock: ProjectLock | None = None
    try:
        task, raw_task = load_task(task_path)
        task_id = task.task_id
        step = "enforce policy"
        ensure_no_secrets(json.dumps(raw_task, ensure_ascii=False, default=str), "task payload")
        enforce_task_policy(task)
        branch = require_safe_branch(repo)
        start = starting_commit(repo)
        if git(repo, "status", "--porcelain").strip():
            raise ExecutionError("repository must be clean before task execution")
        step = "claim task and project lock"
        project = resolve_project(repo, task)
        attempt, running = begin_attempt(runtime, task, project, retry=retry)
        lock = ProjectLock(runtime, project, task.task_id).acquire()
        step = "locate project"
        project, reviewed = locate_project(repo, task)
        original_bytes = {
            path: revalidate_project_file(project, path, must_exist=True).read_bytes()
            for path in reviewed
        }
        original_text = {path: data.decode("utf-8") for path, data in original_bytes.items()}
        ensure_no_secrets("\n".join(original_text.values()), "approved source content")
        conflicts = detect_naming_conflicts(reviewed, project)
        step = "create backup"
        backup_files(repo, project, reviewed, runtime, task.task_id, attempt)
        phase = "backed_up"
        step = "apply updates"
        result = apply_updates(project, task)
        phase = "edited"
        step = "validate"
        checks = validate(repo, project, task, original_text)
        phase = "validated_changes"
        diff = git(repo, "diff")
        ensure_no_secrets(diff, "generated diff")
        reports = safe_runtime_path(runtime, "reports")
        reports.mkdir(parents=True, exist_ok=True)
        diff_path = safe_runtime_path(runtime, "reports", task.task_id, f"attempt-{attempt}.diff")
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        revalidate_runtime_path(runtime, diff_path).write_text(diff, encoding="utf-8", newline="\n")
        phase = "artifacts_prepared"
        changed_rel = [path.relative_to(repo).as_posix() for path in result["changed"]]
        data = {
            "task_id": task.task_id, "project_number": task.project_number,
            "project_slug": task.project_slug, "starting_commit": start, "ending_commit": start,
            "branch": branch, "files_reviewed": [p.name for p in reviewed],
            "files_changed": [p.name for p in result["changed"]],
            "facts_added": result["facts_added"], "loops_added": result["loops_added"],
            "loops_resolved": result["loops_resolved"], "notes_added": result["notes_added"],
            "drafts_saved": result["drafts_saved"], "conflicts": conflicts,
            "validation": checks, "diff_path": str(diff_path), "push_performed": False,
            "approval_required": ["review Git diff", "approve before push or merge"],
            "attempt": attempt,
            "policy_enforcement": policy_evidence(task),
        }
        step = "create local commit"
        phase = "staged"
        end = make_local_commit(repo, f"project {task.project_number}: apply approved memory update", changed_rel) if commit else start
        committed = commit and end != start
        phase = "committed" if committed else "validated_changes"
        data["ending_commit"] = end
        data["rollback"] = rollback_command(end) if committed else "git restore -- <changed files>"
        report = write_report(runtime, data)
        data["report_path"] = str(report)
        serialized = json.dumps(data, indent=2) + "\n"
        ensure_no_secrets(serialized, "completed queue record")
        data["status"] = "completed"
        finish_attempt(runtime, task.task_id, running, data)
        running = None
        phase = "finalized"
        return data
    except Exception as exc:
        if committed:
            data["status"] = "committed_needs_recovery"
            data["recovery_record"] = str(_write_committed_recovery(runtime, data, exc, running))
            running = None
            return data
        if phase == "staged":
            unstage_paths(repo, changed_rel)
        if original_bytes and phase in {"backed_up", "edited", "validated_changes", "artifacts_prepared", "staged"}:
            _restore(original_bytes, project)
        _, failure_payload = _write_failure(runtime, task_id, step, exc, attempt)
        if running is not None:
            fail_attempt(runtime, task_id, running, attempt, failure_payload)
            running = None
        if isinstance(exc, ExecutorError):
            raise
        raise ExecutionError(f"{step} failed: {exc}") from exc
    finally:
        if lock is not None:
            lock.release()
