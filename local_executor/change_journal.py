from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .atomic_io import atomic_write_bytes
from .path_guard import revalidate_project_file
from .runtime_guard import revalidate_runtime_path, safe_runtime_path


class ChangeJournal:
    def __init__(
        self, runtime: Path, task_id: str, attempt: int, project: Path,
        original_hashes: dict[Path, str],
    ) -> None:
        self.runtime = runtime
        self.task_id = task_id
        self.attempt = attempt
        self.project = project.resolve()
        self.original_hashes = original_hashes
        self.folder = safe_runtime_path(runtime, "journals", task_id, f"attempt-{attempt}")
        self.folder.mkdir(parents=True, exist_ok=True)
        self._sequence = 0
        self._pending: dict[Path, Path] = {}

    def before_replace(self, path: Path, data: bytes) -> None:
        revalidate_project_file(self.project, path)
        self._sequence += 1
        entry = safe_runtime_path(self.runtime, "journals", self.task_id, f"attempt-{self.attempt}", f"{self._sequence:04d}.json")
        payload = {
            "task_id": self.task_id,
            "attempt": self.attempt,
            "canonical_project_file": str(path.resolve(strict=False)),
            "original_sha256": self.original_hashes.get(path),
            "intended_post_sha256": hashlib.sha256(data).hexdigest(),
            "created_by_task": path not in self.original_hashes,
            "state": "prepared",
        }
        atomic_write_bytes(revalidate_runtime_path(self.runtime, entry), (json.dumps(payload, indent=2) + "\n").encode("utf-8"))
        self._pending[path] = entry

    def after_replace(self, path: Path) -> None:
        entry = self._pending.pop(path)
        payload = json.loads(revalidate_runtime_path(self.runtime, entry).read_text(encoding="utf-8"))
        payload["state"] = "applied"
        atomic_write_bytes(entry, (json.dumps(payload, indent=2) + "\n").encode("utf-8"))

    def recovery_expectations(self) -> tuple[dict[Path, str], set[Path]]:
        expected: dict[Path, str] = {}
        created: set[Path] = set()
        for entry in sorted(self.folder.glob("*.json")):
            payload = json.loads(revalidate_runtime_path(self.runtime, entry).read_text(encoding="utf-8"))
            path = Path(payload["canonical_project_file"])
            expected[path] = payload["intended_post_sha256"]
            if payload["created_by_task"]:
                created.add(path)
        return expected, created
