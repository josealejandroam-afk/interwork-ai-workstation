# Open Loops — Project 7347 MMA McLean Consolidation / Wilmington AV Recovery

## Main Loop — REOPENED 2026-07-21 (delivery timeline conflict)

Recovery itself is complete: the Wilmington Zoom Room AV recovery visit occurred as
scheduled 7/15, all BOM-listed equipment was recovered from the vacated McLean office and
packed. **Delivery is not confirmed closed** — two incompatible accounts of the actual
delivery exist (same-day direct drive by "Aaron" on 7/15, vs. a Bill of Lading showing
freight shipment via Sunset Transportation/LAMTORO Freight LLC with delivery 7/17 @ 0800).
See PROJECT_CARD.md "Conflicting Shipping Accounts." Do not close this loop until Chris
Thorpe's actual receipt is confirmed against one of these two accounts.

## Sub-Loops

| # | Item | Status |
|---|---|---|
| 1 | Reconcile original move scope/inventory against the Alliance AV BOM | Closed 2026-07-17 — Stalin's inspection + the BOM drove the recovery, all listed items recovered |
| 2 | Confirm what actually shipped to Wilmington originally | Closed — only the Zoom touch controller (per the AV issue discovery), remainder recovered separately 7/15 |
| 3 | Confirm nothing was misrouted to DC | Not explicitly addressed in the completion handoff — no DC issue reported, treating as non-issue |
| 4 | Confirm final onsite inventory via Stalin's inspection + BOM | Closed — inventory confirmed, recovery matched |
| 5 | Get access approval (Ivy Ringhoff / landlord) | Closed — access was obtained, recovery occurred |
| 6 | ~~Schedule recovery visit, week of 7/13, not Tuesday~~ | **Confirmed 2026-07-14** — Wednesday 2026-07-15, 8:00 AM |
| 7 | ~~Confirm Stalin or Jose onsite~~ | **Confirmed** — Stalin Alejandro Pena met the team onsite at 8:00 AM |
| 8 | ~~Recover all BOM-listed equipment~~ | **Closed 2026-07-17** — Poly Studio X72, QSC processor, Extron amp, Netgear switch, Shure mics, Sonance speakers, cabling/mounts all recovered |
| 9 | Photo documentation | Not confirmed in the completion handoff — assume done per standard practice, not explicitly stated |
| 10 | ~~Pack/label components~~ | **Closed 2026-07-17** — packed for transport |
| 11 | **REOPENED 2026-07-21** — Confirm destination + shipping method for recovered gear | Conflicting: one account says direct drive to Wilmington 7/15 AM (driver Aaron); a Bill of Lading says freight via Sunset/LAMTORO, delivery 7/17 @ 0800. Verify directly with Chris Thorpe or Francisco Vinueza before treating either as final. |
| 12 | Closeout update to client | Not confirmed sent — do not send until the shipping conflict above is resolved, since the delivery date itself is in question |
| 13 | **REOPENED 2026-07-21** — Confirm routing | Conflicting: "direct to Wilmington, no stop" (Account A) vs. "via InterWork NJ warehouse, then freight-forwarded" (Account B, per BOL shipper address). Not resolved. |
| 18 | Reconcile Stalin Alejandro Pena's office phone number — repo previously had 703-267-7885, his 7/15 email signature shows 202-263-7885. Mobile (202-826-7920) confirmed consistent in both. Alejandro reviewed and chose to flag both rather than pick one. | Open — not blocking, informational |
| 14 | ~~Confirm whether Tyr is assigned to the Wilmington delivery leg~~ | **Resolved 2026-07-14** — Juan Martinez confirmed as InterWork PM for the recovery visit. |
| 15 | ~~Confirm recovery day within week of 7/13~~ | **Resolved 2026-07-14** — Wednesday 7/15, not Monday as earlier speculated; not a Tuesday either way. |

## New Open Item — 2026-07-17

| # | Item | Status |
|---|---|---|
| 16 | Whether client identifies missing components during unpacking, or requests AV install/recommissioning support | Open — contingent, not currently active |
| 17 | Whether a separate client-facing closeout communication is still needed beyond this internal completion summary | Open — check with Alejandro |

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
- 7/10/26 (later): Alejandro decided Juan is the more likely pickup person since he'll already be in the area (supersedes the earlier Tyr idea, not yet finalized). Also flagged that the client may want the recovery specifically on Monday rather than just "avoid Tuesday" — checking with Francisco before locking the date.
- 7/14/26: Calendar entry confirms recovery visit for Wednesday 7/15, 8:00 AM. Juan Martinez confirmed as InterWork PM. Stalin Alejandro Pena confirmed as onsite POC, confirmed he can meet the team at 8:00 AM. Destination/shipping plan for recovered equipment still to be confirmed *after* pickup — items 11/13 (routing) remain open.
- 7/15/26, 10:05 AM: Chris Thorpe asks about carrier/ETA for the recovered equipment.
- 7/15/26, 10:20 AM: Stalin Alejandro Pena defers to Francisco Vinueza on carrier/ETA.
- 7/15/26, 10:23 AM: Francisco Vinueza states equipment is going by private carrier, targeting NC arrival by Friday 7/17.
- 7/15/26, 11:14 AM: Chris Thorpe confirms he'll be in the Wilmington office Friday 7/17 to receive it.
- 7/16/26, 1:04 PM: Justin Maeck (Sunset Transportation) sends BOL and shipment details — pickup NJ 7/16 @ 1400-1500, delivery Wilmington NC 7/17 @ 0800, carrier LAMTORO Freight LLC.
- 7/16/26, 1:31 PM: Justin Maeck confirms driver ETA to pickup revised to 1600.
- (Separately, per a different/later-processed handoff: recovery visit occurred 7/15 8:00 AM and one account states same-day delivery to Wilmington via driver Aaron — see "Conflicting Shipping Accounts" in PROJECT_CARD.md. Not reconciled with the BOL timeline above.)
