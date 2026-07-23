from __future__ import annotations

import json
import time
import traceback
from pathlib import Path

from .errors import ExecutorError
from .executor import execute
from .git_manager import git


def ensure_branch(repo: Path, branch: str) -> None:
    current = git(repo, "branch", "--show-current").strip()
    if current == branch:
        return
    existing = git(repo, "branch", "--list", branch).strip()
    git(repo, "checkout", branch) if existing else git(repo, "checkout", "-b", branch)


def pending_tasks(inbox: Path) -> list[Path]:
    pending = inbox / "pending"
    pending.mkdir(parents=True, exist_ok=True)
    return sorted(pending.glob("*.json"))


def _archive(path: Path, inbox: Path, subfolder: str, note: str | None = None) -> Path:
    destination_dir = inbox / subfolder
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / path.name
    path.replace(destination)
    if note:
        destination.with_suffix(".error.txt").write_text(note, encoding="utf-8")
    return destination


def process_one(repo: Path, runtime: Path, inbox: Path, task_path: Path) -> dict:
    try:
        json.loads(task_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        _archive(task_path, inbox, "rejected", f"invalid JSON: {exc}")
        return {"status": "rejected", "task_path": str(task_path), "error": str(exc)}
    try:
        result = execute(task_path, repo, runtime, commit=True)
    except ExecutorError as exc:
        task_id = task_path.stem
        _archive(task_path, inbox, "rejected", str(exc))
        return {"status": "rejected", "task_id": task_id, "error": str(exc)}
    _archive(task_path, inbox, "submitted")
    return result


def run_cycle(repo: Path, runtime: Path, inbox: Path, branch: str) -> list[dict]:
    tasks = pending_tasks(inbox)
    if not tasks:
        return []
    if git(repo, "status", "--porcelain").strip():
        print("watcher: repository is not clean; skipping this cycle until it's clean again")
        return []
    ensure_branch(repo, branch)
    results = []
    for task_path in tasks:
        try:
            result = process_one(repo, runtime, inbox, task_path)
        except Exception:
            print(f"watcher: unexpected error processing {task_path}")
            traceback.print_exc()
            continue
        results.append(result)
        print(json.dumps(result, indent=2))
    return results


def watch(repo: Path, runtime: Path, inbox: Path, branch: str, poll_seconds: float = 5.0, iterations: int | None = None) -> None:
    count = 0
    while iterations is None or count < iterations:
        run_cycle(repo, runtime, inbox, branch)
        count += 1
        if iterations is None or count < iterations:
            time.sleep(poll_seconds)
