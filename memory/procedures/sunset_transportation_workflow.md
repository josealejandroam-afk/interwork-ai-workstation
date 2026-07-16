---
name: sunset-transportation-workflow
description: "How Claude engages Sunset Transportation — when to use them, quote-to-delivery workflow, status definitions, and message templates"
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

# Sunset Transportation Workflow
_Last updated: 2026-07-16. See [[vendor-sunset]] (`memory/vendors/sunset.md`) for contacts and vendor profile._

Sunset Transportation is a freight/transportation coordinator, not an installation
company or furniture-moving labor provider, unless a specific quote explicitly
includes those services.

---

## When to Engage Sunset

Contact Sunset for:
- Same-day or urgent cargo van service
- Dedicated 26-foot box trucks
- Full 53-foot dry van trailers
- Long-distance or regional transportation
- LTL freight
- Furniture and equipment transfers
- Warehouse-to-site deliveries / site-to-warehouse returns
- Decommission material transportation

Sunset is especially useful when InterWork needs transportation between cities or
states but does not need Sunset to dismantle, pack, install, or handle furniture
inside the facilities.

---

## Information Required Before Requesting a Quote

Confirm or request the following before drafting a Sunset inquiry. **Do not invent
missing information** — use "to be confirmed" or ask Alejandro for the missing detail.

- InterWork project number
- Pickup address / delivery address
- Pickup contact and phone / delivery contact and phone
- Requested pickup date / requested delivery date
- Access hours; whether appointments are required
- Equipment requested, if known
- Inventory or freight description; approximate volume; approximate weight, if available
- Pallet count, if applicable
- Whether freight is boxed, wrapped, palletized, or loose
- Whether loading/unloading assistance is available
- Whether a liftgate or pallet jack is required
- Whether the shipment is ready
- Any hard deadline or urgency; any site restrictions

---

## Selecting the Service Type

**Cargo van** — smaller urgent shipments that safely fit inside a van (small equipment
shipments, limited boxed material, same-day regional delivery).

**Dedicated 26-foot box truck** — full box truck, not a tractor-trailer (office
furniture, decom equipment, warehouse transfers, regional/interstate dedicated
delivery). Confirm whether a liftgate or loading dock is required.

**53-foot dry van** — large-volume shipments expected to fill or substantially use a
full trailer. Provide detailed inventory, estimated cubic footage, pickup readiness
date, loading/unloading arrangements, and whether it's straight-through dedicated
service. **Do not state the shipment fits one trailer** unless volume has been
reasonably assessed — instead say: "Estimated to fit one 53-foot dry van, subject to
Sunset's assessment."

**LTL** — shipment doesn't require a dedicated truck and can travel with other
freight. Do not select LTL when exact pickup/delivery timing is critical, unless
Sunset confirms an appointment or guaranteed service.

### Dedicated vs. LTL
Dedicated service is assigned specifically to the InterWork shipment: better timing
control, direct transportation, fewer handling points, clearer coordination. LTL
shares carrier capacity and may involve terminal transfers, flexible pickup windows,
deliveries occurring before pickups, afternoon pickups, delays, or pickups rolling to
the next business day. **Never present an LTL pickup time as guaranteed** unless
Sunset explicitly confirms it is guaranteed.

---

## Standard Quote-Request Workflow

1. **Ask for capacity and pricing.** Include project number, pickup/delivery location,
   requested date, requested equipment/service type, freight description, timing
   requirement, and a request for pricing + estimated transit time.
2. **Review the quote.** A price + capacity response is only a quote — never describe
   it as booked. Review price, equipment type, transit time, pickup/delivery timing,
   dedicated vs. LTL, limitations, whether it's based on a placeholder address, and
   whether Sunset needs more information.
3. **Approve the booking.** InterWork must explicitly authorize Sunset to proceed. A
   quote is not approval.
4. **Obtain booking confirmation.** After approval, confirm Sunset has entered the
   order, assigned/requested capacity, confirmed pickup date, confirmed delivery
   expectation, and issued the Sunset order number and BOL (when applicable).
5. **Monitor pickup.** Before pickup, confirm driver assignment, pickup ETA, pickup
   contact, freight readiness, BOL availability, loading access, truck requirements.
6. **Monitor transit.** After pickup, confirm freight was loaded, pickup completed,
   delivery date/window, updated ETA when available, any delays/exceptions.
7. **Confirm delivery.** Do not mark a shipment delivered based only on a scheduled
   arrival time — confirm via Sunset confirmation, driver confirmation, receiving
   contact confirmation, proof of delivery, or signed delivery documentation.

---

## Shipment Status Definitions

Use these accurately — **never skip directly from "quoted" to "in transit" without
evidence.**

| Status | Meaning |
|---|---|
| Quoted | Sunset provided price, capacity, or transit info. Not booked. |
| Approved | InterWork instructed Sunset to proceed. Doesn't mean a carrier is assigned yet. |
| Booked | Sunset confirmed the shipment was entered/accepted. Order number or booking confirmation usually available. |
| Driver assigned | A carrier/driver assigned. Pickup hasn't necessarily occurred. |
| En route to pickup | Driver traveling to the pickup location. |
| Picked up | Sunset or site confirms freight was loaded and departed. |
| In transit | Freight picked up and moving toward destination. |
| Out for delivery | Driver traveling to the delivery location. |
| Delivered | Shipment arrived and was accepted at destination. |
| Exception / rollover | Pickup or delivery delayed, missed, or moved to another date. |

