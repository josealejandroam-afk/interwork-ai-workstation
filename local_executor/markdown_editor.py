from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import TaskValidationError
from .path_guard import revalidate_project_file
from .policy_engine import ensure_no_secrets
from .task_schema import Task


def _text(item: Any, *, fact: bool = False) -> str:
    if isinstance(item, str):
        value = item.strip()
    elif isinstance(item, dict):
        if fact and "field" in item and "value" in item:
            value = f"{item['field']}: {item['value']}"
        else:
            value = str(item.get("item", item.get("text", item.get("content", "")))).strip()
    else:
        value = ""
    if not value or "\n" in value or "\r" in value:
        raise TaskValidationError("update items must be non-empty single-line strings or supported objects")
    return value


def _append_section(path: Path, heading: str, items: list[str]) -> bool:
    if not items:
        return False
    current = path.read_text(encoding="utf-8") if path.exists() else f"# {path.stem.title()}\n"
    block = f"\n## {heading}\n\n" + "\n".join(f"- {item}" for item in items) + "\n"
    proposed = current.rstrip() + "\n" + block
    ensure_no_secrets(proposed, "proposed project content")
    path.write_text(proposed, encoding="utf-8", newline="\n")
    return True


def _resolve_loops(path: Path, requested: list[str]) -> tuple[bool, list[str]]:
    if not requested or not path.exists():
        return False, []
    text = path.read_text(encoding="utf-8")
    resolved = []
    lines = text.splitlines()
    for item in requested:
        for index, line in enumerate(lines):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[1] == item and cells[-1].lower() not in {"resolved", "closed", "complete"}:
                cells[-1] = "Resolved"
                lines[index] = "| " + " | ".join(cells) + " |"
                resolved.append(item)
                break
    if resolved:
        proposed = "\n".join(lines) + "\n"
        ensure_no_secrets(proposed, "proposed project content")
        path.write_text(proposed, encoding="utf-8", newline="\n")
    return bool(resolved), resolved


def apply_updates(project: Path, task: Task) -> dict:
    paths = {name: project / name for name in ("PROJECT_CARD.md", "OPEN_LOOPS.md", "NOTES.md", "DRAFTS.md")}
    for path in paths.values():
        revalidate_project_file(project, path)
    changed = []
    facts = [_text(item, fact=True) for item in task.confirmed_facts]
    added = [_text(item) for item in task.open_loops_to_add]
    requested_resolutions = [_text(item) for item in task.open_loops_to_resolve]
    notes = [_text(item) for item in task.notes_to_add]
    drafts = [_text(item) for item in task.drafts_to_save]
    revalidate_project_file(project, paths["PROJECT_CARD.md"], must_exist=True)
    if _append_section(paths["PROJECT_CARD.md"], f"Confirmed Update - {task.task_id}", facts):
        changed.append(paths["PROJECT_CARD.md"])
    revalidate_project_file(project, paths["OPEN_LOOPS.md"])
    did_resolve, resolved = _resolve_loops(paths["OPEN_LOOPS.md"], requested_resolutions)
    if did_resolve:
        changed.append(paths["OPEN_LOOPS.md"])
    revalidate_project_file(project, paths["OPEN_LOOPS.md"])
    if _append_section(paths["OPEN_LOOPS.md"], f"Added by {task.task_id}", added):
        changed.append(paths["OPEN_LOOPS.md"])
    revalidate_project_file(project, paths["NOTES.md"])
    if _append_section(paths["NOTES.md"], f"Update {task.task_id}", notes):
        changed.append(paths["NOTES.md"])
    revalidate_project_file(project, paths["DRAFTS.md"])
    if _append_section(paths["DRAFTS.md"], f"Saved by {task.task_id}", drafts):
        changed.append(paths["DRAFTS.md"])
    return {
        "changed": sorted(set(changed)), "facts_added": len(facts),
        "loops_added": added, "loops_resolved": resolved,
        "unresolved_resolution_requests": [x for x in requested_resolutions if x not in resolved],
        "notes_added": len(notes), "drafts_saved": len(drafts),
    }
