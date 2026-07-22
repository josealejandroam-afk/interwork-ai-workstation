from pathlib import Path, PurePosixPath

from .errors import PolicyError
from .task_schema import APPROVED_FILES, Task


def _safe_relative(value: str) -> PurePosixPath:
    normalized = value.replace("\\", "/").rstrip("/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise PolicyError(f"unsafe or traversing path: {value}")
    return path


def resolve_project(repo: Path, task: Task) -> Path:
    expected = PurePosixPath("memory", "clients", task.client_slug, "projects", task.project_slug)
    allowed = {_safe_relative(item) for item in task.allowed_paths}
    if expected not in allowed:
        raise PolicyError("project path is outside allowed_paths")
    candidate = (repo / Path(*expected.parts)).resolve()
    repo_root = repo.resolve()
    if repo_root not in candidate.parents:
        raise PolicyError("resolved project path escaped repository")
    if not candidate.is_dir():
        raise PolicyError(f"requested project folder does not exist: {expected.as_posix()}")
    if not candidate.name.startswith(f"{task.project_number}_"):
        raise PolicyError("project number conflicts with resolved folder")
    return candidate


def guard_project_file(project: Path, path: Path) -> None:
    resolved = path.resolve()
    if resolved.parent != project.resolve() or resolved.name not in APPROVED_FILES:
        raise PolicyError(f"file is not approved for modification: {path}")
