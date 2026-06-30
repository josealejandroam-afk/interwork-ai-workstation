# Dashboard Check Rules
_For Claude Chat and Claude Code — how to answer operational status questions_
_Last updated: 2026-06-30_

---

## Source Priority

| Priority | Source | Use for |
|---|---|---|
| 1 (highest) | Supabase / live dashboard | Current operational counts, status, dates |
| 2 | `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` | AI-readable snapshot when live access unavailable |
| 3 | Client knowledge pack | Client-specific project context, contacts, scope |
| 4 | Project card (`PROJECT_CARD.md`) | Richer context, manually confirmed details, open loops |

---

## Rules

### 1. Dashboard is the live operational source
The Vercel dashboard draws from Supabase in real time.
It is the authoritative source for project status, dates, readiness, PMs, and alert counts.
Repo memory does not replace it — it supplements it.

### 2. Use the dashboard snapshot for operational counts
When Claude Chat cannot directly access Supabase or the dashboard URL,
use `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` for:
- Total project count
- Today / Tomorrow / This Week counts
- At-risk and alert counts
- Flagged row details (at-risk, missing PM, stale scheduled)

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

### 6. Check snapshot freshness
The dashboard snapshot has a `Last Updated` timestamp.
If the snapshot is more than 24 hours old, warn that it may be stale.
Advise running `scripts/update_dashboard_snapshot.ps1` to refresh it.

### 7. Snapshot vs. repo memory divergence
If a project card was updated after the snapshot timestamp,
prefer the project card for that project's specific facts,
but use the snapshot for global counts (today/tomorrow/alerts).

---

## When to Use Each Source

| Question | Use |
|---|---|
| "How many projects are today?" | Dashboard snapshot |
| "What's the status of project 7552?" | Dashboard snapshot + project card |
| "Who is the PM for 7391?" | Project card (if exists), then dashboard snapshot |
| "What is the scope for Dropbox 1800 Owens?" | Project card |
| "Are there any at-risk projects?" | Dashboard snapshot |
| "Has Morgan confirmed the new date?" | Project card open loops |

---

## What Claude Chat Cannot Do

- Access the Vercel dashboard URL directly (unreliable without browser control)
- Query Supabase directly (no live credentials in chat session)
- Know about changes made after the last snapshot timestamp

These limitations are why the AI-readable snapshot exists.
See `docs/DASHBOARD_AI_ACCESS_MODEL.md` for architecture details.
