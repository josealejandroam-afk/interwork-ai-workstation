# Pending Handoff — Project 7347 BOL Confirmed + Sunset Vendor Contact Fill-In

**Written by:** Claude Chat (Desktop Commander)
**Date:** 2026-07-16 13:45
**Source:** Bill of Lading PDF (bill_of_lading_6482184.pdf) and email thread from Justin Maeck (Sunset Transportation) to Francisco Vinueza +2 others, shared by Alejandro, 2026-07-16.

---

## Part 1 — Project 7347: Shipping Confirmed (resolves remaining open loop item)

### Project Identity
- Project number: 7347
- Existing folder: memory/clients/marsh_mclennan/projects/7347_mma_mclean_consolidation/
- Updates OPEN_LOOPS.md (closes the "confirm carrier/tracking details" sub-loop from the 2026-07-15 pending handoff) and NOTES.md timeline.

### New Facts To Save
- Bill of Lading confirmed: Load #6482184, PO #7347, dated Jul 16, 2026.
- Shipper: InterWork, 439 Commerce Lane, West Berlin, NJ 08091. Contact on BOL: Francisco Vinueza, 609-744-1467.
- Consignee: McGriff, 1111 Military Cutoff Road, Suite 221, Wilmington, NC 28405. (Consistent with prior confirmation that McGriff is filed under marsh_mclennan as an MMA-affiliated entity.)
- Scheduled ship date/window: 07/16/2026, 1400-1500. Per Justin Maeck's follow-up email (7/16, 1:31 PM), driver ETA to pickup revised to 1600.
- Delivery: Wilmington, NC, 7/17/2026 @ 0800. Inside delivery to suite #221 (per BOL planning comments).
- Carrier: LAMTORO FREIGHT LLC (subcontracted carrier arranged via Sunset Transportation).
- Freight: 1 BIN, AV/conference room equipment, 1 C-bin, NMFC 39625-05, class 125.
- Billing: 3rd party, billed to Sunset Transportation, 10877 Watson Rd, St Louis, MO 63127, 800-849-6540.
- This matches and confirms what was already communicated to Chris Thorpe (delivery Friday 7/17) — no conflict.

### Open Loops To Update
- Resolve sub-loop "Confirm carrier name/tracking details once Francisco Vinueza follows up" — CONFIRMED: carrier LAMTORO Freight LLC via Sunset Transportation, Load #6482184, delivery 7/17 @ 0800.
- Main loop status: equipment picked up 7/16, in transit, delivery confirmed for 7/17 8:00 AM to Wilmington. Still open: closeout update to client once delivery is confirmed received, and confirmation of what was actually recovered vs. BOM (sub-loop items 8/9 from earlier handoffs — still not explicitly confirmed in writing, recommend closing only after delivery confirmation from Chris Thorpe).

### Timeline Additions
- 7/16/26, 1:04 PM: Justin Maeck (Sunset) sends BOL and shipment details — pickup NJ 7/16 @ 1400-1500, delivery Wilmington NC 7/17 @ 0800, carrier LAMTORO LLC.
- 7/16/26, 1:31 PM: Justin Maeck confirms driver ETA to pickup revised to 1600.

---

## Part 2 — Vendor File Update: memory/vendors/sunset.md

The existing Sunset vendor profile is a stub (all fields "unknown"). Fill in with confirmed details gathered across recent 7347 correspondence:

### Contacts (replace "unknown" row)
| Name | Role | Phone | Email | Notes |
|------|------|-------|-------|-------|
| Peter Daly | Agent of Sunset Transportation (nlm: Network Logistics Management), Armada company | 952-224-2403 x205 / 651-308-1002 | peter@sunsettrans.com | Primary quoting contact, handles rate/availability requests |
| Justin Maeck | Agent of Sunset Transportation, Network Logistics Management | 952-224-2403 x402 | jmaeck@sunsettrans.com | Handles BOL/dispatch coordination, based in Lakeville, MN |

### Other Notes
- Sunset Transportation is now branded "an Armada company" (seen in recent email signatures).
- Sunset brokers/subcontracts to underlying carriers — e.g., LAMTORO Freight LLC used for Load #6482184 (PO #7347).
- Billing/remit address: Sunset Transportation, 10877 Watson Rd, St Louis, MO 63127, 800-849-6540. Billing terms used: 3rd party.
- Past quote history observed (for rate-range reference, not to be shared with clients): cargo van NJ-to-NC (project 7347) ~$888; 53' van trailer Tampa-to-Mendota Heights, MN ~$3,981 (3-day transit); cargo van same-day NJ-to-Mount Pocono, PA ~$565; dedicated 26ft box truck Lakewood, CO-to-West Berlin, NJ ~$3,140.
- Update `status` field from stub to active, and `confidence` from low to medium given multiple confirmed data points.

### Requested Repo Action
1. Update memory/clients/marsh_mclennan/projects/7347_mma_mclean_consolidation/OPEN_LOOPS.md and NOTES.md per Part 1.
2. Update memory/vendors/sunset.md per Part 2 — replace unknown contact/identity fields, add past project rate notes, update metadata status/confidence.
3. Do not close the 7347 main loop yet — awaiting delivery confirmation and final recovered-items confirmation from the client side.

### Safety Notes
No email sent. Alejandro shared the BOL and email thread for context only; no action taken on the live thread itself. Rate figures noted are for internal vendor-reference only — per company rules, do not share vendor rate info with clients.
