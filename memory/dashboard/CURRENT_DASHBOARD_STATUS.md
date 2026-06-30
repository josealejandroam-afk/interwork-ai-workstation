# Current Dashboard Status
_AI-readable snapshot of the InterWork Operations Dashboard_

---

## Snapshot Metadata

| Field | Value |
|---|---|
| **Last Updated** | 2026-06-30 |
| **Data Source** | Manual screenshot — live Supabase read not available at snapshot time |
| **Snapshot Method** | Manual — captured from dashboard screenshot |
| **Needs Refresh** | Yes — run `scripts/update_dashboard_snapshot.ps1` when Supabase env vars are available |
| **Snapshot Age Warning** | If today's date is more than 1 day after Last Updated, treat counts as stale |

---

## Summary Counts

| Filter | Count |
|---|---|
| **All (active)** | 140 |
| **Alerts** | 47 |
| **At Risk** | 46 |
| **Today** | 4 |
| **Tomorrow** | 3 |
| **This Week** | 9 |

---

## Today's Projects (2026-06-30)

| Project # | Client | Location | Type | Date Range | Time | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|---|
| 7053 | StratEdu | 901 15th St NW, Washington | Relocation | 3/21/26–6/30/26 | 9:00 AM | Juan Martinez | Scheduled | Ready |
| 7391 | Premier Ortho | 3809 W. Chester Pike, Suite 150, Newtown Square | Decom | 4/24/26–6/30/26 | — | Melvin Hernandez | Scheduled | At Risk |
| 7552 | Dropbox | 1800 Owens St, San Francisco, CA 94117 | Relocation | 6/22/26–6/30/26 | 9:00 AM | Frank Barrett | Scheduled | At Risk |
| 7556 | MMA | 1717 Main St, Dallas, TX | Install | 6/24/26–6/30/26 | 9:00 AM | External PM | Scheduled | Ready |

---

## Tomorrow's Projects

_Not captured in this snapshot — run live refresh to populate._

---

## At-Risk Projects

_Full at-risk list not captured in this snapshot._
At-risk count: **46** (from summary counts above).
Run live refresh to get full at-risk row details.

---

## Missing PM Projects

_Not captured in this snapshot — run live refresh to populate._

---

## Stale Scheduled Projects

_Not captured in this snapshot — run live refresh to populate._

---

## Data Source Notes

- This snapshot was created manually from a dashboard screenshot taken on 2026-06-30.
- Only Today rows were captured at row level. Tomorrow, at-risk detail, missing PM, and stale scheduled rows are not available without a live Supabase read.
- Summary counts (All, Alerts, At Risk, Today, Tomorrow, This Week) are from the same screenshot and are reliable for that point in time.
- To get full row-level data, run `scripts/update_dashboard_snapshot.ps1` with valid Supabase env vars.

---

## How to Refresh

```powershell
# From repo root:
.\scripts\update_dashboard_snapshot.ps1
```

Requires: `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (or `SUPABASE_ANON_KEY` with RLS) set in environment.
If env vars are missing, the script will prompt for manual fallback mode.
