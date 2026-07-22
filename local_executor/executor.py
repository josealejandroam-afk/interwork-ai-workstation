from __future__ import annotations

import json
import shutil
from pathlib import Path

from .backup_manager import backup_files
from .errors import ExecutorError, ExecutionError
from .git_manager import git, make_local_commit, require_safe_branch, starting_commit
from .markdown_editor import apply_updates
from .policy_engine import detect_naming_conflicts, enforce_task_policy
from .project_locator import locate_project
from .report_generator import write_report
from .rollback import rollback_command
from .task_loader import load_task
from .validator import validate


def _restore(original: dict[Path, bytes], project: Path | None = None) -> None:
    for path, data in original.items():
        path.write_bytes(data)
    if project is not None:
        for name in ("PROJECT_CARD.md", "OPEN_LOOPS.md", "NOTES.md", "DRAFTS.md"):
            path = project / name
            if path.exists() and path not in original:
                path.unlink()


def _write_failure(runtime: Path, task_id: str, step: str, error: Exception) -> Path:
    failed = runtime / "queue" / "failed"
    reports = runtime / "reports"
    failed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    payload = {
        "task_id": task_id, "status": "failed", "failed_step": step,
        "error": str(error), "recovery": "Review the task and policy error; no external action was taken.",
    }
    path = reports / f"{task_id}-error.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (failed / f"{task_id}.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def execute(task_path: Path, repo: Path, runtime: Path, *, commit: bool = True) -> dict:
    step = "load task"
    task_id = task_path.stem
    original_bytes: dict[Path, bytes] = {}
    project: Path | None = None
    try:
        task, _ = load_task(task_path)
        task_id = task.task_id
        step = "enforce policy"
        enforce_task_policy(task)
        branch = require_safe_branch(repo)
        start = starting_commit(repo)
        if git(repo, "status", "--porcelain").strip():
            raise ExecutionError("repository must be clean before task execution")
        step = "locate project"
        project, reviewed = locate_project(repo, task)
        original_bytes = {path: path.read_bytes() for path in reviewed}
        original_text = {path: data.decode("utf-8") for path, data in original_bytes.items()}
        conflicts = detect_naming_conflicts(reviewed)
        step = "create backup"
        backup_files(repo, project, reviewed, runtime / "backups", task.task_id)
        step = "apply updates"
        result = apply_updates(project, task)
        step = "validate"
        checks = validate(repo, project, task, original_text)
        diff = git(repo, "diff")
        reports = runtime / "reports"
        reports.mkdir(parents=True, exist_ok=True)
        diff_path = reports / f"{task.task_id}.diff"
        diff_path.write_text(diff, encoding="utf-8", newline="\n")
        changed_rel = [path.relative_to(repo).as_posix() for path in result["changed"]]
        step = "create local commit"
        end = make_local_commit(repo, f"project {task.project_number}: apply approved memory update", changed_rel) if commit else start
        data = {
            "task_id": task.task_id, "project_number": task.project_number,
            "project_slug": task.project_slug, "starting_commit": start, "ending_commit": end,
            "branch": branch, "files_reviewed": [p.name for p in reviewed],
            "files_changed": [p.name for p in result["changed"]],
            "facts_added": result["facts_added"], "loops_added": result["loops_added"],
            "loops_resolved": result["loops_resolved"], "notes_added": result["notes_added"],
            "drafts_saved": result["drafts_saved"], "conflicts": conflicts,
            "validation": checks, "diff_path": str(diff_path),
            "push_performed": False, "rollback": rollback_command(end) if commit and end != start else "git restore -- <changed files>",
            "approval_required": ["review Git diff", "approve before push or merge"],
        }
        report = write_report(reports, data)
        data["report_path"] = str(report)
        completed = runtime / "queue" / "completed"
        completed.mkdir(parents=True, exist_ok=True)
        (completed / f"{task.task_id}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return data
    except Exception as exc:
        if original_bytes:
            _restore(original_bytes, project)
        _write_failure(runtime, task_id, step, exc)
        if isinstance(exc, ExecutorError):
            raise
        raise ExecutionError(f"{step} failed: {exc}") from exc
