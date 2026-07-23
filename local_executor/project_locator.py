from pathlib import Path

from .path_guard import resolve_project
from .task_schema import APPROVED_FILES, Task


def locate_project(repo: Path, task: Task) -> tuple[Path, list[Path]]:
    project = resolve_project(repo, task)
    files = sorted((p for p in project.iterdir() if p.is_file() and p.name in APPROVED_FILES), key=lambda p: p.name)
    card = project / "PROJECT_CARD.md"
    if not card.exists():
        raise FileNotFoundError("PROJECT_CARD.md is required")
    return project, files
