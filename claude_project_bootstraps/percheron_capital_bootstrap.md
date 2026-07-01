# Percheron Capital / Facilitate — Claude Project Bootstrap
_Upload this file to the "Percheron Capital / Facilitate Projects" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-07-01_

---

## Client

- **Name:** Percheron Capital / Facilitate
- **Slug:** `percheron_capital`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Client Note

"Facilitate" appears in project records alongside Percheron Capital. The exact relationship between the two entities is not confirmed in file — file all projects under `percheron_capital/` until Alejandro clarifies.

---

## At the Start of Each Chat — Fetch These Files

0. **AI index (fast lookup):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md`

   Use this first. It points to CLIENT_ROSTER.md, PROJECT_INDEX.md, and OPEN_LOOPS_SUMMARY.md for quick navigation.

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Live dashboard API (operational status — use this first):**
   `https://interwork-command-center.vercel.app/api/ai/dashboard-summary`

   Returns live counts and today/tomorrow/at-risk rows from Supabase. No auth needed. Confirmed live 2026-06-30.
   Fallback if unavailable: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Percheron Capital client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/percheron_capital/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug | Notes |
|---|---|---|
| 7581 — Site Walk, Presidio SF | `7581_project` | One Letterman Drive, Bldg C, SF CA 94129. Site walk done 2026-06-30. PM: Frank Barrett. Client POC: Shaelyn Hesch (415) 425-7611. |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/percheron_capital/projects/<slug>/PROJECT_CARD.md`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` from the same folder when available.

**Future move note:** An anticipated furniture relocation on ~2026-08-24 (same Presidio campus) will be assigned a **separate project number**. Do NOT extend project 7581 to cover the August move — 7581 was the site walk only.

---

## Dashboard Rule

- For live counts (today/tomorrow/this week/at-risk), call `GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary`.
- For quick project, client, location, PM, or scope lookup, call `GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>` — use search before scanning repo folders.
- Use project cards for scope, contacts, notes, history, and manually confirmed facts.
- If live API and project card conflict, flag the conflict — do not silently pick one.
- Knowledge packs and dashboard snapshots are fallback only.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Percheron Capital / Facilitate [project]

New confirmed facts:
- [fact 1]

Update:
memory/clients/percheron_capital/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- The anticipated August 2026 move is a future project with its own number — do not extend 7581.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
