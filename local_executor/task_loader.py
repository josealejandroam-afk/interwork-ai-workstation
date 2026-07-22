import json
from pathlib import Path

from .errors import TaskValidationError
from .task_schema import Task


def load_task(path: Path) -> tuple[Task, dict]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TaskValidationError(f"invalid task JSON: {exc}") from exc
    return Task.from_dict(data), data