**Sunset order numbers** (e.g. "Sunset Order No. 6406895") should be captured in
project notes and used in tracking email subjects, e.g.:
`Status Request | Sunset Order 6406895 | Project 7492`

**Pickup alerts / shipment documents** from Sunset may include order number, status,
shipper/consignee, addresses, site contacts, scheduled pickup/delivery, arrival and
departure fields, driver info, tractor/trailer info, BOL info, and stop details. The
scheduled time shown is not always the current live ETA — when a shipment is late,
request a direct status update.

---

## Bill-of-Lading (BOL) Process

Before pickup, remind Alejandro to confirm: Sunset issued the BOL, the pickup contact
received and can print it, it's ready for the driver, the shipper signs it where
required, and a signed copy is retained.

If a driver leaves before receiving the signed BOL, send the signed copy
electronically to Sunset with an explanation of what occurred (see template below).

---

## Tracking and Follow-Up Rules

Help Alejandro monitor: driver assignment, pickup ETA, arrival at pickup, loading
completion, departure from pickup, delivery date/window, final delivery ETA, delivery
completion.

- If the driver is late: ask for current status and updated ETA.
- If an LTL pickup nears end of day: confirm whether it's still expected today or
  rolling to tomorrow.
- If a scheduled delivery time has passed: state the scheduled time, note it hasn't
  arrived, and request current status + updated ETA.

---

## Communication Style

Direct, professional, operational, brief, specific, time-sensitive when required.
Avoid unnecessary project history. Use exact addresses, dates, deadlines, equipment
types. When urgent, state the operational requirement clearly (see communication
rules in `memory/procedures/interwork_communication_rules.md` for general tone).

**Do not state that a deadline is guaranteed unless Sunset confirms it.**

---

## People to Copy

Commonly copied: InterWork Operations, Francisco Vinueza, the assigned InterWork
project manager, relevant Sunset tracking addresses (e.g. `TrackingMN@sunsettrans.com`
if already on the thread). **Do not automatically copy every person from an older
thread** — copy only who's relevant to the current project.

---

## What Claude Must Not Do

- Invent a project number, truck requirement, weight, or cubic footage.
- Assume Sunset performs loading labor or installation.
- Treat a quote as a booking, or booking approval as pickup completion.
- Treat a scheduled ETA as actual delivery.
- Promise exact LTL timing, or state freight fits a truck without support.
- Use an old pickup/delivery address without confirming it.
- Remove Sunset tracking contacts from an active thread without reason.
- Tell the client Sunset is being used, unless operationally necessary.

---

## Internal Recordkeeping

For each Sunset shipment, help maintain: project number, Sunset order number, Sunset
contact, service type, equipment type, quoted amount, approval date, pickup date,
delivery date, pickup/delivery contacts, BOL status, driver status, final delivery
confirmation, and any delays/exceptions.

---

## Standard Templates

**Quote request**
```
Subject: Project [number] | [Origin City] to [Destination City] | Transport Quote

Hi [Peter/Krista/Marcus],

Could you please provide pricing and availability for the following shipment?

Project: [number]
Requested service: [cargo van / dedicated 26-foot box truck / 53-foot dry van / LTL]

Pickup:
[Company or site name]
[Full address]
Contact: [name and phone]

Delivery:
[Company or site name]
[Full address]
Contact: [name and phone]

Requested pickup: [date and time]
Requested delivery: [date, window, or deadline]

Freight:
[Inventory, volume, pallet count, weight, and packing condition]

Site requirements:
[Dock, liftgate, pallet jack, appointment, access hours]

Please confirm availability, estimated transit time, equipment type, and pricing.

Thank you,
```

**Booking approval**
```
Hi [name],

Please proceed with the booking at the quoted cost of $[amount].
Please send the Sunset order number, BOL, pickup ETA, and driver information when available.

Thank you,
```

**Pickup-status request**
```
Hi [name],

Could you please provide an update on Sunset Order [number]?
The shipment is scheduled for pickup today. Please confirm:
- Driver assignment
- Current pickup ETA
- Whether the pickup remains on schedule

Thank you,
```

**Delivery-status request**
```
Hi [name],

Could you please provide an update on Sunset Order [number]?
The scheduled delivery window was [time], and the shipment has not arrived. Please provide the driver's current status and updated delivery ETA.

Thank you,
```

**LTL rollover confirmation**
```
Hi Krista,

Please confirm whether the LTL driver is still expected to complete the pickup today. If not, please confirm that the shipment is scheduled to roll to tomorrow and provide the expected pickup window when available.

Thank you,
```

**Signed BOL return**
```
Hi [name],

Attached is the signed BOL for Sunset Order [number].
The driver departed before we were able to provide the document onsite, so I am sending the signed copy electronically for your records.

Thank you,
```

---

## Core Decision Rule

When Alejandro asks Claude to contact Sunset, first determine which stage applies,
then draft for that specific stage without assuming later stages have occurred:

1. We need a quote.
2. We received a quote and need to approve or decline it.
3. The shipment is booked and needs pickup coordination.
4. The freight was picked up and needs tracking.
5. The shipment is late and needs escalation.
6. Delivery is complete and documentation needs to be closed out.

All drafted messages go through the standard approval gate — see
`memory/procedures/interwork_communication_rules.md` (draft first, surface to
Alejandro, wait for explicit "send it").
