import json
from pathlib import Path

from .policy_engine import ensure_no_secrets
from .runtime_guard import revalidate_runtime_path, safe_runtime_path


def write_report(runtime: Path, data: dict) -> Path:
    report_dir = safe_runtime_path(runtime, "reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    path = safe_runtime_path(runtime, "reports", f"{data['task_id']}-completion.txt")
    checks = "\n".join(f"- {name}: {result}" for name, result in data["validation"].items())
    conflicts = "\n".join(f"- {item}" for item in data["conflicts"]) or "- None detected"
    changed = "\n".join(f"- {item}" for item in data["files_changed"]) or "- None"
    reviewed = "\n".join(f"- {item}" for item in data["files_reviewed"])
    policy = data["policy_enforcement"]
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
- Action allowlist enforced: {'PASS' if policy['action_allowlisted'] else 'FAIL'}
- Internal prohibited-action denylist enforced: {'PASS' if policy['internal_prohibited_actions_enforced'] else 'FAIL'}
- External adapters registered: {'YES' if policy['external_adapters_registered'] else 'NO'}
- Prohibited command path invoked: {'YES' if policy['prohibited_command_path_invoked'] else 'NO'}

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
    serialized = json.dumps(data, indent=2) + "\n"
    ensure_no_secrets(text + serialized, "generated report")
    revalidate_runtime_path(runtime, path).write_text(text, encoding="utf-8", newline="\n")
    json_path = safe_runtime_path(runtime, "reports", f"{data['task_id']}-completion.json")
    revalidate_runtime_path(runtime, json_path).write_text(serialized, encoding="utf-8")
    return path
