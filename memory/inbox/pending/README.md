# Pending Handoffs — Drop Zone for Claude Chat

## What Goes Here

**Confirmed working path (2026-07-15):** this is the Claude Desktop app, and the **Desktop
Commander** extension is installed and enabled at the desktop-app level (Settings →
Connectors — confirmed connected, applies to Chat sessions, not just Code). Desktop Commander
can run shell commands, so Claude Chat should use `git` (via Desktop Commander's
`start_process`/`interact_with_process`) against the local clone to push handoffs straight to
GitHub — not just write a local file that might never leave the machine.

Local clone path: `C:\Users\AlejandroAcosta\Documents\ai-workstation` (same clone Claude Code
uses).

**Sequence:** `git pull` → write the file → `git add` / `git commit` / `git push`. Always
pull first — local state can be stale, and pulling first avoids push conflicts with Code.

One file per handoff, written to:

```
memory/inbox/pending/YYYY-MM-DD_HHMM_short-topic-slug.md
```

Example: `memory/inbox/pending/2026-07-15_1030_dropbox-pm-update.md`

Use the existing structure in
`memory/inbox/claude_code_project_update_handoff_template.md` as the format — project
identity, new facts, open loops, drafts, requested repo action, safety notes.

Desktop Commander's write and process-execution tools require Alejandro's one-time approval
per call (read-only tools are always-allow) — tell him what's about to be written/run before
calling the tool so the approval prompt isn't a surprise.

**Only write and push inside this `pending/` folder.** Chat should never commit directly into
`memory/clients/**` or elsewhere in the repo — Desktop Commander has general filesystem/shell
access on the machine, not access scoped to this repo, and the pending/ → review → file step
is the checkpoint that catches bad assumptions before they land as "official." Claude Code
still does the filing.

If `git push` is rejected (non-fast-forward): `git pull` and retry. Never force-push. If a
command reports uncommitted local changes or a real conflict, stop and surface it to
Alejandro — don't stash, reset, or resolve it yourself.

## What Happens Next

Claude Code checks this folder (on request, or via a scheduled routine if Alejandro has set
one up) and processes each file per
`memory/company_knowledge/INBOX_PROCESSING_RULES.md`. Once a file is processed, it moves to
`memory/inbox/processed/` — files are never left in `pending/` indefinitely, and never
reprocessed once moved.

## If Desktop Commander Isn't Available

Fall back to the current flow: display the handoff in chat, Alejandro copies it and pastes
it into a Claude Code session directly. Nothing changes for that path.
