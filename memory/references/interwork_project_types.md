---
name: interwork-project-types
description: "Common InterWork project types — required information, typical risks, and completion signals for each type"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Project Types
_Last updated: 2026-06-26_

---

## How to Use This File

When reviewing a project, match it to a type below to identify:
- What information should already be confirmed
- What fields to flag as missing
- What risks to surface
- What completion evidence to expect

Project names often include the type (Decom, Move, Install, Delivery, Walkthrough, etc.).
Use this as a checklist for `/project-brief` and `/completion-intake`.

---

## Decommission

**Description:** Remove, dispose, donate, or relocate all furniture and equipment from a site.

**Required information:**
- Full address (street, floor, suite)
- Scope: what items are being decommissioned (furniture, electronics, fixtures)
- Disposal plan: trash, recycling, donation, warehouse, liquidation
- e-waste requirements and vendor
- Building access: loading dock, freight elevator, after-hours restrictions, COI needed
- Client POC (on-site contact name and phone)
- PM/vendor crew size and truck type
- Schedule: start date, duration estimate
- Photos required: before, during, after

**Completion signals:**
- FastField submitted with site-clear confirmation
- WC report sent
- Photos received showing empty space
- Client confirmation of completion

**Typical risks:**
- Scope unclear (client adds items day-of)
- Building restrictions discovered on arrival
- After-hours work required but not arranged
- Vendor disposal mistakes (wrong items removed, improper e-waste handling)
- Missing photos/evidence
- Punch items discovered post-completion
- COI not obtained in time

---

## Move / Relocation

**Description:** Move furniture, equipment, or personnel belongings from one location to another.

**Required information:**
- Origin address (with floor, suite, dock/elevator access)
- Destination address (with floor, suite, dock/elevator access)
- Inventory list or item count
- Packing needs (client packing or vendor packing)
- Crates, dollies, or specialty equipment needed
- Elevator/dock/access timing at both ends
- PM assigned
- Crew size and truck type
- Schedule (date, arrival time, estimated duration)
- Client POC at origin and destination
- IT coordination if computers or servers are included

**Completion signals:**
- FastField submitted
- All items confirmed at destination
- Client sign-off
- WC report sent

**Typical risks:**
- Wrong items moved or left behind
- Inventory not confirmed before move day
- Client not packed on arrival
- Elevator access window missed
- Vendor crew size mismatch with scope
- Damage not documented

---

## Internal Relocation

**Description:** Move people, workstations, or belongings within the same building or campus.

**Required information:**
- From location (floor, suite, room/desk labels)
- To location (floor, suite, room/desk labels)
- Item list or headcount
- Access to both areas on move day
- PM assigned
- Schedule
- Client POC
- Floor plan if available (especially for large restacks)

**Completion signals:**
- FastField submitted
- Client confirmation of completion
- Post-move check by PM

**Typical risks:**
- Room or desk labels unclear or unlabeled
- Occupied spaces during move
- Scope creep (items added day-of)
- No post-move verification
- IT equipment moved without IT sign-off

---

## Installation

**Description:** Install furniture, fixtures, or equipment at a client site.

**Required information:**
- Full install scope (what is being installed, quantities)
- Product/materials confirmed received or ETA
- Drawings or floor plans provided
- Delivery status of materials before install date
- Site access (dock, elevator, parking)
- PM/crew assigned
- Tools and equipment needed
- Punch list process (who reviews, what standard)
- Client POC on-site

**Completion signals:**
- FastField submitted
- Punch list cleared or documented
- Client sign-off
- WC report sent
- Photos of completed install

**Typical risks:**
- Missing or damaged parts (no replacement lead time)
- Product delayed to site
- Field measurements differ from drawings
- Building access issues on install day
- Client expectations exceed approved scope
- Punch list not formally closed

---

## Delivery

**Description:** Deliver furniture, equipment, or materials to a client site without full installation.

**Required information:**
- Pickup address (warehouse, vendor, or supplier)
- Delivery address (full address, floor, dock/liftgate needs)
- Item list with quantities
- Truck type and liftgate requirement
- POC at pickup and delivery locations
- Date and time window
- Special handling requirements

**Completion signals:**
- Signed delivery confirmation (BOL or POD)
- FastField or photo evidence
- Client confirmation of receipt

**Typical risks:**
- Wrong item count or missing items
- Dock or liftgate mismatch
- Driver contact missing or unreachable
- Damage not documented with photos
- No delivery confirmation obtained

---

## Walkthrough / Assessment

**Description:** On-site visit to assess scope, verify conditions, take measurements, or prepare for a future project.

**Required information:**
- Site address (full, with floor/suite)
- Client POC (on-site contact name and phone)
- Date and arrival time
- Purpose of walkthrough (scope assessment, punch list check, post-project verification)
- What to verify or measure on-site
- Photos needed (yes/no, what to capture)
- Questions to answer during the visit
- PM assigned

**Completion signals:**
- Walkthrough notes written and saved to memory
- Photos received or documented
- Follow-up scope or open loops created
- FastField submitted if applicable

**Typical risks:**
- No follow-up notes or memory save after visit
- Project number missing (cannot link walkthrough to a Supabase record)
- Scope ambiguous after visit (no clear next action)
- Photos not taken or not shared
- Measurements missing

---

## Punchlist / Service Call

**Description:** Return visit to correct specific items, complete unfinished work, or respond to a client issue.

**Required information:**
- Itemized punch list (specific items by location/room)
- Photos of each punch item
- Parts or materials needed for correction
- PM/technician assigned
- Client POC
- Date and arrival time
- Approval scope: what is InterWork responsible for vs. out of scope

**Completion signals:**
- FastField submitted for each item resolved
- Photos of corrected items
- Client sign-off on punch list completion
- No remaining open items

**Typical risks:**
- Incomplete or vague punch list (items added day-of)
- Parts not available on arrival
- Unclear ownership of items (InterWork vs. client vs. vendor)
- Client expects more than approved scope
- No completion evidence obtained

---

## Storage / Return Shipment

**Description:** Retrieve items from storage, return items to client, or ship items to a new location.

**Required information:**
- Items in storage (description, quantity, location in warehouse)
- Pickup address (warehouse location and contact)
- Delivery address
- Item ownership (client-owned vs. InterWork-held)
- Bill of Lading (BOL) if needed
- Truck type and equipment
- Pickup/delivery POC
- Date and time

**Completion signals:**
- Delivery confirmation (BOL, POD, or signed receipt)
- Photos of items loaded and delivered
- Client confirmation of receipt

**Typical risks:**
- Wrong items pulled from storage
- Missing or unreadable labels
- Client and vendor warehouse confusion (wrong address)
- No return confirmation or signature obtained
- Item condition not documented before shipment

---

## Project Type Flags for Claude

When reviewing a project, use the project name to detect type:
- Contains "Decom" → Decommission checklist
- Contains "Move" or "Relocation" → Move checklist
- Contains "Install" → Installation checklist
- Contains "Delivery" → Delivery checklist
- Contains "Walkthrough" or "Assessment" → Walkthrough checklist
- Contains "Punch" or "Service Call" → Punchlist checklist
- Contains "Storage" or "Shipment" → Storage checklist

For completion backlog reviews, match type to expected completion signals.
Multi-phase projects (Phase 2, Punch List + Move, etc.) may span multiple types.
