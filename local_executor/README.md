# Local Executor MVP

This standard-library Python tool applies explicitly supplied JSON updates to one approved project-memory folder. It validates the task and path, creates external backups, edits only `PROJECT_CARD.md`, `OPEN_LOOPS.md`, `NOTES.md`, and `DRAFTS.md`, validates the diff, writes a report and diff outside the repository, and optionally creates a local commit.

It never pushes, merges, writes to Supabase or Smartsheet, sends communications, deletes files, installs packages, or changes credentials.

## Requirements

- Python 3.11 or newer
- Git
- A clean repository on a non-main branch

## Run

From the repository root on Windows:

```powershell
python -m local_executor examples/tasks/7556-valid.json --repo . --runtime C:\Users\1\interwork-agent-runtime
```

To validate and report without committing:

```powershell
python -m local_executor examples/tasks/7556-valid.json --repo . --runtime C:\Users\1\interwork-agent-runtime --no-commit
```

Reports, diffs, backups, and queue records are written under the supplied external runtime directory. A failed task restores modified project files and writes an error record.

## Task item formats

Facts may be strings or objects with `field` and `value`. Open loops, notes, and drafts may be strings or objects containing `item`, `text`, or `content`. Values must be explicit, single-line, and cannot be unsupported placeholders.

## Review and rollback

Review the generated report and `.diff` file before approving any push or merge. For a committed task, use the exact `git revert --no-edit <commit>` command in the completion report.

## Phase 2 recommendations

- Add signed task provenance and explicit human-approval records.
- Add a lock to prevent concurrent tasks for the same project.
- Add semantic Markdown section adapters for more project-card layouts.
- Add optional index-rebuild proposals after the deterministic core is proven.
- Keep model integration and external writes behind separate, explicit policy gates.
