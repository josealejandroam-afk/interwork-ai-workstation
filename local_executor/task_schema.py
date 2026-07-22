from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import TaskValidationError


APPROVED_FILES = {"PROJECT_CARD.md", "OPEN_LOOPS.md", "NOTES.md", "DRAFTS.md"}
SUPPORTED_ACTION = "apply_project_update"
PROHIBITED_ACTIONS = {
    "git_push", "git_merge", "supabase_write", "send_email", "send_teams",
    "send_calendar_invite", "smartsheet_write", "delete_files", "install_packages",
    "modify_credentials", "modify_access_controls",
}
PLACEHOLDERS = {"TBD", "UNKNOWN", "TO BE DETERMINED", "???", "<PLACEHOLDER>"}


def _string_list(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise TaskValidationError(f"{key} must be an array")
    return value


@dataclass(frozen=True)
class Task:
    task_id: str
    project_number: str
    client_slug: str
    project_slug: str
    action: str
    instructions: str
    source_type: str
    confirmed_facts: list[Any] = field(default_factory=list)
    open_loops_to_add: list[Any] = field(default_factory=list)
    open_loops_to_resolve: list[Any] = field(default_factory=list)
    notes_to_add: list[Any] = field(default_factory=list)
    drafts_to_save: list[Any] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    prohibited_actions: list[str] = field(default_factory=list)
    approval_required_before: list[str] = field(default_factory=list)
    requested_actions: list[str] = field(default_factory=list)
    maximum_attempts: int = 1

    @classmethod
    def from_dict(cls, data: Any) -> "Task":
        if not isinstance(data, dict):
            raise TaskValidationError("task JSON must contain an object")
        required = ("task_id", "project_number", "client_slug", "project_slug", "action", "allowed_paths")
        for key in required:
            if key not in data or data[key] in (None, "", []):
                raise TaskValidationError(f"missing required field: {key}")
        for key in ("task_id", "project_number", "client_slug", "project_slug", "action"):
            if not isinstance(data[key], str):
                raise TaskValidationError(f"{key} must be a string")
        attempts = data.get("maximum_attempts", 1)
        if not isinstance(attempts, int) or attempts < 1:
            raise TaskValidationError("maximum_attempts must be a positive integer")
        task = cls(
            task_id=data["task_id"], project_number=data["project_number"],
            client_slug=data["client_slug"], project_slug=data["project_slug"],
            action=data["action"], instructions=str(data.get("instructions", "")),
            source_type=str(data.get("source_type", "")),
            confirmed_facts=_string_list(data, "confirmed_facts"),
            open_loops_to_add=_string_list(data, "open_loops_to_add"),
            open_loops_to_resolve=_string_list(data, "open_loops_to_resolve"),
            notes_to_add=_string_list(data, "notes_to_add"),
            drafts_to_save=_string_list(data, "drafts_to_save"),
            allowed_paths=[str(x) for x in _string_list(data, "allowed_paths")],
            prohibited_actions=[str(x) for x in _string_list(data, "prohibited_actions")],
            approval_required_before=[str(x) for x in _string_list(data, "approval_required_before")],
            requested_actions=[str(x) for x in _string_list(data, "requested_actions")],
            maximum_attempts=attempts,
        )
        task.validate_content()
        return task

    def validate_content(self) -> None:
        if self.action != SUPPORTED_ACTION:
            raise TaskValidationError(f"unsupported action: {self.action}")
        if not self.project_slug.startswith(f"{self.project_number}_"):
            raise TaskValidationError("project number conflicts with project folder name")
        requested = {self.action, *self.requested_actions}
        blocked = requested & (PROHIBITED_ACTIONS | set(self.prohibited_actions))
        if blocked:
            raise TaskValidationError(f"task requests prohibited action(s): {', '.join(sorted(blocked))}")
        for item in self.all_update_items():
            for value in _leaf_strings(item):
                if value.strip().upper() in PLACEHOLDERS:
                    raise TaskValidationError(f"unsupported placeholder supplied: {value}")

    def all_update_items(self) -> list[Any]:
        return [*self.confirmed_facts, *self.open_loops_to_add,
                *self.open_loops_to_resolve, *self.notes_to_add, *self.drafts_to_save]


def _leaf_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from _leaf_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _leaf_strings(nested)
