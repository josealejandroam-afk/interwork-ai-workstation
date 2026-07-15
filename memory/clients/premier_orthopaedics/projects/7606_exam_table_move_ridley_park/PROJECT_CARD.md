# Project 7606 — Premier Orthopaedics Exam Table Move

## Core Facts

| Field | Value |
|---|---|
| Project number | 7606 |
| Client | Premier Orthopaedics |
| Project name | Exam Table Move |
| Location | Ridley Park, PA (per Smartsheet calendar — full address not confirmed) |
| Scheduled date | 2026-07-16 (per Smartsheet calendar) |
| PM | Needs confirmation |
| Status | Scheduled per Smartsheet |

## Second Activity Under Same Project Number (flagged, not merged)

Smartsheet calendar also shows a second line item under project 7606 on **2026-07-23**:
"Donation pickup," location partially cut off in the calendar view (possibly Rockledge, PA —
not confirmed). Supabase's `projects` table only supports one `scheduled_date` per
`project_number`, so only the 7/16 exam table move is reflected there — this second activity
is not captured in Supabase and needs a decision on how to track it (second project number?
sub-record?) once confirmed.

## Missing Information

- Full site address for the exam table move
- PM assignment
- Details and confirmed location for the 7/23 donation pickup
- Whether the two activities are billed/tracked together or need separate project numbers

## Source Notes

- Source: Smartsheet calendar, viewed 2026-07-15 — this project was missing from Supabase
  entirely; added during a full-calendar reconciliation pass
- Created: 2026-07-15
