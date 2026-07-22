from __future__ import annotations

import re
from pathlib import Path

from .errors import ExecutionError
from .git_manager import changed_paths, git
from .policy_engine import PROTECTED_FIELDS, scan_for_secrets
from .path_guard import revalidate_project_file
from .task_schema import APPROVED_FILES, Task


PROJECT_REFERENCE = re.compile(r"(?i)\bproject(?:\s+number)?\s*(?:\||:|#|-)?\s*(\d{4,})\b")


def project_numbers(text: str) -> set[str]:
    return set(PROJECT_REFERENCE.findall(text))


def validate(repo: Path, project: Path, task: Task, original: dict[Path, str]) -> dict[str, str]:
    expected_prefix = project.relative_to(repo).as_posix() + "/"
    changed = changed_paths(repo)
    checks: dict[str, str] = {}
    allowed = all(path.startswith(expected_prefix) and Path(path).name in APPROVED_FILES for path in changed)
    checks["Allowed paths only"] = "PASS" if allowed else "FAIL"
    checks["No prohibited files changed"] = checks["Allowed paths only"]
    checks["No accidental deletion"] = "PASS" if all(not line.startswith(" D") for line in git(repo, "status", "--porcelain").splitlines()) else "FAIL"
    checks["No .env files changed"] = "PASS" if all(Path(path).name != ".env" and not Path(path).name.startswith(".env.") for path in changed) else "FAIL"
    approved = [path for path in project.iterdir() if path.is_file() and path.name in APPROVED_FILES]
    content = "\n".join(revalidate_project_file(project, path, must_exist=True).read_text(encoding="utf-8") for path in approved)
    checks["Valid UTF-8 text"] = "PASS"
    checks["No secrets detected"] = "FAIL" if scan_for_secrets(content) else "PASS"
    before = "\n".join(original.values()).lower()
    protected_changed = any(before.count(field) != content.lower().count(field) for field in PROTECTED_FIELDS)
    checks["Protected fields unchanged"] = "PASS" if not protected_changed else "FAIL"
    before_numbers = project_numbers("\n".join(original.values()))
    after_numbers = project_numbers(content)
    introduced_conflicts = after_numbers - before_numbers - {task.project_number}
    checks["Project number unchanged"] = "PASS" if task.project_number in after_numbers and not introduced_conflicts else "FAIL"
    checks["Valid JSON task record"] = "PASS"
    checks["Clean markdown formatting"] = "PASS" if git(repo, "diff", "--check", check=False).strip() == "" else "FAIL"
    checks["Git diff check"] = checks["Clean markdown formatting"]
    failures = [name for name, result in checks.items() if result != "PASS"]
    if failures:
        raise ExecutionError(f"validation failed: {', '.join(failures)}")
    return checks
