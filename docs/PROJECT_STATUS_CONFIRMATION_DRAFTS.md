# Project Status Confirmation Drafts
**Date:** 2026-06-28
**Revised:** 2026-06-28 (Codex safety review applied)
**Mode:** Drafts only — nothing sent, nothing written to Supabase
**Purpose:** Give Alejandro ready-to-use or easy-to-adapt outreach for confirming project completion status before any database writes occur.

> **DO NOT UPDATE SUPABASE until confirmations are received and each field change is individually approved.**
> See `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` for the full write procedure, field-by-field approval sequence, and rollback plan.

> **Contact details** (phone numbers, email addresses) are intentionally omitted from this file. Use Outlook, Teams, or local contact records to reach the relevant parties.

---

## Project 7060 — MMC Dallas Walnut Hill to Galleria Relocation & Decommission

### Background (for Alejandro's reference)
- DB shows `status = in_progress`, last updated **Apr 3** (Phase 0 launch day only).
- Scheduled end: **Apr 30, 2026** — 59 days ago.
- Phases 2–4 have no DB record of execution. `fastfield_submitted = false`. `actual_end_at = NULL`.
- PM on record: **Frank Barrett**. Vendor: **Exserv Facility Services** (Sergio Rios, field lead).

---

### Internal Note (Alejandro's own reference — not for sending)

```
PROJECT 7060 STATUS CHECK — FOR MY RECORDS

Before asking Claude to write anything, I need answers to all of these:

FIELD COMPLETION (on-site work):
  1. Were Phases 2–4 executed as planned?
     - Phase 2 (Apr 7–9): IT install at Galleria Floors 11–14
     - Phase 3 (Apr 11–29): Walnut Hill Floors 15–18 decom
     - Phase 4 (Apr 30): Final punch/closeout
  2. What is the actual date the on-site work was physically finished?
     Time and timezone helpful but not required if unknown.

ADMINISTRATIVE CLOSURE (separate question from field work):
  3. Was a completion report sent to the client? If yes, on what date?
  4. Has this project been invoiced?
  5. Were the Finance Group move and docking station delivery resolved,
     or are those threads still open under a different tracking entry?

FASTFIELD:
  6. Was a FastField form submitted for this project?
     If yes: what is the submission reference or project number it was logged under?
     If no: confirm whether a FastField submission was required for this project type.

WHAT STAYS OPEN:
  7. Are there any remaining on-site, administrative, or billing items
     that would prevent marking this project as fully closed?

Note: The Brent Lee contact phone discrepancy is a separate records task —
it does not block project closure and should be addressed independently.

I will review the answers, then request specific field-by-field approval
for any database updates.
```

---

### Teams-Style Message (to Frank Barrett)

```
Hey Frank — doing a records check on project 7060 (MMC Dallas, Walnut Hill → Galleria).

Our system still shows it as in-progress from Apr 3 — nothing logged after that.
A few things I need to confirm:

1. Did Phases 2–4 run as planned through Apr 30?
   (Phase 2 IT install, Phase 3 Walnut Hill decom, Phase 4 punch/closeout)

2. What's the actual date the on-site work finished?

3. Was a FastField submitted? If yes, under what entry or reference?

4. Any admin items still open — completion report, invoice, outstanding threads
   on the Finance Group move or docking station delivery?

No rush, but want to make sure the record is accurate before anything gets updated.
Thanks
```

---

### Email-Style Draft (to Frank Barrett)

```
Subject: Project 7060 — MMC Dallas Status Confirmation

Hi Frank,

I'm doing a records review and project 7060 (MMC Dallas — Walnut Hill to Galleria
Relocation & Decommission) still shows as "in progress" in our system with no updates
after April 3. The project was scheduled to close April 30, so I want to make sure
we have an accurate record before making any changes.

A few questions — on-site work and admin are separate:

ON-SITE / FIELD WORK:
1. Were Phases 2 through 4 completed as planned?
   - Phase 2: IT install at Galleria Floors 11–14 (Apr 7–9)
   - Phase 3: Walnut Hill Floors 15–18 decommission (Apr 11–29)
   - Phase 4: Final punch/closeout (Apr 30)
2. What was the actual date the on-site work finished?

FASTFIELD:
3. Was a FastField form submitted for this project? Our system shows none linked.
   If one was submitted under a different entry or reference, can you share the ID?

ADMINISTRATIVE:
4. Was a completion report sent to the client? If yes, approximate date?
5. Any remaining open items — Finance Group move, docking station delivery,
   or anything else that would keep this from being fully closed?

Once I have your answers I'll review the evidence and request approval for any
appropriate record update.

Thanks,
[Alejandro]
```

---

## Project 7348 — Amtrust (record name: "Amtrust Cleveland" / location: Princeton NJ)

### Background (for Alejandro's reference)
- DB shows `status = in_progress`, last updated **Apr 17** (2 days after the scheduled job).
- Scheduled date: **Apr 15, 2026** — 74 days ago.
- `fastfield_submitted = true` in DB — but the specific submission has not been verified.
- **Data flag:** Project named "Amtrust Cleveland" but location recorded as Princeton NJ.
  The authoritative record must be identified before any location field is changed.
