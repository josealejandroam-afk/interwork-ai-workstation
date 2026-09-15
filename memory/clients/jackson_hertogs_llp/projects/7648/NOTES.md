# Notes — Jackson & Hertogs LLP December 2026 Move

## 2026-08-07 — Initial Repository Intake

- Project number 7648 was confirmed directly by Alejandro on August 18, 2026; the prior unnumbered project folder was renamed to the canonical numbered folder.
- Recorded 909 Montgomery Street, Suite 200 as the origin.
- Recorded 388 Market Street, 14th Floor, Suite 1460 as the drawing-based planning destination, subject to Brooks's confirmation.
- Preserved the conflict with the earlier email recap that identified Suite 200 at the destination.
- Recorded the project as an integrated planning, selective-reuse move, installation and decommission engagement.
- Recorded the requested December 12–13 move weekend and December 14 lease expiration without treating the exact execution window as final.
- Captured Francisco's August 6 walkthrough conclusion that most existing furniture will not fit and additional measurements/design coordination are needed.
- No emails, credentials or unconfirmed project number were added.

## 2026-08-18 — Inventory and Design-Planning Update

- Confirmed the August 12 follow-up measurement visit by Francisco Vinueza and Jairo Escalante at both locations.
- Marked the full 909 Montgomery furniture inventory complete based on Jill's August 18 update.
- Preserved Suite 1460 as the architectural planning reference while keeping the earlier Suite 200 discrepancy open.
- Added the long-white-table / approximately eight-seat benching configuration as an active design decision.
- Separated the engagement into inventory/assessment, reuse planning, relocation, and decommission workstreams.
- Preserved December 12–13 as a requested planning weekend, not a confirmed execution schedule.
- Added Brooks Paine, Lisa Gelardi, Ryan Kenney, Jill Buchman, Jairo Escalante and David Steinbrecher to the operational context.
- Supabase Project 7648 and the Jackson & Hertogs LLP client record already exist; update those records rather than creating duplicates.

## August 18, 2026 — Brooks Call Timing

- A next-steps call with Brooks Paine remains pending.
- A 1:30 PM PT conflict was noted; no replacement call time is confirmed.

## 2026-08-26 — Detailed Scope and Data Reconciliation

- Reconfirmed that 7648 is the InterWork project number based on Alejandro's August 18 direction; the newer handoff's "not confirmed" statement is stale. Drawing 37491 must not be used as the project number.
- Added the current Suite 1460 plan: four workstations, three private offices, no dedicated reception desk/sofa, one workstation serving reception, and private-office desks limited to 60 inches or smaller.
- Added the current move inventory: three desks, four workstations, seven office chairs, seven VariDesks, double-monitor setups, signage, artwork and one fireproof safe.
- Excluded regular Jackson & Hertogs filing cabinets from the move while retaining the safe.
- Added the full origin decommission, separate other-law-firm decommission line item, low-voltage workstream and separately priced conference-room island/credenza.
- Preserved December 12-13 as an unconfirmed target and Suite 1460 as a planning destination pending formal confirmation.
- The 909 Montgomery furniture inventory remains complete.

## 2026-08-26 — Supabase Sync

- Updated the existing Project 7648 record; no duplicate project or client was created.
- Retained `planning` status and left `client_confirmed`, `vendor_confirmed`, `access_confirmed`, and `pm_assigned` false.
- Stored December 12-13 as target dates with explicit unconfirmed-date and unconfirmed-suite tags.
- Added the primary open loop `Finalize furniture reuse/layout and scope split`.
- Logged the update in `activity_log` as `Codex@FrankWork`, source `manual`.

## 2026-09-15 — Repeat Handoff Reconciliation

Alejandro supplied another "Updated Git + Supabase Handoff" for this project, almost entirely restating the August 26 content verbatim (same locations, contacts, background, new-space plan, relocation inventory, decommission scope, other-law-firm scope, low-voltage scope, conference-room island/credenza, and proposal structure). Reconciled as follows:

- **Project number:** this handoff again states "Not confirmed" and repeats "do not use drawing number 37491 as the InterWork project number." As on August 26, this is stale — Project 7648 was confirmed directly by Alejandro on August 18, 2026, and remains the confirmed number. Not reverted.
- **Long-white-table / eight-seat benching item:** the August 18/26 records carry an open item to reconcile an "approximately eight-seat long-white-table concept" with the current four-workstation direction (see OPEN_LOOPS.md #6). This newest handoff does not mention that concept at all. It is unclear whether it has been dropped or is simply omitted from this restatement — **carried forward as open rather than silently removed; confirm with Alejandro whether the long-white-table concept is still live.**
- **Open items:** all 14 items listed in this handoff match existing open loops already tracked (destination suite, private-office furniture assignment, workstation configuration, CAD/layout, refrigerator disposition, low-voltage/data/fiber, lease-end requirements, patch/paint, building protection, freight/loading, COI, exact December schedule, island/credenza pricing, move-vs-decom inventory split). None resolve any existing open loop with new information — no facts changed, so OPEN_LOOPS.md is unchanged apart from the note above.
- **Supabase contact gap found and fixed:** despite this project's Git contacts table being complete since August, Supabase had no contact records for Brooks Paine, Lisa Gelardi, Ryan Kenney, Jill Buchman, or Jairo Escalante (only David Steinbrecher existed, and `client_poc_id` on the project was NULL). Created the missing contacts and set `client_poc_id` to Brooks Paine while processing this handoff — an overdue sync gap, not new information from this handoff.
