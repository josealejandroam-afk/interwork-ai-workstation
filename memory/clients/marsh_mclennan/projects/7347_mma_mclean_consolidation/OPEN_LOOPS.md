# Open Loops — Project 7347 MMA McLean Consolidation / Wilmington AV Recovery

## Main Loop

Schedule Wilmington Zoom Room AV recovery visit at the former McLean office (8180 Greensboro Dr, Suite 400). Confirm building/site access via Ivy Ringhoff/landlord. Confirm recovery date week of 7/13/26, avoiding Tuesday per Melinda Morris's request. Confirm whether Stalin Alejandro Pena or Jose will be onsite. Confirm destination/shipping method for recovered equipment (direct to Wilmington vs. staged). Use the Alliance Telecommunications AV BOM/drawings (from Bob Kist) as the recovery checklist. Photo-document before/during/after. Send a closeout update on what was recovered, what was not found, and where it was shipped.

## Sub-Loops

| # | Item | Status |
|---|---|---|
| 1 | Reconcile original move scope/inventory against the Alliance AV BOM | Open |
| 2 | Confirm what actually shipped to Wilmington | Open |
| 3 | Confirm nothing was misrouted to DC | Open |
| 4 | Confirm final onsite inventory via Stalin's inspection + BOM | Open |
| 5 | Get access approval (Ivy Ringhoff / landlord) | Open |
| 6 | Schedule recovery visit, week of 7/13, not Tuesday | Open |
| 7 | Confirm Stalin or Jose onsite | Open |
| 8 | Recover all BOM-listed equipment | Open |
| 9 | Photo documentation | Open |
| 10 | Pack/label components | Open |
| 11 | Confirm destination + shipping method for recovered gear | Open |
| 12 | Closeout update to client | Open |
| 13 | Confirm routing: InterWork warehouse vs. direct to Wilmington, possible Columbia MD stop | Open |
| 14 | Confirm whether Tyr is assigned to the Wilmington delivery leg | Open |

## Conflict Flagged 2026-07-10 (Claude Code)

Project 7347 was sitting in a HELD, pending-approval Supabase batch-completion loop
("approve batch complete 6" — see `memory/shared/OPEN_LOOPS.md`, `memory/company_knowledge/GLOBAL_OPEN_LOOPS.md`,
`memory/references/interwork_ai_ops_master_context.md`), which would have set
`status = 'completed'` for 7347 based solely on `fastfield_submitted = true` from the
original May move. That signal predates this AV recovery finding and does not account
for it — the project has real, active, unresolved work. **Removed 7347 from that batch**
(now a 5-project batch: 7374, 7499, 7498, 7472, 7482) and from
`scripts/sql/draft_batch_complete_fastfield.sql`'s project list, so approving that batch
will no longer touch 7347. Do not mark 7347 completed until the AV recovery above closes out.

## Timeline

- 5/5/26: Manny Gonzalez handles crate delivery
- 5/13/26: Original move BOL (Sunset Transportation, Load #6414658)
- 7/8/26: Chris Thorpe reports missing AV equipment; Stalin suggests checking DC crates
- 7/9/26 AM: Melinda requests inventory review
- 7/9/26 midday: Melinda confirms equipment still onsite
- 7/9/26: Hunter confirms InterWork can return if access granted
- 7/9/26: Ivy contacts Bob Kist; Bob provides BOM/drawings
- Week of 7/13/26 (planned): recovery visit, avoid Tuesday per Melinda's request
- 7/10/26 (Ops Huddle): full AV system confirmed still at McLean (only the controller had shipped). Routing options discussed: return to InterWork warehouse, or truck directly to Wilmington with a possible stop in Columbia, MD depending on travel schedules. Tyr raised as a possible owner of the Wilmington delivery leg — not yet confirmed as an assignment.
