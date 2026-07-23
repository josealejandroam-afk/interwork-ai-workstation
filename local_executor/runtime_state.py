from __future__ import annotations

import hashlib
import json
import os
import socket
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .errors import ExecutionError, PolicyError
from .git_manager import git
from .runtime_guard import revalidate_runtime_path, safe_runtime_path
from .runtime_guard import validate_task_id


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_exclusive(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def _failure_records(runtime: Path, task_id: str) -> list[Path]:
    folder = safe_runtime_path(runtime, "queue", "failed", task_id)
    return sorted(folder.glob("attempt-*.json")) if folder.is_dir() else []


def _interrupted_records(runtime: Path, task_id: str) -> list[Path]:
    folder = safe_runtime_path(runtime, "queue", "interrupted", task_id)
    return sorted(folder.glob("attempt-*.json")) if folder.is_dir() else []


def begin_attempt(runtime: Path, task, project: Path, *, retry: bool = False) -> tuple[int, Path]:
    completed = safe_runtime_path(runtime, "queue", "completed", f"{task.task_id}.json")
    running = safe_runtime_path(runtime, "queue", "running", f"{task.task_id}.json")
    recovery = safe_runtime_path(runtime, "queue", "committed_needs_recovery", f"{task.task_id}.json")
    if completed.exists():
        raise ExecutionError("duplicate completed task_id; execution refused")
    if running.exists():
        raise ExecutionError("duplicate running task_id; execution refused")
    if recovery.exists():
        raise ExecutionError("task has a committed recovery state; finalize it before retrying")
    failures = _failure_records(runtime, task.task_id)
    interrupted = _interrupted_records(runtime, task.task_id)
    prior_attempts = [*failures, *interrupted]
    if prior_attempts and not retry:
        raise ExecutionError("failed or interrupted task requires an explicit retry invocation")
    attempt = len(prior_attempts) + 1
    if attempt > task.maximum_attempts:
        raise ExecutionError("maximum_attempts reached; execution refused")
    backup = safe_runtime_path(runtime, "backups", task.task_id)
    reports = safe_runtime_path(runtime, "reports", task.task_id)
    if (backup.exists() or reports.exists()) and not prior_attempts:
        raise ExecutionError("interrupted or duplicate task artifacts detected; inspect before recovery")
    pending = safe_runtime_path(runtime, "queue", "pending", f"{task.task_id}.json")
    if pending.exists():
        raise ExecutionError("duplicate pending task_id; execution refused")
    payload = {
        "task_id": task.task_id, "project_number": task.project_number,
        "canonical_project_path": str(project.resolve()), "process_id": os.getpid(),
        "hostname": socket.gethostname(), "started_at": _now(), "attempt": attempt,
    }
    revalidate_runtime_path(runtime, pending)
    _write_exclusive(pending, payload)
    running.parent.mkdir(parents=True, exist_ok=True)
    revalidate_runtime_path(runtime, running)
    os.replace(pending, running)
    return attempt, running


def finish_attempt(runtime: Path, task_id: str, running: Path, data: dict) -> Path:
    destination = safe_runtime_path(runtime, "queue", "completed", f"{task_id}.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    running = revalidate_runtime_path(runtime, running)
    revalidate_runtime_path(runtime, destination)
    running.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(running, destination)
    return destination


def fail_attempt(runtime: Path, task_id: str, running: Path | None, attempt: int, payload: dict) -> Path:
    folder = safe_runtime_path(runtime, "queue", "failed", task_id)
    folder.mkdir(parents=True, exist_ok=True)
    destination = safe_runtime_path(runtime, "queue", "failed", task_id, f"attempt-{attempt}.json")
    revalidate_runtime_path(runtime, destination)
    _write_exclusive(destination, payload)
    if running and running.exists():
        revalidate_runtime_path(runtime, running)
        running.unlink()
    return destination


def move_to_recovery(runtime: Path, task_id: str, running: Path | None, payload: dict) -> Path:
    destination = safe_runtime_path(runtime, "queue", "committed_needs_recovery", f"{task_id}.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    revalidate_runtime_path(runtime, destination)
    _write_exclusive(destination, payload)
    if running and running.exists():
        revalidate_runtime_path(runtime, running)
        running.unlink()
    return destination


def interrupt_attempt(runtime: Path, task_id: str, running: Path, attempt: int, reason: str) -> Path:
    folder = safe_runtime_path(runtime, "queue", "interrupted", task_id)
    folder.mkdir(parents=True, exist_ok=True)
    destination = safe_runtime_path(runtime, "queue", "interrupted", task_id, f"attempt-{attempt}.json")
    payload = json.loads(revalidate_runtime_path(runtime, running).read_text(encoding="utf-8"))
    payload.update({"status": "interrupted", "interrupted_at": _now(), "reason": reason})
    _write_exclusive(destination, payload)
    running.unlink()
    return destination


def project_lock_path(runtime: Path, project: Path) -> Path:
    key = hashlib.sha256(str(project.resolve()).casefold().encode("utf-8")).hexdigest()
    return safe_runtime_path(runtime, "locks", f"{key}.lock")


@dataclass
class ProjectLock:
    runtime: Path
    project: Path
    task_id: str
    path: Path | None = None

    def acquire(self) -> "ProjectLock":
        path = project_lock_path(self.runtime, self.project)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.mkdir()
        except FileExistsError as exc:
            raise ExecutionError("project is locked by another task; inspect the lock before recovery") from exc
        payload = {
            "task_id": self.task_id, "process_id": os.getpid(), "hostname": socket.gethostname(),
            "canonical_project_path": str(self.project.resolve()), "acquired_at": _now(),
            "executor_version": __version__,
        }
        metadata = revalidate_runtime_path(self.runtime, path / "lock.json")
        try:
            metadata.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        except Exception:
            if metadata.exists():
                metadata.unlink()
            path.rmdir()
            raise
        self.path = path
        return self

    def release(self) -> None:
        if not self.path or not self.path.exists():
            return
        metadata = revalidate_runtime_path(self.runtime, self.path / "lock.json")
        payload = json.loads(metadata.read_text(encoding="utf-8"))
        if payload.get("task_id") != self.task_id:
            raise PolicyError("lock ownership changed; automatic release refused")
        metadata.unlink()
        self.path.rmdir()
        self.path = None


def _process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes

        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        ctypes.windll.kernel32.CloseHandle(handle)
        return True
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def inspect_lock(runtime: Path, project: Path) -> dict:
    path = project_lock_path(runtime, project)
    if not path.is_dir():
        return {"locked": False, "canonical_project_path": str(project.resolve())}
    metadata = revalidate_runtime_path(runtime, path / "lock.json")
    try:
        data = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        return {"locked": True, "canonical_project_path": str(project.resolve()), "metadata_error": type(exc).__name__, "same_host": None, "process_alive": None}
    same_host = data.get("hostname") == socket.gethostname()
    data.update({"locked": True, "same_host": same_host, "process_alive": _process_alive(int(data.get("process_id", -1))) if same_host else None})
    return data


def recover_stale_lock(runtime: Path, project: Path, *, force: bool = False) -> dict:
    info = inspect_lock(runtime, project)
    if not info.get("locked"):
        return info
    if info.get("metadata_error") and not force:
        raise ExecutionError("lock metadata is missing or malformed; explicit --force recovery required")
    if info.get("same_host") and info.get("process_alive"):
        raise ExecutionError("lock owner process is still live; recovery refused")
    if not info.get("same_host") and not force:
        raise ExecutionError("lock belongs to another host; repeat explicit recovery with --force after review")
    path = project_lock_path(runtime, project)
    metadata = revalidate_runtime_path(runtime, path / "lock.json")
    if metadata.exists():
        metadata.unlink()
    path.rmdir()
    info["recovered"] = True
    return info


def inspect_running(runtime: Path, task_id: str) -> dict:
    validate_task_id(task_id)
    running = safe_runtime_path(runtime, "queue", "running", f"{task_id}.json")
    if not running.is_file():
        return {"running": False, "task_id": task_id}
    try:
        data = json.loads(revalidate_runtime_path(runtime, running).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        return {"running": True, "task_id": task_id, "metadata_error": type(exc).__name__, "process_alive": None, "lock": None}
    same_host = data.get("hostname") == socket.gethostname()
    try:
        pid = int(data.get("process_id", -1))
    except (TypeError, ValueError):
        pid = -1
    data.update({"running": True, "same_host": same_host, "process_alive": _process_alive(pid) if same_host else None})
    project_value = data.get("canonical_project_path")
    if project_value:
        data["lock"] = inspect_lock(runtime, Path(project_value))
    else:
        data["lock"] = None
    return data


def recover_running(runtime: Path, task_id: str, *, force: bool = False) -> dict:
    validate_task_id(task_id)
    info = inspect_running(runtime, task_id)
    if not info.get("running"):
        raise ExecutionError("running task record was not found")
    if info.get("same_host") and info.get("process_alive"):
        raise ExecutionError("running task process is still live; recovery refused")
    if (info.get("metadata_error") or not info.get("same_host")) and not force:
        raise ExecutionError("running record is remote or malformed; explicit --force recovery required")
    project_value = info.get("canonical_project_path")
    if project_value:
        lock_info = inspect_lock(runtime, Path(project_value))
        if lock_info.get("locked"):
            if lock_info.get("task_id") not in (None, task_id) and not force:
                raise ExecutionError("project lock belongs to a different task; explicit --force recovery required")
            recover_stale_lock(runtime, Path(project_value), force=force)
    running = safe_runtime_path(runtime, "queue", "running", f"{task_id}.json")
    folder = safe_runtime_path(runtime, "queue", "interrupted", task_id)
    folder.mkdir(parents=True, exist_ok=True)
    attempt = info.get("attempt", 0)
    destination = safe_runtime_path(runtime, "queue", "interrupted", task_id, f"attempt-{attempt or 'unknown'}.json")
    if destination.exists():
        destination = safe_runtime_path(runtime, "queue", "interrupted", task_id, f"recovered-{int(datetime.now().timestamp())}.json")
    os.replace(revalidate_runtime_path(runtime, running), revalidate_runtime_path(runtime, destination))
    info.update({"recovered": True, "interrupted_record": str(destination)})
    return info


def finalize_recovery(runtime: Path, repo: Path, task_id: str, write_report_callback) -> dict:
    recovery = safe_runtime_path(runtime, "queue", "committed_needs_recovery", f"{task_id}.json")
    if not recovery.is_file():
        raise ExecutionError("committed recovery record was not found")
    payload = json.loads(revalidate_runtime_path(runtime, recovery).read_text(encoding="utf-8"))
    data = payload["completion_data"]
    commit_sha = payload["commit_sha"]
    if git(repo, "rev-parse", "--verify", f"{commit_sha}^{{commit}}", check=False).strip() != commit_sha:
        raise ExecutionError("recovery commit SHA is not present in the repository")
    report = write_report_callback(runtime, data)
    data["report_path"] = str(report)
    data["status"] = "completed"
    completed = safe_runtime_path(runtime, "queue", "completed", f"{task_id}.json")
    completed.parent.mkdir(parents=True, exist_ok=True)
    recovery.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    os.replace(recovery, completed)
    return data
