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

To generate an isolated proposal without modifying the source repository:

```powershell
python -m local_executor examples/tasks/7556-valid.json --repo . --runtime C:\Users\1\interwork-agent-runtime --no-commit
```

Proposal mode copies the approved project files into an isolated runtime workspace, applies changes only there, and records `proposal_generated`. It verifies the source files remain byte-identical and does not consume the task ID for a later approved execution.

Use `--retry` only for an explicit retry below the task's `maximum_attempts` limit.

## Optional inbox watcher

The watcher automates execution of fully formed task files; it does not create tasks or decide which facts are confirmed. Place approved JSON tasks in:

```text
C:\Users\1\interwork-agent-runtime\inbox\pending
```

Run one cycle for review or testing:

```powershell
python -m local_executor watch --repo . --runtime C:\Users\1\interwork-agent-runtime --once
```

Without `--once`, the watcher polls continuously. It uses the dedicated `executor/auto` branch by default, creating it from local `main` when needed. A different non-main branch can be supplied with `--branch`.

Successful tasks move to `inbox\submitted`; malformed or policy-rejected tasks move to `inbox\rejected` with an adjacent error record. Files are atomically claimed in `inbox\processing` during execution. If the repository is dirty, the cycle does nothing and leaves pending files untouched.

The watcher never pushes or merges. Installing this code does not start it; continuous operation requires a separate, explicit launch and operating-system scheduling decision.

## Shared queue for multiple PCs

One designated PC may extend the watcher with the authenticated Supabase queue:

```powershell
python -m local_executor watch --repo . --runtime C:\Users\1\interwork-agent-runtime --remote
```

The worker requires these user-level environment variables:

- `SUPABASE_URL`
- `SUPABASE_PUBLISHABLE_KEY` (or the legacy `SUPABASE_ANON_KEY`)
- `INTERWORK_QUEUE_WORKER_TOKEN`

Every other PC is a submitter, not another executor. After configuring `SUPABASE_URL`, the publishable key, and a separately issued `INTERWORK_QUEUE_SUBMIT_TOKEN`, submit a fully formed task with:

```powershell
python -m local_executor submit C:\path\to\approved-task.json
```

The shared queue atomically leases one task to one worker. Submitter credentials cannot claim or complete tasks, worker credentials are stored only on the designated executor, and the database stores only token hashes. Local completed records reconcile an expired remote lease without running the same task twice.

Do not copy the worker token to secondary PCs and do not run `--remote` on more than one designated executor. Queue credentials are secrets and must stay in the Windows user environment or another operating-system credential store, never in the repository.

## Queue and project locks

The executor atomically claims a pending task as running and acquires one exclusive lock per canonical project path. Completed task IDs cannot run again. Failed tasks retain attempt history and require `--retry`.

Inspect a project lock:

```powershell
python -m local_executor inspect-lock --runtime C:\Users\1\interwork-agent-runtime --project C:\path\to\project
```

Recover a confirmed stale lock. Recovery refuses a live same-host process:

```powershell
python -m local_executor recover-lock --runtime C:\Users\1\interwork-agent-runtime --project C:\path\to\project
```

Inspect or explicitly recover an interrupted running task:

```powershell
python -m local_executor inspect-running TASK_ID --runtime C:\Users\1\interwork-agent-runtime
python -m local_executor recover-running TASK_ID --runtime C:\Users\1\interwork-agent-runtime
```

Running-task recovery refuses a live same-host process, preserves the running record in interrupted history, and requires `--force` for another host or malformed metadata.

Finalize a task whose local commit succeeded but report finalization failed:

```powershell
python -m local_executor recover-finalization TASK_ID --repo . --runtime C:\Users\1\interwork-agent-runtime
```

Reports, diffs, backups, and queue records are written under the supplied external runtime directory. A failed task restores modified project files and writes an error record.

Before every atomic project-file replacement, the executor writes a content-free SHA-256 change journal under the runtime directory. Interrupt recovery compares the actual Git HEAD with the recorded starting commit: pre-commit interruptions unstage and safely restore executor-owned changes, while post-commit interruptions preserve the clean commit and enter `committed_needs_recovery`.

## Task item formats

Facts may be strings or objects with `field` and `value`. Open loops, notes, and drafts may be strings or objects containing `item`, `text`, or `content`. Values must be explicit, single-line, and cannot be unsupported placeholders.

## Review and rollback

Review the generated report and `.diff` file before approving any push or merge. For a committed task, use the exact `git revert --no-edit <commit>` command in the completion report.

## Phase 2 recommendations

- Add signed task provenance and explicit human-approval records.
- Add semantic Markdown section adapters for more project-card layouts.
- Add optional index-rebuild proposals after the deterministic core is proven.
- Keep model integration and external writes behind separate, explicit policy gates.
