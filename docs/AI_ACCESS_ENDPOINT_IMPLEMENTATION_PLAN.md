# AI Access Endpoint Implementation Plan
_Created: 2026-06-30_
_Status: Phase 1 complete (static index), Phase 2 planned (Vercel API)_

---

## Purpose

Define the architecture and implementation path for AI-readable access to InterWork operational data.

Any AI chat (Claude Chat, ChatGPT, future AI) should be able to access current project facts through stable, consistent URLs — without uploading changing knowledge packs.

---

## Current State (as of 2026-06-30)

| Capability | Status | Path |
|---|---|---|
| Static AI index (raw GitHub) | **Live** | `memory/ai_index/` |
| Dashboard snapshot (raw GitHub) | **Live** | `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` |
| Client context (raw GitHub) | **Live** | `memory/clients/<slug>/CLIENT_CONTEXT.md` |
| Project cards (raw GitHub) | **Live** | `memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md` |
| Bootstrap routing files | **Live** | `claude_project_bootstraps/<slug>_bootstrap.md` |
| Vercel AI API endpoints | **Planned — not yet built** | `interwork-command-center` repo |

---

## Phase 1 — Static AI Index (this repo, complete)

### What was built

Five AI-readable index files in `memory/ai_index/`:

| File | Purpose |
|---|---|
| `START_HERE_FOR_AI.md` | Navigation guide — lookup flow, source priority, rules |
| `CLIENT_ROSTER.md` | All clients, slugs, project counts, bootstrap/pack pointers |
| `PROJECT_INDEX.md` | All known projects with source paths to PROJECT_CARD.md |
| `OPEN_LOOPS_SUMMARY.md` | Cross-client open items and pending decisions |
| `DASHBOARD_STATUS.md` | Dashboard snapshot mirror with staleness warning |

### How it works

Any AI fetches via raw GitHub URL:
```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md
```

The lookup flow:
```
START_HERE_FOR_AI → CLIENT_ROSTER → PROJECT_INDEX → PROJECT_CARD.md
```

### Limitations

- Not live. Requires manual or scripted regeneration after repo changes.
- `update_ai_index.ps1` regenerates from repo data and dashboard snapshot.
- Stale within hours if projects change without index regeneration.

---

## Phase 2 — Vercel AI API (planned, not yet built)

### Where to build

The `interwork-command-center` Vercel app — a separate repo from this one.
**Do not add API routes to this repo (`interwork-ai-workstation`)** — it has no Next.js app.

### Proposed Endpoints

#### `GET /api/ai/dashboard-summary`

**Data source:** Supabase (live read)

```json
{
  "updated_at": "2026-06-30T18:00:00Z",
  "counts": {
    "all": 140,
    "alerts": 47,
    "at_risk": 46,
    "today": 4,
    "tomorrow": 3,
    "this_week": 9
  },
  "today_rows": [
    {
      "project_number": 7053,
      "client": "StratEdu",
      "location": "901 15th St NW, Washington DC",
      "type": "Relocation",
      "time": "9:00 AM",
      "status": "Scheduled",
      "readiness": "Ready"
    }
  ]
}
```

**Security:** Read-only Supabase query. No auth required if data is non-sensitive. Consider IP allowlist or bearer token if needed.

---

#### `GET /api/ai/client/[client_slug]`

**Data source:** GitHub raw files (this repo)

Returns:
- `CLIENT_CONTEXT.md` content
- List of known project slugs
- Link to each project endpoint

---

#### `GET /api/ai/project/[client_slug]/[project_slug]`

**Data source:** GitHub raw files (this repo)

Returns:
- `PROJECT_CARD.md` content
- `OPEN_LOOPS.md` content
- `NOTES.md` content (if exists)

**Note:** `DRAFTS.md` should be omitted unless explicitly included — drafts may contain client-facing content not ready to share.

---

#### `GET /api/ai/search?q=`

**Data source:** GitHub repo file index or Supabase full-text search

Returns: matching clients, projects, files.

**Phase 2b — lower priority.** Start with dashboard-summary and project endpoint first.

---

#### `GET /api/ai/open-loops`

**Data source:** This repo (OPEN_LOOPS_SUMMARY.md or Supabase `open_loops` table)

Returns: global cross-client open loops.

---

### Security Assumptions

| Assumption | Notes |
|---|---|
| All endpoints are read-only | No writes in this phase |
| Supabase access uses read-only service role or anon key with RLS | Never expose write credentials |
| No client PII in responses | Project locations and contacts are not PII under normal B2B context |
| Endpoint URLs are not secret | Any AI or person can query them |
| Secrets (env vars, tokens) never appear in response body | Validated at code review |

---

### What to NOT Include in API Responses

- Raw email content (screenshots, message bodies)
- Credentials, tokens, API keys
- Internal notes marked as "do not share"
- Personal contact information beyond what is already in project cards

---

### How Claude Chat Uses These Endpoints

At the start of a session:
1. Fetch `/api/ai/dashboard-summary` for operational status
2. Fetch `/api/ai/client/<slug>` for client context
3. Fetch `/api/ai/project/<slug>/<project_slug>` for the relevant project
4. Flag stale data; ask for live refresh if needed

---

### How ChatGPT Uses These Endpoints

Same pattern. Both Claude Chat and ChatGPT can use these as read-only data sources from any session.

---

### How Claude Code Updates Memory

Claude Code continues to edit repo files directly. The API endpoints serve the current state of the repo. Updates flow:

```
Claude Code edits PROJECT_CARD.md → commit + push → API serves updated card
```

No sync script needed — GitHub raw URLs always reflect the latest commit.

---

## Phase 3 — Controlled Write API (future)

Not designed yet. Requires:
- Explicit approval from Alejandro
- Audit log for every write
- Clear approval gate before any data change

Possible future endpoints:
- `POST /api/ai/project/<slug>/status` — update project status with approval token
- `POST /api/ai/open-loops/<id>/resolve` — mark loop resolved

---

## Recommended Build Order

1. `GET /api/ai/dashboard-summary` — highest value, live Supabase read
2. `GET /api/ai/project/[client_slug]/[project_slug]` — most frequent use case
3. `GET /api/ai/client/[client_slug]` — client context
4. `GET /api/ai/open-loops` — global pending items
5. `GET /api/ai/search?q=` — nice-to-have, build last

---

## Next Step

Open the `interwork-command-center` repo in a new Claude Code session and build Phase 2.

```
Claude Code Handoff — interwork-command-center

Goal: Add read-only AI access API routes.

Do not deploy until Alejandro approves.
Do not expose secrets.
Do not add write endpoints in this phase.

Reference: docs/AI_ACCESS_ENDPOINT_IMPLEMENTATION_PLAN.md in interwork-ai-workstation repo.
```
