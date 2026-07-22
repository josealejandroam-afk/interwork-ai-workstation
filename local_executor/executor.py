from __future__ import annotations

import json
import hashlib
import shutil
import uuid
from pathlib import Path

from .backup_manager import backup_files
from .errors import ExecutorError, ExecutionError
from .git_manager import git, make_local_commit, require_safe_branch, sha256_file, starting_commit, unstage_paths, verify_expected_changes
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
from .runtime_state import interrupt_attempt
from .atomic_io import atomic_write_bytes, cleanup_abandoned_temps
from .task_schema import APPROVED_FILES


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _restore(
    original: dict[Path, bytes], project: Path, expected_post: dict[Path, str], created: set[Path]
) -> list[dict]:
    conflicts: list[dict] = []
    for path, data in original.items():
        if path not in expected_post:
            continue
        revalidate_project_file(project, path, must_exist=True)
        current = sha256_file(path)
        if current != expected_post[path]:
            conflicts.append({"path": str(path), "original_sha256": _digest(data), "expected_post_sha256": expected_post[path], "current_sha256": current})
            continue
        atomic_write_bytes(path, data)
    for path in created:
        if not path.exists():
            continue
        revalidate_project_file(project, path, must_exist=True)
        current = sha256_file(path)
        if current != expected_post.get(path):
            conflicts.append({"path": str(path), "original_sha256": None, "expected_post_sha256": expected_post.get(path), "current_sha256": current})
            continue
        path.unlink()
    cleanup_abandoned_temps(project)
    return conflicts


