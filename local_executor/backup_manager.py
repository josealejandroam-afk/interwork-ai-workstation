import hashlib
import json
import shutil
from pathlib import Path

from .git_manager import git
from .path_guard import revalidate_project_file
from .policy_engine import ensure_no_secrets
from .runtime_guard import safe_runtime_path, revalidate_runtime_path


def backup_files(repo: Path, project: Path, files: list[Path], runtime: Path, task_id: str, attempt: int = 1) -> list[dict]:
    destination = safe_runtime_path(runtime, "backups", task_id, f"attempt-{attempt}")
    revalidate_runtime_path(runtime, destination)
    destination.mkdir(parents=True, exist_ok=False)
    commit = git(repo, "rev-parse", "HEAD").strip()
    records = []
    for source in files:
        revalidate_project_file(project, source, must_exist=True)
        data = source.read_bytes()
        ensure_no_secrets(data.decode("utf-8"), "approved source content")
        target = destination / source.name
        revalidate_runtime_path(runtime, target)
        shutil.copy2(source, target)
        records.append({
            "file": source.name,
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_commit": commit,
            "backup": str(target),
        })
    manifest = revalidate_runtime_path(runtime, destination / "manifest.json")
    manifest.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return records
