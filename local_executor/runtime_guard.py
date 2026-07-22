from __future__ import annotations

import re
from pathlib import Path

from .errors import PolicyError, TaskValidationError


TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def validate_task_id(value: str) -> str:
    if not isinstance(value, str) or not TASK_ID_PATTERN.fullmatch(value):
        raise TaskValidationError("task_id must be 1-128 characters using only letters, numbers, periods, underscores, or hyphens")
    if value.startswith(".") or value.endswith((" ", ".")) or ".." in value:
        raise TaskValidationError("task_id contains a prohibited path-like sequence")
    if value.split(".", 1)[0].upper() in WINDOWS_RESERVED:
        raise TaskValidationError("task_id uses a reserved Windows device name")
    return value


def safe_runtime_path(runtime_root: Path, *parts: str) -> Path:
    root = runtime_root.resolve()
    candidate = root.joinpath(*parts).resolve(strict=False)
    if candidate == root or root not in candidate.parents:
        raise PolicyError("runtime destination escaped the configured runtime root")
    return candidate


def revalidate_runtime_path(runtime_root: Path, path: Path) -> Path:
    root = runtime_root.resolve()
    candidate = path.resolve(strict=False)
    if candidate == root or root not in candidate.parents:
        raise PolicyError("runtime destination escaped the configured runtime root")
    return candidate
