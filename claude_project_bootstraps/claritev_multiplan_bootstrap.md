# Claritev / MultiPlan — Claude Project Bootstrap
_Upload this file to the "Claritev Projects" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-07-01_

---

## Client

- **Name:** Claritev (formerly MultiPlan)
- **Slug:** `claritev_multiplan`
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Naming Note

The company rebranded from MultiPlan to Claritev. Older project records may say "MultiPlan." File under `claritev_multiplan/` regardless of which name appears on paperwork.

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

3. **Claritev client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/claritev_multiplan/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug | Notes |
|---|---|---|
| 7420 Laguna Hills CA | `7420_parsippany` | Folder slug is a legacy name — confirmed location is Laguna Hills, CA |
| 6836 Historical | `6836_historical` | Historical record |
| 6837 Historical | `6837_historical` | Historical record |
| Chattanooga TN (# TBD) | — | Project number not confirmed |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/claritev_multiplan/projects/<slug>/PROJECT_CARD.md`

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
Claude Code Handoff — Claritev [project number / location]

New confirmed facts:
- [fact 1]

Update:
memory/clients/claritev_multiplan/projects/<slug>/PROJECT_CARD.md
memory/clients/claritev_multiplan/projects/<slug>/OPEN_LOOPS.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- File under `claritev_multiplan/` whether the paperwork says Claritev or MultiPlan.
- Folder `7420_parsippany` is a legacy slug — the confirmed location is Laguna Hills, CA.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