- PM on record: **Pedro Martinez**.

---

### Internal Note (Alejandro's own reference — not for sending)

```
PROJECT 7348 STATUS CHECK — FOR MY RECORDS

Before asking Claude to write anything, I need answers to all of these:

NAME / LOCATION:
  1. Is "Amtrust Cleveland" the correct project name, or is "Cleveland" the
     Amtrust account/division name (not the city)?
  2. Was the Apr 15 work actually performed at the Princeton NJ address on file?
  3. Is there a separate Amtrust project for a Cleveland OH location?
     If so, what is its project number?
  Clarification needed before any location field is changed — do not correct
  until the authoritative record is identified.

FIELD COMPLETION:
  4. Was the Apr 15 visit completed on-site with no open punch items?
  5. What is the actual date the job closed — Apr 15 or Apr 16?

FASTFIELD:
  6. DB shows fastfield_submitted = true.
     What is the FastField submission reference number or project ID?
     Which project address or name does the submission list?
     This must be confirmed — not assumed from the DB flag alone.

ADMINISTRATIVE CLOSURE (separate question):
  7. Was a completion report sent to the client?
  8. Has this project been invoiced?
  9. Any remaining open items?

I will review the answers, then request specific field-by-field approval
for any database updates. "Completed" for DB purposes means both fieldwork
and administrative closure are either done or explicitly deferred with
Alejandro's knowledge.
```

---

### Teams-Style Message (to Pedro Martinez)

```
Hey Pedro — quick records check on project 7348, Amtrust, Apr 15.

Two things I need to sort out before I can update the record:

1. The project is listed as "Amtrust Cleveland" but the address is Princeton NJ.
   Can you confirm: was the Apr 15 work in Princeton NJ?
   Is there a separate Cleveland project, or is the city in the name wrong?
   (I won't change the location in the record until I know which one is correct.)

2. DB shows FastField submitted — can you confirm the FastField submission
   reference or project number it was logged under, and that it matches
   the Princeton NJ address?

Also:
3. Was the Apr 15 visit fully completed with no open items?
4. Actual close date — Apr 15 or Apr 16?
5. Was a completion report sent? Has it been invoiced?

Once I have your answers I'll review the evidence and request approval for
any appropriate record update. Thanks
```

---

### Email-Style Draft (to Pedro Martinez)

```
Subject: Project 7348 — Amtrust Status Confirmation + Location Clarification

Hi Pedro,

I'm reviewing project 7348 (Amtrust, Apr 15) and have a few things I need
to clarify before making any record updates.

LOCATION CLARIFICATION:
1. The project is listed as "Amtrust Cleveland" but the address on file is in Princeton NJ.
   - Was the Apr 15 work performed at the Princeton NJ location?
   - Is "Cleveland" the Amtrust account or division name, or was the city entered in error?
   - Is there a separate Amtrust project covering a Cleveland OH location?
   I want to make sure I'm looking at the right authoritative record before
   changing anything.

FASTFIELD:
2. Our system shows FastField as submitted for this project. To verify:
   - What is the FastField submission reference number or project ID?
   - Does the submission reference the Princeton NJ address or another location?

FIELD COMPLETION:
3. Was the Apr 15 visit completed on-site with no remaining punch items?
4. What was the actual close date — April 15 or April 16?

ADMINISTRATIVE:
5. Was a completion report sent to the client? If yes, approximate date?
6. Has this project been invoiced?

Once I have your answers I'll review the evidence and request approval for
any appropriate record update. I won't change any fields — including the location —
until the authoritative record is confirmed.

Thanks,
[Alejandro]
```

---

## Fields Pending Confirmation (no writes until approved, field by field)

### Project 7060
| Field | Current | Under consideration | Evidence required |
|-------|---------|---------------------|------------------|
| `status` | `in_progress` | `completed` | Field + admin closure confirmed by Frank/Alejandro |
| `actual_end_at` | NULL | Confirmed date from PM | PM states exact date; time/tz if available |
| `fastfield_submitted` | false | true | FastField submission reference confirmed |
| `completion_report_sent` | false | true | Evidence report was actually sent |
| `invoiced` | false | true | Alejandro confirms invoice issued |
| `ai_summary` | Apr 3 in-progress entry | Versioned addition | Status confirmed — prior entry preserved |

### Project 7348
| Field | Current | Under consideration | Evidence required |
|-------|---------|---------------------|------------------|
| `status` | `in_progress` | `completed` | Field + admin closure confirmed by Pedro/Alejandro |
| `actual_end_at` | NULL | Confirmed date from PM | PM states Apr 15 or 16 |
| `fastfield_submitted` | true | (verify, not change) | Submission reference confirmed |
| `completion_report_sent` | false | true | Evidence report was actually sent |
| `invoiced` | false | true | Alejandro confirms invoice issued |
| `location_city` | Princeton | TBD | Authoritative record identified first |
| `ai_summary` | Apr 15 in-progress entry | Versioned addition | Status confirmed — prior entry preserved |

---

> **Rollback plan and full write procedure:** See `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`.
> Rollback targets are generated from the pre-write SELECT snapshot at write time — not from the values listed above.

---

*Drafts only. Nothing sent. Nothing written to Supabase.*
