# Current Dashboard Status
_AI-readable snapshot of the InterWork Operations Dashboard_

---

## Snapshot Metadata

| Field | Value |
|---|---|
| **Last Updated** | 2026-07-16 15:52 UTC |
| **Data Source** | Live read via `/api/ai/dashboard-summary` (source: `supabase:v_project_card`, confidence: live) |
| **Snapshot Method** | Automated — AI dashboard-summary API (read-only) |
| **Needs Refresh** | No — generated from live data |
| **Snapshot Age Warning** | If today's date is more than 1 day after Last Updated, treat counts as stale |

---

## Summary Counts

| Filter | Count |
|---|---|
| **All** | 166 |
| **Active** | 36 |
| **Alerts** | 16 |
| **At Risk** | 11 |
| **Today** | 7 |
| **Tomorrow** | 4 |
| **This Week** | 12 |

---

## Today's Projects (2026-07-16)

| Project # | Client | Location | Type | Date | Time | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|---|
| 7378 | MMA | 5990 Sepulveda Blvd, Suite 550, Van Nuys, CA | Decommission | 2026-07-13 | 9:00 AM | Frank Barrett | In Progress | IN_PROGRESS |
| 7427 | Oliver Wyman | Toronto, ON | Relocation | 2026-07-13 | — | David Steinbrecher | In Progress | IN_PROGRESS |
| 7547 | Dropbox | 50 Hawthorne St, San Francisco, CA | Install | 2026-07-15 | 9:00 AM | Pedro Martinez | Scheduled | READY |
| 7574 | MMA | 2301 Sugar Bush Road, Suite 600, Raleigh, NC | Install | 2026-07-15 | 9:00 AM | External PM | Scheduled | READY |
| 7465 | MMA | San Diego, CA → Van Nuys, CA | Relocation | 2026-07-16 | 3:30 PM | External PM | Scheduled | READY |
| 7597 | CRC | 1717 Alliant Avenue, Suites 1/4/5, Louisville, KY | Relocation | 2026-07-16 | 9:00 AM | External PM | Scheduled | READY |
| 7606 | Premier Ortho | 1 Bartol Avenue, Ridley Park, PA | Delivery | 2026-07-16 | 9:00 AM | Juan Martinez | Scheduled | READY |

---

## Tomorrow's Projects (2026-07-17)

| Project # | Client | Location | Type | Date | Time | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|---|
| 7427 | Oliver Wyman | Toronto, ON | Relocation | 2026-07-13 | — | David Steinbrecher | In Progress | IN_PROGRESS |
| 7547 | Dropbox | 50 Hawthorne St, San Francisco, CA | Install | 2026-07-15 | 9:00 AM | Pedro Martinez | Scheduled | READY |
| 7465 | MMA | San Diego, CA → Van Nuys, CA | Relocation | 2026-07-16 | 3:30 PM | External PM | Scheduled | READY |
| 7597 | CRC | 1717 Alliant Avenue, Suites 1/4/5, Louisville, KY | Relocation | 2026-07-16 | 9:00 AM | External PM | Scheduled | READY |

_Note: the API's own "tomorrow" set is carried over from prior-day rows still open — dates on these rows don't all literally equal 7/17. Reported as returned, not corrected._

---

## At-Risk Projects

