# Rothman Orthopaedics — Claude Project Bootstrap
_Upload this file to the "Rothman Orthopaedics" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** Rothman Orthopaedics
- **Slug:** `rothman_orthopaedics`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## At the Start of Each Chat — Fetch These Files

0. **AI index (fast lookup):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md`

   Use this first. It points to CLIENT_ROSTER.md, PROJECT_INDEX.md, and OPEN_LOOPS_SUMMARY.md for quick navigation.

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Rothman client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/rothman_orthopaedics/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug |
|---|---|
| 7440 Wayne PA | `7440_wayne_pa` |
| 7583 Philadelphia Service Call | `7583_service_call_philadelphia` |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/rothman_orthopaedics/projects/<slug>/PROJECT_CARD.md`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` when available.

Note: Project 7572 was previously misfiled under Rothman — it is an AmTrust project (59 Maiden Lane NYC). Do not look for 7572 here.

---

## Dashboard Rule

- Dashboard snapshot for operational status.
- Project cards for scope, contacts, notes, history.
- Flag conflicts, do not pick silently.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Rothman Orthopaedics [project]

New confirmed facts:
- [fact 1]

Update:
memory/clients/rothman_orthopaedics/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Project 7572 is NOT a Rothman project — it belongs to amtrust/.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
