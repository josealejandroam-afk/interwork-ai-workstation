# Pending Handoff — Project 7595 POC Split, Supply Receipt Confirmed, Zip Code Correction

**Written by:** Claude Chat (Desktop Commander)
**Date:** 2026-07-21 16:15
**Source:** "Moving Supplies" email thread, Brad Southerland / Jill Buchman / Chris Thorpe / Alejandro Acosta, 2026-07-17 through 2026-07-21, shared by Alejandro.

## Project Identity
- Project number: 7595
- Existing folder: memory/clients/marsh_mclennan/projects/7595_mcgriff_wilmington_consolidation/

## New Facts To Save

**Supply delivery confirmed:**
- Jill Buchman followed up 7/21, 1:13 PM checking on receipt.
- Brad Southerland confirmed 7/21, 1:58 PM: supplies received, "everything went smooth."

**POC split — confirmed by Chris Thorpe (7/19, 5:34 PM):**
- Brad Southerland is the POC for the origin location (1411 Commonwealth Drive, Suite 201).
- Chris Thorpe is the POC for "the Military location" — i.e., the destination (1111 Military Cutoff Road, Suite 221).
- Update PROJECT_CARD.md Key Contacts table to reflect this split explicitly rather than just listing both names without role-to-location mapping.

## Correction (Not Just New Fact) — Destination Zip Code

- PROJECT_CARD.md currently lists the destination as: "1111 Military Cutoff Road, Suite 221, Wilmington, NC **28403**"
- This appears to be an error — likely copied from the origin's zip (Commonwealth Drive is 28403).
- Three independent sources all say **28405** instead:
  1. Project 7347's PROJECT_CARD.md (tech shipment destination): "...Wilmington, NC 28405"
  2. The Sunset Transportation BOL (Load #6482184, consignee McGriff): "...WILMINGTON, NC 28405"
  3. Brad Southerland's own email auto-signature/company notice (7/21 thread): "NEW PHYSICAL ADDRESS: 1111 Military Cutoff Road, Suite 221, Wilmington, NC 28405"
- Recommend correcting 7595's PROJECT_CARD.md destination zip to 28405. Flagging as a correction rather than applying it silently, per repo convention — Claude Code should verify before overwriting.

## Additional Context (client's own notice, informational)
- Brad Southerland's signature includes a standing company notice: "We are moving. Effective August 18, we will be moving to a new location in Wilmington, NC... Keep in mind – our payment address remains the same." This independently corroborates the 8/18 date already on file (last day at origin) — no conflict, just a client-side confirmation worth noting as a source in NOTES.md.

## Requested Repo Action
1. Update PROJECT_CARD.md Key Contacts: Brad Southerland (origin POC), Chris Thorpe (destination/"Military location" POC).
2. Correct destination zip code from 28403 to 28405 in PROJECT_CARD.md (cross-verify against 7347 and the BOL before applying).
3. Add to NOTES.md/OPEN_LOOPS.md: supply order received and confirmed by Brad Southerland, 7/21/26 — no issues reported. This can close the "confirm packing supplies delivered" open item, though the earlier box/C-bin quantity vs. Uline order-type discrepancy (flagged in the 2026-07-17_1530 handoff) is still unresolved and separate from delivery success.

## Safety Notes
No email sent or replied to as part of this handoff — Alejandro shared the thread for context only.