def _write_manual_recovery(runtime: Path, task_id: str, attempt: int, conflicts: list[dict]) -> Path:
    folder = safe_runtime_path(runtime, "queue", "manual_recovery", task_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = safe_runtime_path(runtime, "queue", "manual_recovery", task_id, f"attempt-{attempt}.json")
    payload = {"task_id": task_id, "attempt": attempt, "status": "manual_recovery_required", "files": conflicts}
    revalidate_runtime_path(runtime, path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


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


def _execute_in_place(task_path: Path, repo: Path, runtime: Path, *, commit: bool = True, retry: bool = False) -> dict:
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
    expected_post: dict[Path, str] = {}
    created: set[Path] = set()
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
        original_hashes = {path: _digest(data) for path, data in original_bytes.items()}
        originally_absent = {project / name for name in APPROVED_FILES if not (project / name).exists()}
        ensure_no_secrets("\n".join(original_text.values()), "approved source content")
        conflicts = detect_naming_conflicts(reviewed, project)
        step = "create backup"
        backup_files(repo, project, reviewed, runtime, task.task_id, attempt)
        phase = "backed_up"
        step = "apply updates"
        phase = "edited"
        def record_write(path: Path) -> None:
            expected_post[path] = sha256_file(path)
            if path not in original_bytes:
                created.add(path)

        result = apply_updates(project, task, on_write=record_write, originally_absent=originally_absent)
        changed_paths_for_task = set(result["changed"])
        expected_post.update({path: sha256_file(path) for path in changed_paths_for_task})
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
        expected_rel = {path.relative_to(repo).as_posix(): expected_post[path] for path in result["changed"]}
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
            "file_hashes": {
                path.name: {"original_sha256": original_hashes.get(path), "expected_post_sha256": expected_post.get(path), "created_by_task": path in created}
                for path in result["changed"]
            },
        }
        step = "create local commit"
        phase = "staged"
        verify_expected_changes(repo, expected_rel)
        hooks_dir = safe_runtime_path(runtime, "policies", "empty-hooks", task.task_id, f"attempt-{attempt}")
        end = make_local_commit(
            repo, f"project {task.project_number}: apply approved memory update", changed_rel, expected_rel, hooks_dir
        ) if commit else start
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
    except KeyboardInterrupt:
        conflicts: list[dict] = []
        if original_bytes and expected_post and project is not None:
            conflicts = _restore(original_bytes, project, expected_post, created)
            if conflicts:
                _write_manual_recovery(runtime, task_id, attempt, conflicts)
        if running is not None:
            interrupt_attempt(runtime, task_id, running, attempt, "KeyboardInterrupt")
            running = None
        raise
    except Exception as exc:
        if committed:
            data["status"] = "committed_needs_recovery"
            data["recovery_record"] = str(_write_committed_recovery(runtime, data, exc, running))
            running = None
            return data
        if phase == "staged":
            unstage_paths(repo, changed_rel)
        recovery_conflicts: list[dict] = []
        if original_bytes and expected_post and project is not None and phase in {"edited", "validated_changes", "artifacts_prepared", "staged"}:
            recovery_conflicts = _restore(original_bytes, project, expected_post, created)
            if recovery_conflicts:
                recovery_path = _write_manual_recovery(runtime, task_id, attempt, recovery_conflicts)
                exc = ExecutionError(f"automatic rollback refused for externally changed files; manual recovery record: {recovery_path}")
        _, failure_payload = _write_failure(runtime, task_id, step, exc, attempt)
        if running is not None:
            fail_attempt(runtime, task_id, running, attempt, failure_payload)
            running = None
        if isinstance(exc, ExecutorError):
            raise exc
        raise ExecutionError(f"{step} failed: {exc}") from exc
    finally:
        if lock is not None:
            lock.release()


def _generate_proposal(task_path: Path, repo: Path, runtime: Path) -> dict:
    task, raw_task = load_task(task_path)
    ensure_no_secrets(json.dumps(raw_task, ensure_ascii=False, default=str), "task payload")
    enforce_task_policy(task)
    require_safe_branch(repo)
    if git(repo, "status", "--porcelain").strip():
        raise ExecutionError("repository must be clean before proposal generation")
    source_project, source_files = locate_project(repo, task)
    source_hashes = {path: sha256_file(path) for path in source_files}
    proposal_id = uuid.uuid4().hex
    proposal_root = safe_runtime_path(runtime, "proposals", task.task_id, proposal_id)
    workspace_repo = safe_runtime_path(runtime, "proposals", task.task_id, proposal_id, "workspace", "repo")
    relative_project = source_project.relative_to(repo)
    copied_project = workspace_repo / relative_project
    copied_project.mkdir(parents=True, exist_ok=True)
    for source in source_files:
        shutil.copy2(source, copied_project / source.name)
    git(workspace_repo, "init", "-b", "proposal")
    git(workspace_repo, "add", ".")
    baseline_hooks = safe_runtime_path(runtime, "proposals", task.task_id, proposal_id, "baseline-empty-hooks")
    baseline_hooks.mkdir(parents=True)
    git(
        workspace_repo, "-c", "user.name=Local Executor Proposal", "-c", "user.email=proposal@localhost",
        "-c", f"core.hooksPath={baseline_hooks.resolve()}", "-c", "commit.gpgSign=false",
        "commit", "--no-gpg-sign", "-m", "proposal baseline",
    )
    copied_task = safe_runtime_path(runtime, "proposals", task.task_id, proposal_id, "task.json")
    copied_task.write_text(json.dumps(raw_task, indent=2) + "\n", encoding="utf-8")
    inner_runtime = safe_runtime_path(runtime, "proposals", task.task_id, proposal_id, "runtime")
    result = _execute_in_place(copied_task, workspace_repo, inner_runtime, commit=False)
    current_source_hashes = {path: sha256_file(path) for path in source_files}
    if current_source_hashes != source_hashes:
        raise ExecutionError("source project changed during proposal generation; proposal rejected")
    state_dir = safe_runtime_path(runtime, "queue", "proposal_generated", task.task_id)
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path = safe_runtime_path(runtime, "queue", "proposal_generated", task.task_id, f"{proposal_id}.json")
    proposal = {
        **result, "status": "proposal_generated", "proposal_id": proposal_id,
        "source_project": str(source_project), "source_byte_identical": True,
        "proposal_workspace": str(proposal_root),
        "final_execution_task_id_consumed": False,
    }
    revalidate_runtime_path(runtime, state_path).write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    return proposal


def execute(task_path: Path, repo: Path, runtime: Path, *, commit: bool = True, retry: bool = False) -> dict:
    if not commit:
        return _generate_proposal(task_path, repo, runtime)
    return _execute_in_place(task_path, repo, runtime, commit=True, retry=retry)
