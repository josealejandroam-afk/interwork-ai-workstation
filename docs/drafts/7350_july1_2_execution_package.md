# Project 7350 - July 1-2 Execution Package
_Status: DRAFT - all items below require Alejandro review before use_
_Created: 2026-06-30_

---

## 1. FastField - Pedro Martinez (July 1-2)

Use the following information to complete the FastField form for the July 1 execution day.
A separate FastField entry may be needed for July 2 if that is standard practice.

---

**FastField Entry - July 1**

Project Number: 7350
Client: Bentley Systems
Date: July 1, 2026
PM: Pedro Martinez

Origin Address:
601 Walnut Street
Curtis Building (Cesium)
Philadelphia, PA

Scope (July 1):
- Protect common areas
- Disassemble (12) height-adjustable desks
- Disassemble (3) height-adjustable hoteling stations
- Remove (16) monitor arms
- Pack and protect furniture
- Pack IT equipment: (1) Aruba Switch, (1) Palo Alto 440 Firewall, (8) Aruba Wireless Access Points
- Label all components
- Load and secure trucks
- Transport to 685 Stockton Drive, Exton, PA

Special notes:
- (1) Teknion Media Cart - protect and load
- All IT equipment must be individually labeled before loading
- Confirm onsite contact at origin on arrival

---

**FastField Entry - July 2**

Project Number: 7350
Client: Bentley Systems
Date: July 2, 2026
PM: Pedro Martinez

Destination Address:
685 Stockton Drive
Exton, PA

Scope (July 2):
- Offload all furniture
- Install (12) height-adjustable desks
- Install (3) height-adjustable hoteling stations
- Install (16) monitor arms
- Reassemble all desk components
- Stage IT equipment: (1) Aruba Switch, (1) Palo Alto 440 Firewall, (8) Aruba Wireless Access Points
- Position (1) Teknion Media Cart per client direction
- Remove all packing materials
- Final walkthrough with onsite contact
- Obtain client sign-off

---

## 2. Teams Notification - Pedro Martinez

_DRAFT - do not send without Alejandro approval ("send it")_

---

Hi Pedro,

You are confirmed as the PM for Bentley Systems Project 7350.

Execution dates: July 1 and July 2, 2026.

July 1 - Pack and load at 601 Walnut Street, Curtis Building (Cesium), Philadelphia, PA.
July 2 - Offload and install at 685 Stockton Drive, Exton, PA.

Confirmed inventory:
- (12) HA Desks
- (3) HA Hoteling Stations
- (16) Monitor Arms
- (1) Teknion Media Cart
- (1) Aruba Switch
- (1) Palo Alto 440 Firewall
- (8) Aruba Wireless Access Points

Known onsite contacts:
- Philadelphia: Marlies Duncan (phone pending) / Mark Giorgio - IT (phone pending)
- Exton: TBD (phone pending)

We are requesting the missing phone numbers from the client now. I will forward them as soon as we receive them.

Please confirm receipt.

Francisco Vinueza will be available for any questions before execution.

---

## 3. Client Email - Confirm PM, Dates, Request Missing Phones

_DRAFT - do not send without Alejandro approval ("send it")_
_Send to: Meg Craig (267-481-1782) and/or Cathy Zaharko (412-508-5291)_
_Confirm which contact receives this before sending_

---

Subject: Bentley Systems - Move Confirmation and Onsite Contact Information Request

Hi Meg / Cathy,

I want to confirm the upcoming move schedule for Bentley Systems and request a few contact details before we begin.

Confirmed schedule:

July 1, 2026 - Our team will be at 601 Walnut Street (Curtis Building) in Philadelphia to pack and load the furniture and IT equipment.

July 2, 2026 - Our team will be at 685 Stockton Drive in Exton to offload and install.

Our project manager for both days will be Pedro Martinez. He can be reached at 732-421-1470.

To finalize our preparation, we need the following:

1. Onsite contact name and phone number for July 1 at the Philadelphia location (601 Walnut Street).
2. Onsite contact name and phone number for July 2 at the Exton location (685 Stockton Drive).

We have Marlies Duncan and Mark Giorgio on file as Philadelphia contacts. If either of them is the onsite contact for July 1, please send us a phone number where they can be reached that day.

For Exton, please send us the name and number of whoever will be available to receive us on July 2.

Please let us know if anything has changed with the scope or schedule.

Thank you,

Alejandro Acosta
InterWork Office
[phone]

---

## 4. Calendar Entry

_Information for whoever creates the calendar entry_

**Title:** 7350 Bentley Systems - Pack/Load (Philadelphia)
**Date:** July 1, 2026
**Location:** 601 Walnut Street, Curtis Building (Cesium), Philadelphia, PA
**Notes:** Field PM: Pedro Martinez 732-421-1470. Origin move day. Inventory: 12 HA desks, 3 hoteling stations, 16 monitor arms, 1 media cart, IT equipment.

---

**Title:** 7350 Bentley Systems - Offload/Install (Exton)
**Date:** July 2, 2026
**Location:** 685 Stockton Drive, Exton, PA
**Notes:** Field PM: Pedro Martinez 732-421-1470. Destination install day. Same inventory.

---

## 5. Pending Supabase Updates (do not apply without Alejandro approval)

### Safe to update (dates + address only)

These fields are stale and safe to correct. They do not touch PM or personnel fields.

```sql
UPDATE projects
SET
  scheduled_date     = '2026-07-01',
  scheduled_end_date = '2026-07-02',
  location_address   = '601 Walnut Street / 685 Stockton Drive'
WHERE project_number = '7350';
```

Trigger phrase to apply: "update 7350 dates and address"

---

### Do NOT update yet - needs verification

| Field | Current | Why holding |
|---|---|---|
| pm_id / Office Assignee | Hunter Barbieri in internal_notes | Hunter may legitimately own the project administratively even if Francisco is Office PM. Verify before changing. |
| ai_summary PM name | "Juan Martinez" | Field may reflect overall project history, not July execution only. May need Francisco + Pedro both documented rather than one overwriting the other. |

These fields will be updated separately once the field purpose is confirmed.

Trigger phrase when ready: "update 7350 PM fields in Supabase"

---

## Consistency Check

The following was verified against the handoff before generating this package:

| Check | Result |
|---|---|
| Inventory source | Latest confirmed by Jill Buchman only - earlier large quantities not used |
| PM assignment | Pedro Martinez confirmed - not changed |
| Dates | July 1-2 only - May dates not used |
| Origin | 601 Walnut Street (Cesium/Curtis) - not 1601 Cherry or old Exton address |
| Client contacts | Only confirmed names used - no phones invented |
| Exton contact | Not invented - flagged as missing |
| Arrival times | Not stated - not invented |
| Labor count | Not stated - not invented |
| Truck count | Not stated - not invented |
| Vendor information | Not disclosed in any client-facing draft |
