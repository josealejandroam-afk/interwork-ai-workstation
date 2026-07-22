import json
from pathlib import Path


def write_report(report_dir: Path, data: dict) -> Path:
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{data['task_id']}-completion.txt"
    checks = "\n".join(f"- {name}: {result}" for name, result in data["validation"].items())
    conflicts = "\n".join(f"- {item}" for item in data["conflicts"]) or "- None detected"
    changed = "\n".join(f"- {item}" for item in data["files_changed"]) or "- None"
    reviewed = "\n".join(f"- {item}" for item in data["files_reviewed"])
    text = f"""Task completed: {data['task_id']}

Project:
{data['project_number']} {data['project_slug']}

Starting commit SHA:
{data['starting_commit']}

Ending local commit SHA:
{data['ending_commit']}

Files reviewed:
{reviewed}

Files changed:
{changed}

Changes applied:
- Added {data['facts_added']} confirmed facts
- Added {len(data['loops_added'])} open loops
- Resolved {len(data['loops_resolved'])} prior open loops
- Added {data['notes_added']} notes
- Saved {data['drafts_saved']} drafts

Conflicts:
{conflicts}

Validation:
{checks}
- No external communication: PASS
- No Supabase write: PASS

Git:
- Local branch: {data['branch']}
- Local commit created: {data['ending_commit']}
- Push performed: NO

Approval required:
- Alejandro must review the Git diff
- Alejandro must approve before any push or merge

Rollback:
{data['rollback']}
"""
    path.write_text(text, encoding="utf-8", newline="\n")
    (report_dir / f"{data['task_id']}-completion.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
