from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from .errors import TaskValidationError
from .path_guard import revalidate_project_file
from .policy_engine import ensure_no_secrets
from .task_schema import Task
from .atomic_io import atomic_write_bytes


def _read_markdown(path: Path) -> tuple[str, str, bool, str]:
    data = path.read_bytes()
    encoding = "utf-8-sig" if data.startswith(b"\xef\xbb\xbf") else "utf-8"
    text = data.decode(encoding)
    newline = "\r\n" if b"\r\n" in data else "\n"
    final_newline = text.endswith(("\n", "\r"))
    return text, newline, final_newline, encoding


def _write_markdown(path: Path, text: str, encoding: str, before_replace=None, after_replace=None) -> None:
    atomic_write_bytes(path, text.encode(encoding), before_replace=before_replace, after_replace=after_replace)


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


def _append_section(project: Path, path: Path, heading: str, items: list[str], default_newline: str = "\n", expected_absent: bool = False, before_replace=None, after_replace=None) -> bool:
    if not items:
        return False
    if expected_absent and path.exists():
        raise TaskValidationError(f"approved optional file appeared externally during execution: {path.name}")
    revalidate_project_file(project, path)
    if path.exists():
        current, newline, had_final_newline, encoding = _read_markdown(path)
    else:
        titles = {"PROJECT_CARD": "Project Card", "OPEN_LOOPS": "Open Loops", "NOTES": "Notes", "DRAFTS": "Drafts"}
        newline, had_final_newline, encoding = default_newline, True, "utf-8"
        current = f"# {titles.get(path.stem, path.stem.title())}{newline}"
    separator = "" if current.endswith(newline * 2) else (newline if current.endswith(newline) else newline * 2)
    block = f"## {heading}{newline}{newline}" + newline.join(f"- {item}" for item in items)
    proposed = current + separator + block + (newline if had_final_newline else "")
    ensure_no_secrets(proposed, "proposed project content")
    revalidate_project_file(project, path)
    _write_markdown(path, proposed, encoding, before_replace, after_replace)
    return True


def _resolve_loops(project: Path, path: Path, requested: list[str], expected_absent: bool = False, before_replace=None, after_replace=None) -> tuple[bool, list[str]]:
    if expected_absent and path.exists() and requested:
        raise TaskValidationError(f"approved optional file appeared externally during execution: {path.name}")
    if not requested or not path.exists():
        return False, []
    revalidate_project_file(project, path, must_exist=True)
    text, newline, _, encoding = _read_markdown(path)
    resolved = []
    lines = text.splitlines(keepends=True)
    for item in requested:
        for index, line in enumerate(lines):
            ending = newline if line.endswith(newline) else ""
            body = line[:-len(ending)] if ending else line
            cells = [cell.strip() for cell in body.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[1] == item and cells[-1].lower() not in {"resolved", "closed", "complete"}:
                cells[-1] = "Resolved"
                lines[index] = "| " + " | ".join(cells) + " |" + ending
                resolved.append(item)
                break
    if resolved:
        proposed = "".join(lines)
        ensure_no_secrets(proposed, "proposed project content")
        revalidate_project_file(project, path, must_exist=True)
        _write_markdown(path, proposed, encoding, before_replace, after_replace)
    return bool(resolved), resolved


def apply_updates(
    project: Path, task: Task, on_write: Callable[[Path], None] | None = None,
    originally_absent: set[Path] | None = None,
    before_replace=None, after_replace=None,
) -> dict:
    originally_absent = originally_absent or set()
    paths = {name: project / name for name in ("PROJECT_CARD.md", "OPEN_LOOPS.md", "NOTES.md", "DRAFTS.md")}
    for path in paths.values():
        revalidate_project_file(project, path)
    changed = []
    facts = [_text(item, fact=True) for item in task.confirmed_facts]
    added = [_text(item) for item in task.open_loops_to_add]
    requested_resolutions = [_text(item) for item in task.open_loops_to_resolve]
    notes = [_text(item) for item in task.notes_to_add]
    drafts = [_text(item) for item in task.drafts_to_save]
    existing_data = [revalidate_project_file(project, path, must_exist=True).read_bytes() for path in paths.values() if path.exists() and path not in originally_absent]
    crlf_count = sum(data.count(b"\r\n") for data in existing_data)
    lf_count = sum(data.count(b"\n") - data.count(b"\r\n") for data in existing_data)
    default_newline = "\r\n" if crlf_count > lf_count else "\n"
    revalidate_project_file(project, paths["PROJECT_CARD.md"], must_exist=True)
    if _append_section(project, paths["PROJECT_CARD.md"], f"Confirmed Update - {task.task_id}", facts, default_newline, paths["PROJECT_CARD.md"] in originally_absent, before_replace, after_replace):
        changed.append(paths["PROJECT_CARD.md"])
        if on_write:
            on_write(paths["PROJECT_CARD.md"])
    revalidate_project_file(project, paths["OPEN_LOOPS.md"])
    did_resolve, resolved = _resolve_loops(project, paths["OPEN_LOOPS.md"], requested_resolutions, paths["OPEN_LOOPS.md"] in originally_absent, before_replace, after_replace)
    if did_resolve:
        changed.append(paths["OPEN_LOOPS.md"])
        if on_write:
            on_write(paths["OPEN_LOOPS.md"])
    revalidate_project_file(project, paths["OPEN_LOOPS.md"])
    if _append_section(project, paths["OPEN_LOOPS.md"], f"Added by {task.task_id}", added, default_newline, paths["OPEN_LOOPS.md"] in originally_absent, before_replace, after_replace):
        changed.append(paths["OPEN_LOOPS.md"])
        if on_write:
            on_write(paths["OPEN_LOOPS.md"])
    revalidate_project_file(project, paths["NOTES.md"])
    if _append_section(project, paths["NOTES.md"], f"Update {task.task_id}", notes, default_newline, paths["NOTES.md"] in originally_absent, before_replace, after_replace):
        changed.append(paths["NOTES.md"])
        if on_write:
            on_write(paths["NOTES.md"])
    revalidate_project_file(project, paths["DRAFTS.md"])
    if _append_section(project, paths["DRAFTS.md"], f"Saved by {task.task_id}", drafts, default_newline, paths["DRAFTS.md"] in originally_absent, before_replace, after_replace):
        changed.append(paths["DRAFTS.md"])
        if on_write:
            on_write(paths["DRAFTS.md"])
    return {
        "changed": sorted(set(changed)), "facts_added": len(facts),
        "loops_added": added, "loops_resolved": resolved,
        "unresolved_resolution_requests": [x for x in requested_resolutions if x not in resolved],
        "notes_added": len(notes), "drafts_saved": len(drafts),
    }
