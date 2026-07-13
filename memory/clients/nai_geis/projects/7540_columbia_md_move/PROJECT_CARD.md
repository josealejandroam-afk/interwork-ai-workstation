# Project 7540 — NAI Geis Move, Columbia MD

## Core Facts

| Field | Value |
|---|---|
| Project number | 7540 |
| Client | NAI Geis |
| Location | Columbia, MD |
| Scheduled | 2026-07-13 to 2026-07-18 in Supabase (start date inferred, not directly confirmed — see below) |
| InterWork Field PM | Juan Martinez — juanm@interworkoffice.com, 732-979-7163 |
| Status | Scheduled |

## Supabase Sync (2026-07-10)

This project was missing from Supabase entirely — it only existed in the Smartsheet
calendar snapshot, never synced to the live database. The `smartsheet_sync` table was found
empty (0 rows), suggesting the automated Smartsheet-to-Supabase sync either isn't built or
isn't running — this may affect other projects beyond just this one.

Manually created 2026-07-10:
- `clients` row: "NAI Geis" (id `fb503eaa-1743-4a19-b3dc-a02481d54642`)
- `projects` row: project_number 7540, type workstation_relocation, status scheduled, linked
  to Juan Martinez as PM, location_city "Columbia", location_state "MD"
- Verified visible via `public.v_project_card` (the dashboard's project-card source)
- Initially left `scheduled_date` blank (source calendar only showed a week-long span), which
  made it invisible on the dashboard's Today view and the Live Map — both filter by date.
  Confirmed via a live screenshot that it wasn't appearing. Set `scheduled_date` = 2026-07-13,
  `scheduled_end_date` = 2026-07-18, inferred from the pattern of the two other projects on
  the same Smartsheet week (7420, 7378), which both start Monday 7/13. Not a directly
  confirmed exact day — verify with Juan or Smartsheet.

## Open Loops

| # | Item | Status |
|---|---|---|
| 1 | Confirm 7/13 is actually the right start day (currently inferred, not directly confirmed) | Open |
| 2 | ~~Confirm this shows correctly on the live map~~ | Resolved 2026-07-10 — now shows on dashboard Today view and Live Map after setting scheduled_date |
| 3 | Investigate why `smartsheet_sync` is empty — likely other Smartsheet-only projects missing from Supabase the same way | Open |

## Source Notes

- Source: `memory/shared/CALENDAR_SNAPSHOT.md` (Smartsheet calendar screenshot, 2026-07-10).
- Created: 2026-07-10, in response to Alejandro noticing this project missing from the dashboard/live map.
