# Claritev / MultiPlan — Claude Chat Knowledge Pack

_Updated: 2026-07-28 | Source: memory/clients/claritev_multiplan/_

---

## How to Use This Pack

Upload this file to a Claude Chat Project named "Claritev" or "MultiPlan."
Start every session by telling Claude: "You have the Claritev knowledge pack loaded. Use it as your source of truth for all Claritev/MultiPlan projects."

---

## Client Overview

Claritev (formerly MultiPlan) is a healthcare cost management company. The company may appear as "MultiPlan" in older project records and "Claritev" in newer ones — use whichever name appears on the current paperwork.

---

## Known Projects

| # | Name | Location | Dates | Status | Notes |
|---|---|---|---|---|---|
| 7420 | Laguna Hills Decommission | 23322 Mill Creek Dr, Suite 200, Laguna Hills, CA 92653 | 7/13–7/15/26 | Active | Laguna Hills only. Address conflict remains open. |
| 7641 | Jupiter Delivery and Office Remodel | 4050 S US Highway 1, Suites 319-321, Jupiter, FL 33477 | 7/29–8/24/26 | Active — completion reconciliation needed | Standalone expanded project; do not label 7420 or 7583. |
| 6836 | MultiPlan Project | Needs confirmation | Historical | Needs confirmation | Older project number |
| 6837 | MultiPlan Project | Needs confirmation | Historical | Needs confirmation | Older project number |
| TBD | Claritev Chattanooga | Chattanooga, TN | Needs confirmation | Needs confirmation | Project number unknown |

---

## Project 7420 — Address Data Quality Flag

> **Do not use "Parsippany NJ" for project 7420.** The original ChatGPT export incorrectly identified this project as Parsippany, NJ. The confirmed location is **Laguna Hills, CA**.

Smartsheet contains two conflicting address spellings across legs:
- Leg 1 (3/27 walkthrough): "23382 Mill Creek Rd"
- Leg 2 (7/13 decom): "23322 Mill Creek Dr" ← used as authoritative (more recent)

**Confirm the correct address with Frank Barrett before dispatching crew.**

- FastField: not submitted on current leg

## Project 7641 — Jupiter Delivery and Office Remodel

- Carrier: Sunset Transportation
- Pickup: 2026-07-29 at NRS Warehouse, 14424 Bonelli Street, City of Industry, CA
- Delivery: 2026-08-03 at 8:00 AM to Epic Office Installations,
  35 SW 12th Ave, Suite 108, Dania Beach, FL 33004
- Epic receiving/install contact: Craig Bohres, 754-224-0912
- Sunset contact: Marcus Hasanovic, 616-322-8204
- Jupiter installation: 2026-08-04
- Plumbing: licensed plumber must install and test the refrigerator water line on 2026-08-03
- Privacy film: landlord-approved 5% dark reflective film; preferred installation 8/3–8/4,
  hard deadline 8/24

Open: award plumber, verify freight receipt, obtain film quote, confirm film installer,
coordinate access with Brian Geber, and confirm Epic's installation schedule.

### Project Number Rule

Jupiter originally began as a tail-end activity connected to the Laguna Hills work, but its
scope expanded enough to require a separate project number. Alejandro confirmed 7641 on 2026-08-17.

- Project 7420 is Claritev Laguna Hills only.
- Project 7583 belongs to Rothman.
- Project 7641 is Claritev Jupiter.

---

## Known Contacts

- Brian Geber — Jupiter office setup and privacy-film coordination
- Dave Marcotte — Regional Facilities Manager
- Craig Bohres — Epic Office Installations, 754-224-0912
- Marcus Hasanovic — Sunset Transportation, 616-322-8204

---

## Operating Rules for This Client

1. **Never use "Parsippany NJ" for project 7420** — location is Laguna Hills CA.
2. **Confirm address with PM before dispatch** — two conflicting spellings exist in Smartsheet.
3. **Keep the three projects distinct:** 7420 = Claritev Laguna Hills; 7583 = Rothman;
   7641 = Claritev Jupiter.
4. **Historical projects (6836, 6837) are sparse** — do not guess scope or status.
5. **Do not send communication** — draft only, Alejandro reviews and sends.
6. **Do not write to Supabase** — propose changes, wait for approval.

---

_To refresh this pack: tell Claude Code to regenerate claude_project_packs/claritev_multiplan_knowledge_pack.md_
