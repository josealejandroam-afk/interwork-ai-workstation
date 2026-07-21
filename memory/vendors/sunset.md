---
name: vendor-sunset
description: "Sunset Transportation (now associated with Armada) — freight/transportation coordinator profile, contacts, capabilities, and engagement rules"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: manual
  updated: 2026-07-16
  review_after: 2027-01-16
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# Sunset Transportation

Populated 2026-07-16 from Alejandro's training guide. See
[[sunset_transportation_workflow]] (`memory/procedures/sunset_transportation_workflow.md`)
for the full engagement workflow, status definitions, and message templates.

## Identity
- **Vendor name:** Sunset Transportation
- **DBA / common name:** Now associated with Armada — continue referring to as "Sunset Transportation" unless Sunset instructs otherwise.
- **Service area:** Regional and long-distance (dedicated + LTL); Midwest is a confirmed active tracking region (see `TrackingMN@sunsettrans.com`).
- **Services offered:** Freight and transportation coordination only — cargo van, dedicated 26-foot box truck, 53-foot dry van, LTL, warehouse-to-site and site-to-warehouse delivery, decommission material transportation.
- **Not a furniture/installation labor provider** unless a specific quote explicitly includes dismantle/pack/install services.

---

## Contacts

| Name | Role | Phone | Email | Notes |
|------|------|-------|-------|-------|
| Peter Daly | Agent of Sunset Transportation | Office 952-224-2403 ext. 205 / Cell 651-308-1002 | peter@sunsettrans.com | Primary contact for initial pricing, availability checks, dedicated van/box truck/FTL requests, transit-time estimates, capacity confirmation |
| Justin Maeck | Agent of Sunset Transportation, Network Logistics Management | Office 952-224-2403 ext. 402 | jmaeck@sunsettrans.com | Handles BOL/dispatch coordination; based in Lakeville, MN. Confirmed on project 7347 (BOL Load #6482184). |
| Marcus Hasanovic | Network Logistics Management | Office 952-224-2403 ext. 402 / Cell 616-322-8204 | mhasanovic@sunsettrans.com | Post-booking coordination, carrier assignment, pickup coordination, BOLs, pickup-address confirmation, shipment follow-up |
| Krista Tharaldson | Director of Customer Service | Office 952-224-2403 ext. 204 | ktharaldson@sunsettrans.com | LTL scheduling, driver status, pickup/delivery ETAs, missed/rolled pickups, BOLs, active shipment escalation |
| — | Tracking (Midwest) | — | TrackingMN@sunsettrans.com | Keep copied when Sunset includes it on an active Midwest shipment thread |

---

## Truck / Equipment Capabilities
- **Truck types:** Cargo van (small/urgent, same-day regional); dedicated 26-foot box truck (furniture, decom equipment, warehouse transfers); 53-foot dry van (large-volume/full-trailer shipments); LTL (shares carrier capacity, not dedicated).
- **Liftgate:** Available — confirm per shipment, do not assume.
- **Specialty equipment:** None documented beyond the truck types above.
- **Max / typical crew size:** Not applicable — Sunset provides transportation only, not loading/unloading or install labor unless a quote explicitly states otherwise.

---

## Pricing / Rate Notes
- **Rate structure:** Quote-based per shipment. No standing rate card on file.
- **Rate range:** Unknown — do not share with clients.
- **Minimum:** Unknown.
- **Extra charges:** Unknown (ask per quote: liftgate, pallet jack, appointment fees).
- **Invoicing:** Unknown.
- **Past quote history observed (2026-07-16, internal reference only — do not share with
  clients):** cargo van NJ-to-NC (project 7347) ~$888; 53' van trailer Tampa-to-Mendota
  Heights, MN ~$3,981 (3-day transit); cargo van same-day NJ-to-Mount Pocono, PA ~$565;
  dedicated 26ft box truck Lakewood, CO-to-West Berlin, NJ ~$3,140.
- **Billing/remit address:** Sunset Transportation, 10877 Watson Rd, St Louis, MO 63127,
  800-849-6540. Billing terms observed: 3rd party (billed to Sunset, not the carrier or the
  shipper directly).

## Subcontracting

Sunset brokers/subcontracts to underlying carriers rather than always driving loads
themselves — e.g., **LAMTORO Freight LLC** was the physical carrier for Load #6482184
(PO #7347, project 7347). Confirm the actual carrier name on each BOL rather than assuming
Sunset's own trucks are involved.

---

## Strengths
- Responsive on pricing/availability requests through Peter Daly (demonstrated contact for initial quotes).
- Active Midwest tracking channel (`TrackingMN@sunsettrans.com`) for shipment visibility.

## Weaknesses
- See BOL handoff gap under Issues/Incidents below.

---

## Reliability Notes
- **Arrival punctuality:** No aggregate data yet.
- **Communication:** No aggregate data yet.
- **Follow-through:** No aggregate data yet.
- **Overall rating:** Not yet rated — insufficient project history on file.

---

## Past Projects

| Project # | Job Name | Date | Scope | Outcome |
|-----------|---------|------|-------|---------|
| 7347 | MMA McLean/Wilmington AV recovery shipment | BOL 7/16/26, delivery 7/17 @ 0800 | Cargo/AV equipment, NJ (InterWork warehouse) to Wilmington NC, subcontracted to LAMTORO Freight LLC, Load #6482184 | **Delivery date conflicts with a separate internal account claiming same-day 7/15 delivery by a different driver — not reconciled, see project 7347's OPEN_LOOPS.md. Do not treat this outcome as fully confirmed either.** |

---

## Issues / Incidents
- **BOL handoff gap (undated, from training-guide screenshots):** A driver arrived onsite and departed before receiving the bill of lading from the shipper. Krista Tharaldson asked InterWork to print and sign the BOL while the driver was still onsite. Lesson: always confirm the pickup contact has the BOL printed and ready **before** the driver arrives; if the driver leaves without it, send the signed copy electronically to Sunset with an explanation.

---

## Preferred Use Cases
- Interstate/regional transportation where InterWork needs the freight moved but does not need dismantle, pack, or install labor performed.
- Decommission material transportation (warehouse-to-site and site-to-warehouse).
- Long-distance dedicated box truck or dry van moves.
- Same-day/urgent cargo van needs.

## Do-Not-Use Conditions
- Do not use Sunset for jobs requiring furniture install, dismantling, or packing labor unless the quote explicitly includes those services.
- Do not rely on LTL when exact pickup/delivery timing is critical, unless Sunset explicitly confirms an appointment or guaranteed service.

---

## Source Links
- Supabase: search `activity_log` or `projects` where Sunset appears.
- Smartsheet: search by vendor name.
- Full workflow/procedure: `memory/procedures/sunset_transportation_workflow.md`
