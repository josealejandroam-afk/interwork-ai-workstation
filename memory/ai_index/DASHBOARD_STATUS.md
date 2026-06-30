# Dashboard Status — AI Index
_Last updated: 2026-06-30_
_Mirrored from: memory/dashboard/CURRENT_DASHBOARD_STATUS.md_

---

## Live AI API Endpoints (use these first)

**Dashboard summary** (counts + today/tomorrow/at-risk rows):
```
GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary
```
- Returns: `counts`, `today_rows`, `tomorrow_rows`, `at_risk_rows` — live from Supabase
- No auth required. `confidence: "live"`. No secrets exposed.
- Confirmed live: 2026-06-30 (all: 146, active: 66, today: 7, tomorrow: 8, this_week: 12, alerts: 50, at_risk: 47)

**Search** (project/client/location/PM/scope lookup):
```
GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>
```
- Returns up to 25 matching project rows. Use before scanning repo folders.
- No auth required. Minimum 2 characters. Confirmed live: 2026-06-30.

**Use the snapshot below only if the API is unavailable.**

---

> **Staleness warning (snapshot):** This file mirrors the dashboard snapshot. If today's date is more than 1 day after "Last Updated" below, counts and rows are stale.
> For live data, call the API above or run `scripts/update_dashboard_snapshot.ps1`.

---

## Snapshot Metadata

| Field | Value |
|---|---|
| **Last Updated** | 2026-06-30 |
| **Data Source** | Manual screenshot — live Supabase read not available at snapshot time |
| **Snapshot Method** | Manual |
| **Needs Refresh** | Yes — run `scripts/update_dashboard_snapshot.ps1` when Supabase env vars are available |

---

## Summary Counts (as of 2026-06-30)

| Filter | Count |
|---|---|
| All (active) | 140 |
| Alerts | 47 |
| At Risk | 46 |
| Today | 4 |
| Tomorrow | 3 |
| This Week | 9 |

---

## Today's Projects (2026-06-30)

| Project # | Client | Location | Type | Time | Status | Readiness |
|---|---|---|---|---|---|---|
| 7053 | StratEdu | 901 15th St NW, Washington DC | Relocation | 9:00 AM | Scheduled | Ready |
| 7391 | Premier Ortho | 3809 W. Chester Pike, Suite 150, Newtown Square PA | Decom | — | Scheduled | At Risk |
| 7552 | Dropbox | 1800 Owens St, San Francisco CA | Relocation | 9:00 AM | Scheduled | At Risk |
| 7556 | MMA | 1717 Main St, Dallas TX | Install | 9:00 AM | Scheduled | Ready |

---

## Full Snapshot

Full snapshot with data source notes:
`memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

Raw GitHub URL:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

---

## How to Refresh

```powershell
.\scripts\update_dashboard_snapshot.ps1
```

After refresh, re-run `scripts/update_ai_index.ps1` to pull the updated counts into this file.
