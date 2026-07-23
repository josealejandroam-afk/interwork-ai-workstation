from __future__ import annotations

import json
import os
import socket
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ExecutionError, ExecutorError
from .git_manager import git
from .runtime_guard import safe_runtime_path, validate_task_id
from .task_schema import Task
from .watcher import DEFAULT_BRANCH, run_cycle


MAX_RESPONSE_BYTES = 1_048_576


@dataclass(frozen=True)
class RemoteClaim:
    queue_id: str
    claim_token: str
    task: dict[str, Any]


class RemoteQueueClient:
    def __init__(self, url: str, api_key: str, token: str):
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.token = token

    @classmethod
    def from_environment(cls, token_variable: str) -> "RemoteQueueClient":
        url = os.environ.get("SUPABASE_URL", "").strip()
        api_key = (
            os.environ.get("SUPABASE_PUBLISHABLE_KEY", "").strip()
            or os.environ.get("SUPABASE_ANON_KEY", "").strip()
        )
        token = os.environ.get(token_variable, "").strip()
        missing = [
            name for name, value in (
                ("SUPABASE_URL", url),
                ("SUPABASE_PUBLISHABLE_KEY or SUPABASE_ANON_KEY", api_key),
                (token_variable, token),
            ) if not value
        ]
        if missing:
            raise ExecutionError(f"missing remote queue setting(s): {', '.join(missing)}")
        return cls(url, api_key, token)

    def _rpc(self, function: str, body: dict[str, Any]) -> list[dict[str, Any]]:
        request = urllib.request.Request(
            f"{self.url}/rest/v1/rpc/{function}",
            data=json.dumps(body, separators=(",", ":")).encode("utf-8"),
            headers={
                "apikey": self.api_key,
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            detail = exc.read(4096).decode("utf-8", errors="replace")
            raise ExecutionError(f"remote queue request failed ({exc.code}): {detail}") from exc
        except (OSError, urllib.error.URLError) as exc:
            raise ExecutionError(f"remote queue is unavailable: {type(exc).__name__}") from exc
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ExecutionError("remote queue response exceeded the safety limit")
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ExecutionError("remote queue returned an invalid response") from exc
        if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
            raise ExecutionError("remote queue returned an unexpected response")
        return data

    def submit(self, task: dict[str, Any]) -> dict[str, Any]:
        Task.from_dict(task)
        rows = self._rpc("enqueue_local_executor_task", {"p_token": self.token, "p_task": task})
        if len(rows) != 1:
            raise ExecutionError("remote queue did not confirm task submission")
        return rows[0]

    def claim(self, worker_id: str, lease_seconds: int = 900) -> RemoteClaim | None:
        rows = self._rpc(
            "claim_local_executor_task",
            {"p_token": self.token, "p_worker_id": worker_id, "p_lease_seconds": lease_seconds},
        )
        if not rows:
            return None
        if len(rows) != 1:
            raise ExecutionError("remote queue returned multiple claims")
        row = rows[0]
        task = row.get("task")
        if not isinstance(task, dict):
            raise ExecutionError("remote queue claim contained an invalid task")
        return RemoteClaim(str(row["queue_id"]), str(row["claim_token"]), task)

    def complete(self, claim: RemoteClaim, result: dict[str, Any]) -> dict[str, Any]:
        status = "submitted" if result.get("status") == "completed" else "rejected"
        rows = self._rpc(
            "complete_local_executor_task",
            {
                "p_token": self.token,
                "p_queue_id": claim.queue_id,
                "p_claim_token": claim.claim_token,
                "p_status": status,
                "p_result": result,
                "p_error": result.get("error"),
            },
        )
        if len(rows) != 1:
            raise ExecutionError("remote queue did not confirm task completion")
        return rows[0]


def load_task_file(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ExecutionError(f"cannot read task JSON: {exc}") from exc
    Task.from_dict(data)
    return data


def submit_task(path: Path, client: RemoteQueueClient) -> dict[str, Any]:
    return client.submit(load_task_file(path))


def _completed_result(runtime: Path, task_id: str) -> dict[str, Any] | None:
    path = safe_runtime_path(runtime, "queue", "completed", f"{validate_task_id(task_id)}.json")
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ExecutionError("local completed record is unreadable") from exc
    if not isinstance(data, dict) or data.get("status") != "completed":
        raise ExecutionError("local completed record is invalid")
    return data


def _write_pending(runtime: Path, task: dict[str, Any]) -> Path:
    task_id = validate_task_id(str(task["task_id"]))
    pending = safe_runtime_path(runtime, "inbox", "pending")
    pending.mkdir(parents=True, exist_ok=True)
    destination = pending / f"{task_id}.json"
    serialized = json.dumps(task, indent=2, ensure_ascii=False) + "\n"
    if destination.exists():
        try:
            existing = json.loads(destination.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ExecutionError("existing pending task is unreadable") from exc
        if existing != task:
            raise ExecutionError("pending task_id collision contains different content")
        return destination
    temporary = pending / f".{task_id}.{uuid.uuid4().hex}.tmp"
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return destination


def run_remote_cycle(
    repo: Path,
    runtime: Path,
    client: RemoteQueueClient,
    branch: str = DEFAULT_BRANCH,
    worker_id: str | None = None,
) -> list[dict[str, Any]]:
    local_results = run_cycle(repo, runtime, branch)
    if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
        return local_results
    claim = client.claim(worker_id or socket.gethostname())
    if claim is None:
        return local_results
    try:
        Task.from_dict(claim.task)
    except ExecutorError as exc:
        result = {"status": "rejected", "task_id": claim.task.get("task_id"), "error": str(exc)}
        client.complete(claim, result)
        return [*local_results, result]
    task_id = str(claim.task["task_id"])
    completed = _completed_result(runtime, task_id)
    if completed is not None:
        client.complete(claim, completed)
        return [*local_results, completed]
    try:
        _write_pending(runtime, claim.task)
        execution_results = run_cycle(repo, runtime, branch)
        if not execution_results:
            raise ExecutionError("claimed task was not processed")
        result = execution_results[-1]
    except ExecutionError as exc:
        result = {"status": "rejected", "task_id": task_id, "error": str(exc)}
    client.complete(claim, result)
    return [*local_results, result]
