# Tegna / Premion — Claude Project Bootstrap
_Upload this file to the "Tegna" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** Tegna / Premion
- **Slug:** `tegna_premion`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## At the Start of Each Chat — Fetch These Files

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Tegna client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/tegna_premion/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

No confirmed project number on file. When Alejandro provides a project number or clue:
- Search `memory/clients/tegna_premion/projects/`
- Fetch the matching PROJECT_CARD.md

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/tegna_premion/projects/<slug>/PROJECT_CARD.md`

---

## Dashboard Rule

- Dashboard snapshot for operational status.
- Project cards for scope, contacts, notes, history.
- If no project card exists, say so — do not guess.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Tegna [project]

New confirmed facts:
- [fact 1]

Update or create:
memory/clients/tegna_premion/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
