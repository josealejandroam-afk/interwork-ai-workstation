---
project_number: "7579"
name: "JPMC Miami - Vecos SMART Locker Commissioning - 33rd Floor"
client: "Vecos USA"
status: pending_scheduling
office_pm: "Francisco Vinueza"
field_pm: UNASSIGNED
scheduled_date: UNCONFIRMED
origin: "N/A - commissioning only"
destination: "1450 Brickell Ave, Miami FL 33131 - 33rd Floor"
last_updated: "2026-06-30"
source: "ChatGPT handoff from email review"
supabase_status: "NOT IN DATABASE - record needs to be created"
---

# Project 7579 - JPMC Miami / Vecos SMART Lockers

> **STATUS: PENDING SCHEDULING**
> No execution date confirmed. No technician assigned.
> Do not generate execution documents until scheduling is confirmed by Vecos.

---

## Quote / Pricing (final, do not modify without new client direction)

| Item | Amount |
|---|---|
| Quote number | 8520 |
| Labor | $2,855.00 |
| Project Management | $150.00 |
| Total | $3,215.35 |

Quote prepared by Jill Buchman. Already sent to client.

---

## Client

| Field | Value |
|---|---|
| Client | Vecos USA |
| Primary contact | Cason Perez |
| Email | Cason.Perez@vecos.com |
| Phone | 832-993-6902 |

---

## Project Location

| Field | Value |
|---|---|
| Address | 1450 Brickell Ave, Miami, FL 33131 |
| Work area | 33rd Floor |
| Site contact | Cesar Rivera |
| Site contact phone | 347-258-2897 |

---

## Project Management

| Role | Name |
|---|---|
| Office PM | Francisco Vinueza |
| Field technician | UNASSIGNED -- awaiting scheduling confirmation |

---

## Scope of Work

Commission approximately:
- (75) Vecos lockers
- (3) Vecos terminals

Commissioning tasks:
- Install required cabling, hardware, software, and terminals
- Physical inspection of all lock system installations
- Functional lock testing
- Verify network patching and connectivity
- Troubleshooting with Vecos PM
- Replace defective manufacturer components if applicable
- Enter and activate license keys
- Verify configuration and settings
- Document issues discovered during commissioning

Required tools:
- Screwdriver
- Wrench
- 7 mm socket
- Ladder (wiring above lockers -- confirm whether ladder is provided onsite)

---

## Technical Details

License groups:
- 33.001 to 33.023
- 33.024 to 33.034
- 33.035 to 33.051

Field team tasks:
- Enter Primary LBC IP
- Enter Secondary LBC IP
- Coordinate firmware push with Vecos PM

These items belong in the FastField technician instructions once scheduling is confirmed.

---

## Scheduling Status

**No execution date confirmed.**

Last communication from Vecos: "Mobilization sometime next week if possible."

| Field | Status |
|---|---|
| Execution date | NOT CONFIRMED |
| Start time | NOT CONFIRMED |
| Technician | NOT ASSIGNED |
| Building access instructions | MISSING |
| Parking / loading instructions | MISSING |
| Ladder provided onsite | UNKNOWN |
| Final license / IP package | PENDING (may be updated) |

---

## Documents Status

| Document | Status |
|---|---|
| Quote (8520) | Sent to client |
| Project memory card (this file) | Created 2026-06-30 |
| Technician FastField | NOT YET -- needs scheduling confirmation + technician assignment |
| Teams notification | NOT YET -- needs scheduling confirmation |
| Client confirmation email | NOT YET -- needs scheduling confirmation |
| Calendar entry | NOT YET -- no date to enter |
| Work completion report | NOT YET -- project not started |
| Completion email | NOT YET |

---

## Execution Document Trigger Checklist

Do not create execution documents until ALL of these are confirmed:

- [ ] Execution date confirmed by Vecos
- [ ] Start time confirmed
- [ ] Technician assigned (required before FastField and Teams dispatch)
- [ ] Building access instructions received
- [ ] Parking / loading instructions received
- [ ] Site POC confirmed for execution day
- [ ] Ladder availability confirmed (onsite or bring own)
- [ ] Any updated license / IP information received (or confirmed unchanged)

FastField and Teams dispatch require technician assignment in addition to date + time.
Calendar entry requires date only.

When all boxes are checked, say: **"Create 7579 execution package"**

---

## Supabase Note

Project 7579 is NOT in the Supabase database as of 2026-06-30.

A new INSERT record will need to be created (not a PATCH).
Draft record for Alejandro approval when ready:

```
project_number:   '7579'
name:             'JPMC Miami - Vecos SMART Locker Commissioning'
client:           Vecos USA (client_id needed)
status:           'scheduled' (when date confirmed) or 'pending' now
location_address: '1450 Brickell Ave'
location_city:    'Miami'
location_state:   'FL'
location_zip:     '33131'
pm_id:            Francisco Vinueza (pm_id needed)
scope_summary:    'Vecos SMART locker commissioning - 75 lockers, 3 terminals, 33rd floor'
quote_amount:     3215.35
vendor_required:  false
```

Trigger phrase: "create 7579 in Supabase"

---

## Standard Vecos Closeout Deliverables

These apply to every Vecos commissioning project. Generate each in order once scheduling is confirmed and technician is assigned:

1. Technician FastField (requires: date, start time, technician, building access, license/IP package)
2. Teams dispatch to technician (requires: date, start time, technician assigned)
3. Client confirmation email to Vecos contact (requires: date, start time, technician name + phone)
4. Calendar entry (requires: date only)
5. Work Completion Report (after execution)
6. Completion email to client with attached WCR

---

## Constraints (from InterWork standards)

- Do not invent execution dates
- Do not invent technician names
- Do not assume the project has started
- Do not modify pricing without new client direction
- Do not assume additional lockers, floors, or visits beyond confirmed scope
- Do not expose internal vendor relationships to the client
- Do not generate calendar entries with placeholder dates as actual scheduled events
- Include technician phone number in client notifications after assignment
