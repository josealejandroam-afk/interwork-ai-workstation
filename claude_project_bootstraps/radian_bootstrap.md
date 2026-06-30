# Radian — Claude Project Bootstrap
_Upload this file to the "Radian" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** Radian
- **Slug:** `radian`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## At the Start of Each Chat — Fetch These Files

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Radian client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/radian/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Card URL suffix |
|---|---|
| 7492 Denver Decom | `memory/clients/radian/projects/7492_radian_denver_decom/PROJECT_CARD.md` |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/<suffix>`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` from the same folder.

---

## Dashboard Rule

- Dashboard snapshot for operational status.
- Project card for scope, contacts, notes, history.
- Flag conflicts, do not pick silently.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Radian [project]

New confirmed facts:
- [fact 1]

Update:
memory/clients/radian/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not send emails or Teams messages — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
