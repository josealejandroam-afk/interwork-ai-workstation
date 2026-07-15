# Pending Handoffs — Drop Zone for Claude Chat

## What Goes Here

If Claude Chat has GitHub write access to this repo (a connector configured in claude.ai's
settings — confirm this is actually enabled before relying on it), it should commit new
project handoffs here instead of just displaying them for Alejandro to copy/paste.

One file per handoff. Use the naming convention:

```
memory/inbox/pending/YYYY-MM-DD_HHMM_short-topic-slug.md
```

Example: `memory/inbox/pending/2026-07-15_1030_dropbox-pm-update.md`

Use the existing structure in
`memory/inbox/claude_code_project_update_handoff_template.md` as the format — project
identity, new facts, open loops, drafts, requested repo action, safety notes.

## What Happens Next

Claude Code checks this folder (on request, or via a scheduled routine if Alejandro has set
one up) and processes each file per
`memory/company_knowledge/INBOX_PROCESSING_RULES.md`. Once a file is processed, it moves to
`memory/inbox/processed/` — files are never left in `pending/` indefinitely, and never
reprocessed once moved.

## If Chat Doesn't Have Write Access

Fall back to the current flow: display the handoff in chat, Alejandro copies it and pastes
it into a Claude Code session directly. Nothing changes for that path.
