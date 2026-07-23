from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path

from .errors import ExecutionError, ExecutorError
from .executor import execute
from .git_manager import git
from .runtime_guard import revalidate_runtime_path, safe_runtime_path


DEFAULT_BRANCH = "executor/auto"


def _inbox_path(runtime: Path, folder: str) -> Path:
    return safe_runtime_path(runtime, "inbox", folder)


def ensure_branch(repo: Path, branch: str) -> None:
    if branch in {"main", "master"}:
        raise ExecutionError("watcher branch must not be main or master")
    git(repo, "check-ref-format", "--branch", branch)
    current = git(repo, "branch", "--show-current").strip()
    if current == branch:
        return
    existing = git(repo, "branch", "--list", branch).strip()
    if existing:
        git(repo, "switch", branch)
        return
    git(repo, "rev-parse", "--verify", "refs/heads/main")
    git(repo, "switch", "-c", branch, "main")


def pending_tasks(runtime: Path) -> list[Path]:
    pending = _inbox_path(runtime, "pending")
    pending.mkdir(parents=True, exist_ok=True)
    return sorted(pending.glob("*.json"))


def _available_archive_path(destination_dir: Path, name: str) -> Path:
    destination = destination_dir / name
    if not destination.exists():
        return destination
    source = Path(name)
    return destination_dir / f"{source.stem}-{uuid.uuid4().hex}{source.suffix}"


def _claim(runtime: Path, task_path: Path) -> tuple[Path, str] | None:
    task_path = revalidate_runtime_path(runtime, task_path)
    processing = _inbox_path(runtime, "processing")
    processing.mkdir(parents=True, exist_ok=True)
    claimed = processing / f"{uuid.uuid4().hex}-{task_path.name}"
    try:
        os.replace(task_path, claimed)
    except FileNotFoundError:
        return None
    return claimed, task_path.name


def _archive(
    runtime: Path,
    path: Path,
    original_name: str,
    subfolder: str,
    note: str | None = None,
) -> Path:
    path = revalidate_runtime_path(runtime, path)
    destination_dir = _inbox_path(runtime, subfolder)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = _available_archive_path(destination_dir, original_name)
    os.replace(path, destination)
    if note:
        destination.with_suffix(".error.txt").write_text(note, encoding="utf-8")
    return destination


def process_one(repo: Path, runtime: Path, task_path: Path, original_name: str) -> dict:
    try:
        json.loads(task_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        error = f"invalid JSON: {exc}"
        _archive(runtime, task_path, original_name, "rejected", error)
        return {"status": "rejected", "task_path": original_name, "error": error}
    try:
        result = execute(task_path, repo, runtime, commit=True)
    except ExecutorError as exc:
        error = str(exc)
        _archive(runtime, task_path, original_name, "rejected", error)
        return {"status": "rejected", "task_path": original_name, "error": error}
    except Exception as exc:
        error = f"unexpected watcher error: {type(exc).__name__}"
        _archive(runtime, task_path, original_name, "rejected", error)
        return {"status": "rejected", "task_path": original_name, "error": error}
    _archive(runtime, task_path, original_name, "submitted")
    return result


def run_cycle(repo: Path, runtime: Path, branch: str = DEFAULT_BRANCH) -> list[dict]:
    tasks = pending_tasks(runtime)
    if not tasks:
        return []
    if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
        print("watcher: repository is not clean; pending tasks were left untouched")
        return []
    ensure_branch(repo, branch)
    results = []
    for task_path in tasks:
        if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
            print("watcher: repository became dirty; remaining pending tasks were left untouched")
            break
        claim = _claim(runtime, task_path)
        if claim is None:
            continue
        claimed_path, original_name = claim
        result = process_one(repo, runtime, claimed_path, original_name)
        results.append(result)
        print(json.dumps(result, indent=2))
    return results


def watch(
    repo: Path,
    runtime: Path,
    branch: str = DEFAULT_BRANCH,
    poll_seconds: float = 5.0,
    iterations: int | None = None,
) -> None:
    if poll_seconds <= 0:
        raise ExecutionError("poll interval must be greater than zero")
    count = 0
    while iterations is None or count < iterations:
        run_cycle(repo, runtime, branch)
        count += 1
        if iterations is None or count < iterations:
            time.sleep(poll_seconds)


def watch_remote(
    repo: Path,
    runtime: Path,
    client,
    branch: str = DEFAULT_BRANCH,
    poll_seconds: float = 5.0,
    iterations: int | None = None,
) -> None:
    from .remote_queue import run_remote_cycle

    if poll_seconds <= 0:
        raise ExecutionError("poll interval must be greater than zero")
    count = 0
    while iterations is None or count < iterations:
        run_remote_cycle(repo, runtime, client, branch)
        count += 1
        if iterations is None or count < iterations:
            time.sleep(poll_seconds)
