import hashlib
import json
import shutil
from pathlib import Path

from .git_manager import git
from .path_guard import guard_project_file


def backup_files(repo: Path, project: Path, files: list[Path], backup_root: Path, task_id: str) -> list[dict]:
    destination = backup_root / task_id
    destination.mkdir(parents=True, exist_ok=False)
    commit = git(repo, "rev-parse", "HEAD").strip()
    records = []
    for source in files:
        guard_project_file(project, source)
        data = source.read_bytes()
        target = destination / source.name
        shutil.copy2(source, target)
        records.append({
            "file": source.name,
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_commit": commit,
            "backup": str(target),
        })
    (destination / "manifest.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    return records
