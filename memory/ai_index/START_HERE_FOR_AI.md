# Start Here for AI — InterWork AI Memory Layer
_Last updated: 2026-07-01 — registered /api/ai/project and /api/ai/open-loops_

---

## What This Repo Is

This is the **durable AI memory layer** for InterWork Office Solutions.

It holds project cards, client context, open loops, operating rules, and procedures.
It is committed to GitHub so every AI session can read the same facts.

This is **not** the live dashboard. The dashboard lives in Supabase / Vercel.
The dashboard snapshot in this repo is a point-in-time copy and may be stale.

---

## How to Navigate This Repo

Use the files in this `memory/ai_index/` folder as fast lookup before going deeper.

| File | What it answers |
|---|---|
| `CLIENT_ROSTER.md` | What clients exist? What are their slugs? Which has a bootstrap or pack? |
| `PROJECT_INDEX.md` | What projects exist? Where is the project card? |
| `OPEN_LOOPS_SUMMARY.md` | What is currently pending across clients and projects? |
| `DASHBOARD_STATUS.md` | What does the dashboard show right now (snapshot)? |

---

## Lookup Flow

```
START_HERE_FOR_AI.md
        ↓
Know the exact project number? GET /api/ai/project?number=<project_number>
  → exact match, single record
Otherwise search: GET /api/ai/search?q=<project number, client name, location, or scope term>
  → returns live project rows; identify records before scanning repo folders
        ↓
Check live open loops: GET /api/ai/open-loops?project_number=<project_number>
  → Supabase-tracked pending items (may be empty — check the project's OPEN_LOOPS.md too)
        ↓
(for deeper context)
CLIENT_ROSTER.md → find client slug
        ↓
PROJECT_INDEX.md → find project slug + source path
        ↓
Fetch: memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md
       memory/clients/<client_slug>/projects/<project_slug>/OPEN_LOOPS.md
       memory/clients/<client_slug>/projects/<project_slug>/NOTES.md
```

---

## Raw GitHub URL Base

All files can be fetched via raw GitHub URL:

```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/<path>
```

Example — this file:
```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md
```

Example — a project card:
```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/uipath/projects/unknown_1450_broadway_move_out/PROJECT_CARD.md
```

---

## Live AI API Endpoints

**For current operational status and quick lookup — no auth required:**

**Dashboard summary** (counts + today/tomorrow/at-risk rows):
```
GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary
```
Returns: live counts (`all`, `active`, `today`, `tomorrow`, `this_week`, `alerts`, `at_risk`), `today_rows`, `tomorrow_rows`, `at_risk_rows` — pulled live from Supabase `v_project_card`.
Confirmed live: 2026-06-30. `confidence: "live"`. No secrets exposed.

**Search** (project/client/location/PM/scope lookup, max 25 results):
```
GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>
```
Returns: matching project rows from Supabase. Searches project number, client, location, type, status, readiness, PM, and scope. Use this before scanning repo folders.
Confirmed live: 2026-06-30. Minimum 2 characters. Examples: `?q=UiPath`, `?q=7553`, `?q=Dallas`.

**Project lookup** (exact match by project number — more reliable than search when you already have the number):
```
GET https://interwork-command-center.vercel.app/api/ai/project?number=<project_number>
```
Returns: a single project record from Supabase `v_project_card` (same safe fields as dashboard-summary/search — no internal_notes, emails, or phone numbers). `404` if the project number doesn't exist; `400` if `number` is missing.
Confirmed live: 2026-07-01. Example: `?number=7492`.

**Open loops** (global or project-scoped pending items):
```
GET https://interwork-command-center.vercel.app/api/ai/open-loops?project_number=<project_number>
```
Also supports `?status=open|resolved|snoozed` and `?priority=high|medium|low` filters (combine with `project_number` or use alone).
Returns: rows from the safe view `v_open_loops_ai` — `id`, `project_number`, `title`, `status`, `priority`, `source`, `ai_generated`, `created_at`, `updated_at`, `resolved_at`. No `detail`, `external_ref`, or raw `project_id` — those never leave Supabase through this endpoint. An empty `open_loops: []` array is normal, not an error — most projects have zero open loops in Supabase right now; check the project card's `OPEN_LOOPS.md` for durable historical context Supabase doesn't carry.
Confirmed live: 2026-07-01.

---

## Source Priority

When multiple sources disagree, use this order:

1. **Live project/search APIs** — `GET /api/ai/project?number=<n>` (exact) or `GET /api/ai/search?q=<term>` (loose) — live Supabase read; use for quick project/client lookup
2. **Live dashboard API** — `GET /api/ai/dashboard-summary` — live Supabase read; use for counts and operational status
3. **Live open-loops API** — `GET /api/ai/open-loops?project_number=<n>` — live Supabase read; structured pending items, may be empty
4. **Dashboard snapshot** (`memory/ai_index/DASHBOARD_STATUS.md`) — fallback if API unavailable; stale if >1 day old
5. **Project card** (`memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md`) — best source for scope, contacts, notes, history
6. **Project's OPEN_LOOPS.md** — durable historical open items Supabase doesn't carry (older loops, closed-loop history)
7. **Client knowledge pack** (`claude_project_packs/`) — use for contacts/routing; stale for status/dates
8. **Bootstrap file** (`claude_project_bootstraps/<slug>_bootstrap.md`) — routing only, not project facts

If API/dashboard and project card conflict → **flag the conflict**, do not silently pick one.

---

## What Claude Chat Can Do From This Repo

- Call `GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary` for live operational counts and rows
- Call `GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>` for quick project/client lookup before scanning repo folders
- Call `GET https://interwork-command-center.vercel.app/api/ai/project?number=<project_number>` for an exact single-project record
- Call `GET https://interwork-command-center.vercel.app/api/ai/open-loops?project_number=<project_number>` for live Supabase-tracked open loops (check the project's `OPEN_LOOPS.md` too — Supabase's open-loop table is newer and may not have full history yet)
- Answer questions about project scope, contacts, schedule, location
- Draft client-facing emails and Teams messages (do not send without approval)
- Identify open loops and what needs resolution
- Propose a Claude Code handoff when repo updates are needed

## What Claude Chat Cannot Do

- Send emails or Teams messages without Alejandro saying "send it"
- Write to Supabase without approval
- Invent project numbers, dates, contacts, or statuses
- Push changes to the repo (that is Claude Code's job)

---

## How to Trigger a Repo Update

Draft a handoff in this format and tell Claude Code to execute:

```
Claude Code Handoff — <Client> [Project]

New confirmed facts:
- [fact 1]
- [fact 2]

Update:
memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md
```

---

## Key Company Context Files

| File | URL suffix |
|---|---|
| START_HERE (company rules) | `memory/company_knowledge/START_HERE.md` |
| Communication rules | `memory/company_knowledge/COMMUNICATION_RULES.md` |
| Access and safety rules | `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md` |
| Repo lookup rules | `memory/company_knowledge/REPO_LOOKUP_RULES.md` |

---

## Sole Approval Authority

**Alejandro Acosta** is the only person who can approve:
- Sending emails or Teams messages
- Writing to Supabase
- Deploying code to Vercel
- Any action that affects shared systems outside this repo

_When in doubt, draft and wait for "send it" or "approve"._
