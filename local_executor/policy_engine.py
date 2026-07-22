import json
import re
from pathlib import Path

from .errors import PolicyError
from .path_guard import revalidate_project_file
from .task_schema import PROHIBITED_ACTIONS, Task

PROTECTED_FIELDS = {
    "vendor_confirmed", "client_confirmed", "access_confirmed", "pm_assigned",
    "client_informed", "fastfield_submitted", "completion_report_sent", "actual_end_at",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"(?i)\b(?:https?|postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^\s/:@]+:[^\s/@]+@[^\s]+"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-(?:proj-|ant-api03-)?[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{16,}={0,2}\b"),
    re.compile(r"(?i)(?:api[_-]?key|secret|password|token|service[_-]?role[_-]?key)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)(?:AccountKey|SharedAccessKey|ClientSecret)\s*=\s*[^;\s]+"),
    re.compile(r"(?i)https?://[^\s]+[?&](?:token|key|secret|signature|sig)=[^&\s]+"),
)


def enforce_task_policy(task: Task) -> None:
    blocked = set(task.requested_actions) & (PROHIBITED_ACTIONS | set(task.prohibited_actions))
    if blocked:
        raise PolicyError(f"prohibited action requested: {', '.join(sorted(blocked))}")
    payload = json.dumps(task.all_update_items(), ensure_ascii=False, default=str)
    payload_lower = payload.lower()
    touched = sorted(field for field in PROTECTED_FIELDS if field in payload_lower)
    if touched:
        raise PolicyError(f"protected confirmation field requested: {', '.join(touched)}")
    ensure_no_secrets(payload, "task payload")


def scan_for_secrets(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def ensure_no_secrets(text: str, context: str = "approved content") -> None:
    if scan_for_secrets(text):
        raise PolicyError(f"Potential secret detected in {context}. Processing stopped before persistence.")


def policy_evidence(task: Task) -> dict[str, bool]:
    return {
        "action_allowlisted": task.action == "apply_project_update",
        "internal_prohibited_actions_enforced": not bool(set(task.requested_actions) & PROHIBITED_ACTIONS),
        "external_adapters_registered": False,
        "prohibited_command_path_invoked": False,
    }


def detect_naming_conflicts(files: list[Path], project: Path | None = None) -> list[str]:
    combined = "\n".join(
        (revalidate_project_file(project, path, must_exist=True) if project else path).read_text(encoding="utf-8")
        for path in files
    )
    has_mma = bool(re.search(r"\bMMA\b", combined, re.IGNORECASE))
    has_mmc_res = bool(re.search(r"\bMMC\s+RES\b", combined, re.IGNORECASE))
    return ["MMA versus MMC RES naming remains unresolved; no automatic normalization was performed"] if has_mma and has_mmc_res else []
