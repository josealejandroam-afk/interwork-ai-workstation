# Pending Handoff — Project 7347: Second Equipment Stream (Network Hardware, RETURN TO WESTLAKE)

**Written by:** Claude Chat (Desktop Commander)
**Date:** 2026-07-22 10:00
**Source:** AI-assisted warehouse equipment identification report (Opengear/Cisco serial and hostname matching against William A. Matthias's "MMA - MCLEAN - GREENSBORO - HARDWARE TO WESTLAKE" inventory email), pasted by Alejandro. This is an AI-generated assessment, not a confirmed physical inspection — treat as a lead requiring verification, per the same advisory-only standard applied to Copilot/ChatGPT output.

## Project Identity
- Project number: 7347
- Existing folder: memory/clients/marsh_mclennan/projects/7347_mma_mclean_consolidation/
- This is a NEW, separate equipment stream from the Zoom Room AV recovery already tracked in this project (different equipment type, different destination). Do not merge into the existing AV BOM/recovery narrative — add as a distinct section.

## New Facts To Save (flagged as unconfirmed pending physical verification)

**Proposed match:** Unidentified network equipment currently sitting in the InterWork warehouse is likely the McLean/Greensboro MMA network hardware referenced in William A. Matthias's email "MMA - MCLEAN - GREENSBORO - HARDWARE TO WESTLAKE," all marked disposition RETURN TO WESTLAKE.

**Inventory per that email:**
| Asset | Model | Serial (where given) |
|---|---|---|
| USMCL2-04AP01 through 04AP06 (6 units) | Mist AP34 wireless access point | — |
| USMCL2-04CG01 / 04CG02 | Palo Alto ION 5200 | — |
| USMCL2-04CN01 (Console Server) | Opengear OM2216 | 22162503320399 |
| USMCL2-04CS01 (Core Switch) | Cisco C9300X-48HX | — |
| USMCL2-04CS02 (Core Switch) | Cisco C9300X-48HX | FVH2902L40Z |

**Basis for the match:**
- Warehouse Opengear OM2216 unit's visible label serial "appears to" read 22162503320399 — matches the email's USMCL2-04CN01 exactly, but described as visual inspection only, not a confirmed/verified read.
- A box of access points in the warehouse is consistent with the 6x Mist AP34 units listed, if visually confirmed as that model.
- A previously-asked-about hostname, USMCL2-04CS02, matches the email's Cisco C9300X-48HX core switch entry (serial FVH2902L40Z).
- Connects to 7347 because Juan Martinez (already the confirmed InterWork PM for the 7347 McLean recovery visit, 7/15/26) handled the McLean/Greensboro recovery this equipment would have come from.

## Recommended Action (per the source report, not yet executed)
- Tag this equipment as belonging to project 7347.
- **Do not release/ship it** until Alejandro confirms current Westlake shipping instructions directly with William A. Matthias — the email's disposition may be outdated by now.
- Physically verify the Opengear serial number and AP model against the email before treating the match as certain.

## Requested Repo Action
1. Add a new section to project 7347 (NOTES.md or a new "Network Equipment" section in PROJECT_CARD.md) documenting this as a second, distinct recovered-equipment stream — separate from the Zoom Room AV BOM already tracked, different destination (Westlake, not Wilmington).
2. Add William A. Matthias as a new contact (role/company not yet specified in what was shared — confirm with Alejandro; likely MMC/MMA IT or facilities).
3. Add an open loop: "Confirm current Westlake shipping instructions with William A. Matthias before releasing network equipment; physically verify Opengear serial and AP model match before treating identification as final."
4. Do not mark this equipment as resolved/shipped in any tracker until both the physical verification and the Westlake shipping confirmation happen.

## Safety Notes
No shipment, release, or communication with William Matthias has occurred yet. This is an identification lead only.
