import re
from pathlib import Path

from .errors import PolicyError
from .task_schema import PROHIBITED_ACTIONS, Task

PROTECTED_FIELDS = {
    "vendor_confirmed", "client_confirmed", "access_confirmed", "pm_assigned",
    "client_informed", "fastfield_submitted", "completion_report_sent", "actual_end_at",
}
SECRET_PATTERN = re.compile(
    r"(?i)(api[_-]?key|secret|password|token|service[_-]?role[_-]?key)\s*[:=]\s*[^\s]+"
)


def enforce_task_policy(task: Task) -> None:
    blocked = set(task.requested_actions) & (PROHIBITED_ACTIONS | set(task.prohibited_actions))
    if blocked:
        raise PolicyError(f"prohibited action requested: {', '.join(sorted(blocked))}")
    payload = repr(task.all_update_items()).lower()
    touched = sorted(field for field in PROTECTED_FIELDS if field in payload)
    if touched:
        raise PolicyError(f"protected confirmation field requested: {', '.join(touched)}")
    if SECRET_PATTERN.search(payload):
        raise PolicyError("possible secret detected in task payload")


def scan_for_secrets(text: str) -> bool:
    return bool(SECRET_PATTERN.search(text))


def detect_naming_conflicts(files: list[Path]) -> list[str]:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    has_mma = bool(re.search(r"\bMMA\b", combined, re.IGNORECASE))
    has_mmc_res = bool(re.search(r"\bMMC\s+RES\b", combined, re.IGNORECASE))
    return ["MMA versus MMC RES naming remains unresolved; no automatic normalization was performed"] if has_mma and has_mmc_res else []
