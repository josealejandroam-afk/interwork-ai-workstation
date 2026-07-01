# Strategic Education / Strayer — Claude Project Bootstrap
_Upload this file to the "Strategic Education / Strayer Projects" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-07-01_

---

## Client

- **Name:** Strategic Education, Inc. (SEI) / Strayer University
- **Slug:** `strategic_education`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Naming Note

Strategic Education, Inc. (SEI) is the corporate parent of Strayer University. Projects may be attributed to either name — file under `strategic_education/` for both.

The client context file also references "Guardian Lower Bucks" — do not assume this is a Strategic Education project. Confirm with Alejandro whether it belongs here or is a separate engagement.

Do not conflate with the `guardian/` client folder, which is Guardian Financial Group — a different company.

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

3. **Strategic Education client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/strategic_education/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug | Notes |
|---|---|---|
| 7053 — Washington DC | `7053_project` | 901 15th St NW, DC. Active — Final Punchlist leg in progress through 2026-07-07. |
| 7337 | `7337_project` | Details need confirmation. |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/strategic_education/projects/<slug>/PROJECT_CARD.md`

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
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Strategic Education / Strayer [project]

New confirmed facts:
- [fact 1]

Update:
memory/clients/strategic_education/projects/<slug>/PROJECT_CARD.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Do not conflate with the `guardian/` client folder (Guardian Financial Group) — different company.
- "Guardian Lower Bucks" mentioned in context file: ask Alejandro before assuming it belongs here.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