| Project # | Client | Location | Type | Date | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|
| 7471 | MMA | TBD, Loveland, OH | Relocation | 2026-05-26 | Frank Barrett | Scheduled | AT_RISK |
| 7391 | Premier Ortho | 3809 W. Chester Pike, Suite 150, Newtown Square, PA | Decommission | 2026-06-24 | Melvin Hernandez | Scheduled | AT_RISK |
| 7494 | MMA | San Diego, CA → Walnut Creek, CA | Relocation | 2026-07-07 | External PM | Scheduled | INCOMPLETE |
| 7541 | ADL | Boca Raton, FL | Install | 2026-07-15 | _(none)_ | On Hold | INCOMPLETE |
| 7589 | Innovare | 15050 NW 79th Court, Suite 200, Miami Lakes, FL | Install | 2026-07-17 | External PM | On Hold | AT_RISK |
| 7571 | Spryson | Pittsburgh, PA | Relocation | 2026-07-20 | Melvin Hernandez | On Hold | INCOMPLETE |
| 7588 | CRC | Glen Allen, VA | Relocation | 2026-07-24 | Melvin Hernandez | Scheduled | INCOMPLETE |
| 7552 | Dropbox | 1800 Owens St, San Francisco, CA | Relocation | 2026-07-27 | _(none)_ | Scheduled | INCOMPLETE |
| 7549 | CRC | Indianapolis, IN | Relocation | 2026-07-31 | _(none)_ | Scheduled | INCOMPLETE |
| 7595 | MMA | Wilmington | Relocation | 2026-08-19 | _(none)_ | Scheduled | INCOMPLETE |
| 7594 | Amtrust | 15 Trafalgar Square, Nashua, NH | Walkthrough | _(unset)_ | _(none)_ | Planning | INCOMPLETE |

**⚠ Flag:** `7588 — CRC, Glen Allen, VA, scheduled 2026-07-24` looks like it may be the actual project for the "CRC Glen Allen AV Move" referenced in research this session (calendar showed 7/24 at 12 PM; we mistakenly filed it as project 7855, which was a quote number, and later deleted that record). `7588`'s scope_summary is empty in Supabase. Needs Alejandro to confirm before merging the AV move detail into 7588.

---

## Missing PM Projects (derived from At-Risk rows with no execution owner)

| Project # | Client | Location | Date | Status |
|---|---|---|---|---|
| 7541 | ADL | Boca Raton, FL | 2026-07-15 | On Hold |
| 7552 | Dropbox | 1800 Owens St, San Francisco, CA | 2026-07-27 | Scheduled |
| 7549 | CRC | Indianapolis, IN | 2026-07-31 | Scheduled |
| 7595 | MMA | Wilmington | 2026-08-19 | Scheduled |
| 7594 | Amtrust | 15 Trafalgar Square, Nashua, NH | _(unset)_ | Planning |

---

## Stale Scheduled Projects (derived: status=Scheduled with scheduled_date before 2026-07-16)

| Project # | Client | Location | Date | Execution Owner |
|---|---|---|---|---|
| 7471 | MMA | TBD, Loveland, OH | 2026-05-26 | Frank Barrett |
| 7391 | Premier Ortho | 3809 W. Chester Pike, Suite 150, Newtown Square, PA | 2026-06-24 | Melvin Hernandez |
| 7494 | MMA | San Diego, CA → Walnut Creek, CA | 2026-07-07 | External PM |

---

## Data Source Notes

- Source: live `/api/ai/dashboard-summary` and `/api/ai/search` endpoints (Supabase `v_project_card` view, read-only, no writes).
- Snapshot generated: 2026-07-16 15:52 UTC by Claude Code (no PowerShell/env-var run — pulled directly from the live AI API per `memory/dashboard/DASHBOARD_CHECK_RULES.md` source priority).
- Missing PM and Stale Scheduled tables are derived client-side from the At-Risk rows returned by the API (no dedicated endpoint fields for these yet) — treat as best-effort, not authoritative.
- "Tomorrow" rows as returned by the API include some carried-over in-progress/ready rows whose `scheduled_date` isn't literally 7/17 — flagged above, not corrected.
- This file is committed to GitHub and read by Claude Chat.
- Do not add secrets, tokens, or raw email content to this file.

---

## How to Refresh

```powershell
# From repo root:
.\scripts\update_dashboard_snapshot.ps1
```

Requires: `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` (or `SUPABASE_ANON_KEY`) set in environment.
If env vars are missing, the script will enter manual fallback mode.

Alternative (used for this refresh): pull `GET /api/ai/dashboard-summary` and `GET /api/ai/search?q=<term>` directly (see `memory/dashboard/DASHBOARD_CHECK_RULES.md`) and update this file by hand — no env vars required.
