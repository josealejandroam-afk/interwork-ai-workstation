# Dashboard AI Access Model
_How Claude Chat reads InterWork dashboard state without live browser or URL access_
_Last updated: 2026-06-30_

---

## Problem

Claude Chat cannot reliably inspect the live dashboard UI.
- The Vercel dashboard URL requires browser rendering and authentication.
- Claude Chat cannot hold a browser session or follow redirects with auth cookies.
- Even if Claude Chat could fetch the URL, it would receive raw HTML — not structured data.

Claude Chat also cannot query Supabase directly.
- Supabase credentials are never passed into Claude Chat sessions.
- Passing credentials through chat is a security anti-pattern.

---

## Solution: AI-Readable Dashboard Snapshot

Claude Code (this workstation) can query Supabase read-only and write a structured markdown file.
Claude Chat reads that file via the GitHub repo or uploaded knowledge pack.

```
Supabase (live data)
      │
      ▼
Claude Code runs update_dashboard_snapshot.ps1
      │
      ▼
memory/dashboard/CURRENT_DASHBOARD_STATUS.md  (committed to GitHub)
      │
      ├──▶ Claude Chat reads via raw GitHub URL
      └──▶ Claude Chat reads via uploaded client knowledge pack
```

---

## Roles

| Actor | Role |
|---|---|
| **Supabase** | Live operational source of truth. All project data lives here. |
| **Vercel dashboard** | Human-readable visual view. Draws from Supabase in real time. |
| **GitHub repo** | AI memory source of truth. Stores snapshot, project cards, open loops, context. |
| **Claude Code** | Updates the snapshot. Reads Supabase. Writes markdown. Commits and pushes. |
| **Claude Chat** | Reads the snapshot. Answers operational questions. Cannot write to Supabase. |

---

## Update Flow

1. Alejandro runs `.\scripts\update_dashboard_snapshot.ps1` (or asks Claude Code to run it).
2. Script queries Supabase read-only using env vars on the local machine.
3. Script writes structured markdown to `memory/dashboard/CURRENT_DASHBOARD_STATUS.md`.
4. Claude Code commits and pushes the snapshot.
5. Claude Chat reads the snapshot on next session load or when the file is re-uploaded.

---

## Staleness

The snapshot has a `Last Updated` timestamp.
Claude Chat must check this timestamp before answering operational questions.

| Snapshot age | Claude Chat behavior |
|---|---|
| < 24 hours | Use snapshot counts and rows with normal confidence |
| 1–3 days | Use snapshot but warn: "this snapshot is N days old and may be stale" |
| > 3 days | Warn strongly; advise refreshing before making any decisions |

---

## What Claude Chat Can Answer from the Snapshot

- Total active project count
- Today / Tomorrow / This Week counts
- At-risk count and alert count
- Row-level detail for today's projects (when captured)
- At-risk row detail (when captured by live refresh)
- Missing PM list (when captured by live refresh)

## What Claude Chat Cannot Answer from the Snapshot

- Live real-time changes (e.g. a project just completed 10 minutes ago)
- Data for filters not captured in the last refresh
- Anything requiring a live database query

---

## Future Optional Improvement (Not Yet Implemented)

A read-only Vercel API endpoint could serve fresh JSON directly:

```
GET /api/ai-dashboard-summary
```

Proposed response shape:
```json
{
  "updated_at": "2026-06-30T14:00:00Z",
  "counts": {
    "all": 140,
    "alerts": 47,
    "at_risk": 46,
    "today": 4,
    "tomorrow": 3,
    "this_week": 9
  },
  "today": [...],
  "tomorrow": [...],
  "this_week": [...],
  "at_risk": [...],
  "missing_pm": [...],
  "stale_scheduled": [...]
}
```

**Do not implement this endpoint until explicitly approved by Alejandro.**
It would require auth design, rate limiting, and Vercel deployment review.

**Superseded by:** [`CONTROLLED_DASHBOARD_UPDATES.md`](CONTROLLED_DASHBOARD_UPDATES.md) for anything write-related — any future AI-driven dashboard change should go through the proposal/approval queue design there, not a direct write endpoint.

---

## Related Files

| File | Purpose |
|---|---|
| `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` | The snapshot itself |
| `memory/dashboard/DASHBOARD_CHECK_RULES.md` | Rules for how Claude Chat uses the snapshot |
| `memory/dashboard/DASHBOARD_FIELD_MAP.md` | Column and status definitions |
| `scripts/update_dashboard_snapshot.ps1` | Script that generates the snapshot |
| `memory/inbox/client_chat_start_prompt.md` | Start prompt that points Claude Chat to the snapshot |
