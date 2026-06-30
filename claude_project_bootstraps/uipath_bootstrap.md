# UiPath — Claude Project Bootstrap
_Upload this file to the "UiPath" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** UiPath
- **Slug:** `uipath`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## At the Start of Each Chat — Fetch These Files

0. **AI index (fast lookup):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md`

   Use this first. It points to CLIENT_ROSTER.md, PROJECT_INDEX.md, and OPEN_LOOPS_SUMMARY.md for quick navigation.

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Dashboard snapshot (operational status):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **UiPath client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/uipath/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Card URL |
|---|---|
| 7516 Dallas Service Call | `.../memory/clients/uipath/projects/7516_service_call_dallas/PROJECT_CARD.md` |
| 1450 Broadway Move Out NYC | `.../memory/clients/uipath/projects/unknown_1450_broadway_move_out/PROJECT_CARD.md` |

For each project, also fetch `OPEN_LOOPS.md` and `NOTES.md` from the same folder.

Full raw base for project files:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/uipath/projects/`

---

## Dashboard Rule

- Use the dashboard snapshot for operational counts and today/tomorrow/this week status.
- Use project cards for scope, contacts, notes, and history.
- If dashboard snapshot and project card conflict, flag the conflict — do not silently pick one.
- If the snapshot `Last Updated` timestamp is more than 1 day old, warn that it may be stale.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."

Then ask Alejandro to either:
- Paste the specific file (e.g., "Paste the 1450 Broadway PROJECT_CARD.md")
- Or ask Claude Code to provide a current handoff summary

Do not guess from old chat memory. Do not use stale pack data as if it were current.

---

## Claude Code Handoff Format

When new durable facts appear in this chat (confirmed dates, scope, contacts, status):

```
Claude Code Handoff — UiPath [project name]

New confirmed facts:
- [fact 1]
- [fact 2]

Update:
memory/clients/uipath/projects/<folder>/PROJECT_CARD.md
memory/clients/uipath/projects/<folder>/OPEN_LOOPS.md
```

Claude Chat drafts the handoff. Claude Code executes, commits, and pushes.

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not send emails or Teams messages — draft only, Alejandro approves all sends.
- Do not write to Supabase — propose changes, wait for Alejandro approval.
- Alejandro Acosta is the sole approval authority for all sends and writes.
- If sources conflict, flag it and ask.
