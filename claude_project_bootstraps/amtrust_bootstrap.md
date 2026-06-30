# AmTrust Financial Services — Claude Project Bootstrap
_Upload this file to the "AmTrust" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-06-30_

---

## Client

- **Name:** AmTrust Financial Services
- **Slug:** `amtrust`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

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

3. **AmTrust client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/amtrust/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug |
|---|---|
| 7348 Cleveland | `7348_cleveland` |
| 7502 Garden Grove CA | `7502_small_office_move_garden_grove` |
| 7513 Southington CT | `7513_move_office_furniture_southington` |
| 7515 New York NY | `7515_storage_disposal_new_york` |
| 7536 (location TBC) | `7536_project` |
| 7568 Irvine CA | `7568_site_walk_irvine` |
| 7572 59 Maiden Lane NYC | `7572_amtrust_financial_59_maiden_lane_new_york` |
| Las Vegas task chairs (TBD #) | `unknown_las_vegas_chairs` |
| Nashua e-waste (TBD #) | `unknown_nashua_ewaste` |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/amtrust/projects/<slug>/PROJECT_CARD.md`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` from the same folder when available.

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

Ask Alejandro to paste the specific file, or ask Claude Code for a current handoff summary.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — AmTrust [project name / location]

New confirmed facts:
- [fact 1]

Update:
memory/clients/amtrust/projects/<slug>/PROJECT_CARD.md
memory/clients/amtrust/projects/<slug>/OPEN_LOOPS.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not send emails or Teams messages — draft only, Alejandro approves all sends.
- Do not write to Supabase — propose changes, wait for approval.
- Alejandro Acosta is the sole approval authority.
- If sources conflict, flag it and ask.
