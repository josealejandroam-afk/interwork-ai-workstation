# Marsh McLennan (MMC / MMA) — Claude Project Bootstrap
_Upload this file to the "Marsh McLennan" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** Marsh McLennan (MMC / MMA / Marsh)
- **Slug:** `marsh_mclennan`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Naming Note

MMC, MMA, Marsh, Marsh McLennan Agency, MM Tech, Global Security are all the same client family, filed together. Use the exact entity name on the paperwork.

---

## At the Start of Each Chat — Fetch These Files

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **MMC client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/marsh_mclennan/CLIENT_CONTEXT.md`

---

## Project Lookup

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/marsh_mclennan/projects/<slug>/PROJECT_CARD.md`

When Alejandro gives a project number, city, or scope clue, look up the matching slug from the client context file and fetch it. Also fetch `OPEN_LOOPS.md` and `NOTES.md`.

---

## Dashboard Rule

- Dashboard snapshot wins for current operational status.
- Project cards win for scope, contacts, notes, and history.
- If they conflict, flag it.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific project card, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — MMC/MMA [project number / location]

New confirmed facts:
- [fact 1]

Update:
memory/clients/marsh_mclennan/projects/<slug>/PROJECT_CARD.md
memory/clients/marsh_mclennan/projects/<slug>/OPEN_LOOPS.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Use the exact entity name on paperwork — do not auto-convert MMA to MMC.
- Do not send emails or Teams messages — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
