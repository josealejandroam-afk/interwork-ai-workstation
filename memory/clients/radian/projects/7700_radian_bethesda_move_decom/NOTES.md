# Notes — Project 7700 Radian Bethesda

## 2026-09-10 Walkthrough Findings and Scope Reclassification

- Source: Melvin Hernandez Teams messages documenting the Bethesda walkthrough (with Kris
  Blalock) and requested execution plan; relayed by Alejandro Acosta 2026-09-10.
- Melvin's full walkthrough findings are now documented: the 9/14-9/15 schedule (~5 crew,
  requested arrival 6:00-6:30 AM or earlier, elevator available 6:00 AM-6:00 PM, day-1
  priorities of trash removal and packing, day-2 loading and cleanup); the New York-bound
  items list (~42 Humanscale dual monitor arms — Humanscale-style only, ~90 monitors/
  screens with count not final, keyboards/mice boxed together, 1 heavy TV, conference-room
  ceiling speakers with cables, ceiling-mounted meeting cameras, soundbars with cables, 1
  white sofa, 1 mobile whiteboard, 1 lamp, 1 printer, 1 shredder, plus possible additional
  labeled items); the Cherry Hill-bound items list (all docking stations, client-designated
  files/papers, IT-room black box plus the smaller box beneath it, 6 Cisco units from the
  black rack, 2 TVs, 2 white ceiling-mounted wireless devices, plus possible other labeled
  items); the trash/stay-in-place scope (small desk/table trash, labeled kitchen trash, all
  furniture stays onsite unless listed outbound, building supplies stay, TV wall brackets
  stay installed, vacuum/clean after); and the materials Melvin requested (15 Speedpacks,
  dollies, protective wrap for computers/cameras/soundbars, a ladder, small boxes for
  cables/docking stations, and moving blankets for TVs). Full detail filed in
  PROJECT_CARD.md under Walkthrough Findings.
- Scope reclassified: the previous working label "packing help and move to storage" (vs.
  Supabase's `decommission` type) is superseded. Recommended classification is now
  **Selective Decommission + Packing + Multi-Destination Equipment Relocation**. This is
  explicitly NOT a full furniture decommission — most furniture remains onsite. Do not
  describe this project as a simple storage move absent new evidence of a separate storage
  leg.
- Open loops moved from OPEN to RESOLVED by this update: (1) the 9/14-9/15 start time —
  requested arrival window of 6:00-6:30 AM, earlier if possible, is now documented (the
  onsite POC half of that item stays OPEN — Kris Blalock is directing the work but is not
  confirmed as the onsite POC); (2) full walkthrough findings — Melvin's documented scope
  satisfies this; (3) scope classification — the recommended classification is now
  documented for the memory/git record (note: whether Supabase's project-type field can
  actually store this text is a separate, still-open technical question, not resolved by
  this update).
- Open loops that were NOT touched by this update and remain OPEN: loading dock access/
  reservation (elevator hours 6:00 AM-6:00 PM are known, but that is not the same as dock
  access or a dock reservation); Quote 8677's $0 blank-scope shell; vendor/crew assignment
  and final client approval/PO.
- New open loops added: New York destination address and receiving POC not yet
  documented; Cherry Hill destination address and receiving POC not yet documented; final
  outbound quantities (~42 Humanscale monitor arms and ~90 monitors currently identified,
  but client labeling was still in progress at the time of the walkthrough — additional
  labeled items may be added before execution).

## 2026-09-08 Intake

- Created from the Teams project-number announcement, planning discussion and Quote 8677 proposal.
- Quote 8677 confirms the project, client, site and contact but contains no priced scope.
- Project remains planning-stage; no execution authorization is inferred.

## 2026-09-08 Walkthrough and COI Handoff

- A second handoff arrived the same day covering the walkthrough and COI. It claimed no
  existing project folder existed for 7700 — incorrect, this folder was already created
  earlier the same day from the Teams/Quote 8677 intake above. Merged into the existing
  folder rather than creating a duplicate with a different slug.
- Walkthrough confirmed: 9/8 9:00 AM, Kris Blalock + Melvin Hernandez, office boxed +
  subtenant-decluttering site survey. Melvin also ran a client-requested FedEx errand
  (~8 boxes) during the visit, confirmed by Alejandro via phone call with Melvin.
- COI sent by Scott Rasmussen 9/8 11:52 AM, referencing "Bethesda Crossing" — but the
  original 9/2 requirements doc from Kris was titled "EW Towers." Flagged as unresolved,
  not assumed to be the same property.
- Jill Buchman has 9/8 and 9/14-9/15 on InterWork's internal schedule (9/2 email) — this
  is calendar holding, not client-confirmed building access.
- Scope classification flagged: Alejandro's working label is "packing help and move to
  storage"; Supabase types this project `decommission`. Not reconciled yet — do not
  change either without confirming actual scope.
- Sources: email thread screenshots (Kris Blalock / Jill Buchman / Scott Rasmussen,
  9/2-9/8/2026), Alejandro's phone call with Melvin Hernandez (9/8), and the live
  dashboard/search/open-loops API (checked 2026-09-08).

## 2026-09-08 COI / Building-Name Resolution

- Alejandro reviewed the actual issued COI and resolved the "EW Towers" vs. "Bethesda
  Crossing" flag: Certificate Holder is Bethesda Crossing EW Acquisition LLC, c/o MRP Real
  Estate Services Group, 7315 Wisconsin Ave, Suite 420E, Bethesda, MD 20814; Description
  of Operations lists Bethesda Crossing EW Acquisition LLC and MRP Real Estate Services
  Group LLC as additional insured. Scott's original request referenced "EW Tower," and the
  issued file is named "COI - Bethesda Crossing.pdf" — "EW Tower(s)" is the
  building/property reference, "Bethesda Crossing EW Acquisition LLC" the legal entity
  used on the COI. Not conflicting destinations; no further confirmation from Scott/Kris
  needed on the naming question alone.
- COI submission and the building-name mismatch are both now resolved. Remaining open:
  loading dock week, 9/14-9/15 start time/POC, full walkthrough findings, and final scope
  classification (decommission vs. packing/move to storage).
