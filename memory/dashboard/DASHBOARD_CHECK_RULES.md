# Dashboard Check Rules
_For Claude Chat and Claude Code — how to answer operational status questions_
_Last updated: 2026-06-30_

---

## Live AI API Endpoints

**Dashboard summary** (counts + today/tomorrow/at-risk rows):
```
GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary
```
Live Supabase read. No auth required. Confirmed live: 2026-06-30.

**Search** (project/client/location/PM/scope lookup):
```
GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>
```
Live Supabase read. No auth required. Minimum 2 characters. Max 25 results. Confirmed live: 2026-06-30.
Use search before scanning repo folders for any project or client lookup.

---

## Source Priority

| Priority | Source | Use for |
|---|---|---|
| 1 (highest) | **Live search API** (`/api/ai/search?q=<term>`) | Quick project/client/location/PM lookup — live Supabase |
| 2 | **Live dashboard API** (`/api/ai/dashboard-summary`) | Operational counts, today/tomorrow/at-risk rows — live Supabase |
| 3 | `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` | AI-readable snapshot — fallback only when API unavailable |
| 4 | Project card (`PROJECT_CARD.md`) | Richer context, manually confirmed details, open loops |
| 5 | Client knowledge pack | Client-specific project context, contacts, scope |

---

## Rules

### 1. Use the live AI API for operational status
Call `GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary` for:
- Total project count
- Today / Tomorrow / This Week counts
- At-risk and alert counts
- Today's rows, tomorrow's rows, at-risk rows with readiness labels

This endpoint reads Supabase live. No auth required. Available to any AI that can make HTTP requests.
Confirmed live: 2026-06-30.

### 2. Use the dashboard snapshot only as fallback
Use `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` only when the API above is unavailable.
It is a manual snapshot and may be stale. Always note its `Last Updated` timestamp.

### 3. Use client/project cards for project context
Client knowledge packs and project cards contain:
- Scope details
- Contact names and roles
- Open loops
- Manually confirmed facts
- Historical notes

These may be richer or more current than what Supabase has for a specific project.

### 4. Conflict handling
If the dashboard snapshot contradicts a project card:
- Flag the conflict explicitly — do not silently pick one.
- Ask Alejandro which source to trust.
- Dashboard/Supabase usually wins for current operational status.
- Project card may win if it contains a manually confirmed update not yet in Supabase.

### 5. Never guess
Do not invent or assume:
- Missing execution dates
- PM names
- Project status
- Readiness flags
- Scope details

If a field is missing, say it is missing and flag it as an open loop.

### 6. Check snapshot freshness (fallback only)
The dashboard snapshot has a `Last Updated` timestamp.
If the snapshot is more than 24 hours old, warn that it may be stale.
Prefer the live API (`/api/ai/dashboard-summary`) over the snapshot whenever possible.
If the API is unavailable and the snapshot is stale, advise running `scripts/update_dashboard_snapshot.ps1`.

### 7. Snapshot vs. repo memory divergence
If a project card was updated after the snapshot timestamp,
prefer the project card for that project's specific facts,
but use the snapshot for global counts (today/tomorrow/alerts).

### 8. Use search for quick project/client lookup
Before scanning repo folders, call:
```
GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>
```
Search returns live Supabase data (max 25 rows). It matches against project number, client, location, type, status, readiness, PM name, and scope summary. Use the result to identify records, then fetch the matching project card for deeper context. Search = live quick scan. Project card = durable detailed context.

---

## When to Use Each Source

| Question | Use |
|---|---|
| "How many projects are today?" | Live dashboard API (`/api/ai/dashboard-summary`) |
| "What's the status of project 7552?" | Live search API (`/api/ai/search?q=7552`) + project card |
| "Who is the PM for 7391?" | Live search API (`/api/ai/search?q=7391`), then project card |
| "What is the scope for Dropbox 1800 Owens?" | Project card |
| "Are there any at-risk projects?" | Live dashboard API (`/api/ai/dashboard-summary`) |
| "Has Morgan confirmed the new date?" | Project card open loops |
| "Find all projects in Dallas" | Live search API (`/api/ai/search?q=Dallas`) |

---

## What Claude Chat Can Do (as of 2026-06-30)

- Call `GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary` for live operational counts and rows
- Call `GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>` for quick live project/client/location lookup
- Fetch project cards, open loops, and client context via raw GitHub URLs
- Draft emails and Teams messages (Alejandro approves all sends)

## What Claude Chat Cannot Do

- Access the Vercel dashboard UI directly (browser-based, not AI-accessible)
- Query Supabase directly (no live credentials in chat session)
- Know about changes made to Supabase after the API response was received (point-in-time)
- Push changes to the repo (Claude Code only)

See `docs/HANDS_EYES_EARS_MODEL.md` for the full capability model.
