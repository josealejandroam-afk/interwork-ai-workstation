# Dropbox — Claude Project Bootstrap
_Upload this file to the "Dropbox" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** Dropbox
- **Slug:** `dropbox`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Address Overlap Note

Dropbox's former HQ at 1800 Owens St, San Francisco also appears in Pear VC project 7510. These are separate projects. Do not conflate them.

---

## At the Start of Each Chat — Fetch These Files

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Dropbox client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/dropbox/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug |
|---|---|
| 7399 | `7399_project` |
| 7460 | `7460_project` |
| 7467 Seattle Studio Move | `7467_seattle_studio_move` |
| 7552 SF Relocation | `7552_project` |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/dropbox/projects/<slug>/PROJECT_CARD.md`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` from the same folder when available.

---

## Dashboard Rule

- Dashboard snapshot for operational status.
- Project cards for scope, contacts, notes, history.
- Flag conflicts.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Dropbox [project]

New confirmed facts:
- [fact 1]

Update:
memory/clients/dropbox/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not conflate Dropbox and Pear VC projects even if the address overlaps.
- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
