# Claude Project Bootstrap Model
_How Claude Chat connects to live project knowledge_
_Last updated: 2026-06-30_

---

## The Problem With Full Knowledge Packs

A full knowledge pack (e.g., `uipath_knowledge_pack.md`) embeds changing facts — project dates, status, open loops, contacts — directly into the uploaded file. Every time anything changes:

```
Project changes → repo updates → pack regeneration → manual upload → Claude Chat re-reads pack
```

This creates maintenance drag and risks Claude Chat acting on stale data.

---

## The Better Architecture

```
Bootstrap (uploaded once, stable)     →  tells Claude Chat how to navigate
GitHub repo (updated by Claude Code)  →  holds all changing facts
Dashboard snapshot (in repo)          →  live operational status bridge
Claude Chat                           →  reads current repo files on demand
```

```
Project changes → Claude Code updates repo → Claude Chat fetches current files
```

No re-upload needed when facts change.

---

## Role of Each Layer

| Layer | What it contains | Who updates it | How often uploaded |
|---|---|---|---|
| Claude Project bootstrap | Routing instructions, URL patterns, rules | Claude Code (rare) | Once, or when routing changes |
| GitHub repo memory | Project cards, open loops, notes, contacts | Claude Code | Every session |
| Dashboard snapshot | Operational counts, today rows, at-risk | Claude Code (script) | As needed |
| Claude Project knowledge pack | Full snapshot fallback | Claude Code | Fallback only |

---

## What a Bootstrap Contains

A bootstrap is a stable instruction file, not a data file. It should include:

- Client name and slug
- Public repo URL
- Raw GitHub URL patterns
- Which files to fetch at session start
- How to look up project cards
- What to do when URL fetch is unavailable
- How to create a Claude Code handoff
- Rules: do not guess, do not scan unrelated clients

A bootstrap must NOT include:
- Project dates or statuses
- Open loops
- Contact phone numbers or emails
- Dashboard counts
- Any field that changes more than once a month

---

## URL Fetch Fallback

Not all Claude Chat sessions can fetch raw GitHub URLs (depends on the model and project configuration).

When URL fetch is unavailable, the bootstrap instructs Claude Chat to:
1. Say clearly: "I cannot access the repo directly in this chat."
2. Ask Alejandro to paste the specific file.
3. Or ask Claude Code to provide a current handoff summary.
4. Never guess from old chat memory.

---

## Claude Code Handoff Format

When Claude Chat has new durable facts (client emails, confirmed dates, scope changes):

```
Claude Code Handoff — [Client] [Project]

New confirmed facts:
- [fact 1]
- [fact 2]

Update:
memory/clients/<slug>/projects/<project_folder>/PROJECT_CARD.md
memory/clients/<slug>/projects/<project_folder>/OPEN_LOOPS.md
```

Claude Chat creates the handoff. Claude Code (this workstation) executes it.

---

## Knowledge Packs — Fallback Only

Files in `claude_project_packs/` remain available as a fallback for sessions where URL fetch is unavailable.

Packs are not the primary source of truth. They may be stale.
The repo is always more current than any uploaded pack.

When using a pack as fallback:
- Check the `Generated:` date at the top
- If it is more than a few days old, treat project-specific facts as stale
- Use the pack for contacts and routing patterns only

---

## Related Files

| File | Purpose |
|---|---|
| `claude_project_bootstraps/` | One bootstrap per active client |
| `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` | Live dashboard snapshot |
| `memory/dashboard/DASHBOARD_CHECK_RULES.md` | How to reconcile sources |
| `memory/inbox/client_chat_start_prompt.md` | General session start prompt |
| `claude_project_packs/` | Fallback packs (not primary) |
