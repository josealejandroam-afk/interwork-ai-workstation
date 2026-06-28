# Project Status Confirmation Drafts
**Date:** 2026-06-28  
**Mode:** Drafts only — nothing sent, nothing written to Supabase  
**Purpose:** Give Alejandro ready-to-use or easy-to-adapt outreach for confirming project completion status before any database writes occur.

> **DO NOT UPDATE SUPABASE until confirmations are received.**  
> See `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` for the exact write sequence and rollback plan.

---

## Project 7060 — MMC Dallas Walnut Hill to Galleria Relocation & Decommission

### Background (for Alejandro's reference)
- DB shows `status = in_progress`, last updated **Apr 3** (Phase 0 launch day only).
- Scheduled end: **Apr 30, 2026** — 59 days ago.
- Phases 1–4 have no DB updates. `fastfield_submitted = false`. `actual_end_at = NULL`.
- Need to confirm: phases executed, FastField status, actual close date.
- PM on record: **Frank Barrett**. Vendor: **Sergio Rios / Exserv**.

---

### Internal Note (Alejandro's own reference — not for sending)

```
PROJECT 7060 STATUS CHECK — FOR MY RECORDS

Questions to answer before I ask Claude to update the DB:

1. Were Phases 2–4 executed as planned?
   - Phase 2 (Apr 7–9): IT install at Galleria Floors 11–14
   - Phase 3 (Apr 11–29): Walnut Hill Floors 15–18 decom
   - Phase 4 (Apr 30): Final punch/closeout

2. Was FastField submitted for this project?
   - DB shows fastfield_submitted = false
   - If submitted under a different entry or project number, note which one

3. What is the actual completion date?
   - Expected: on or around Apr 30
   - If Phase 4 ran late, note the actual date

4. Were the Finance Group move date and docking station delivery resolved?
   - These were open as of Apr 3

5. Is there anything still genuinely open, or is this project fully closed?

Once I answer these, I tell Claude to run the write with my approval.
```

---

### Teams-Style Message (to Frank Barrett)

```
Hey Frank — quick records check on the MMC Dallas project (7060, Walnut Hill → Galleria).

Our system still shows it as in-progress from Apr 3. Can you confirm:
1. Did Phases 2–4 run as planned through Apr 30?
2. Was a FastField submitted — if so, under what entry?
3. Any open items still outstanding, or is this fully closed?

No rush — just need this before I update the record. Thanks
```

---

### Email-Style Draft (to Frank Barrett, cc Alejandro)

```
Subject: Project 7060 — MMC Dallas Status Confirmation

Hi Frank,

Hope you're well. I'm doing a quick records cleanup and need your help confirming the status of project 7060 (MMC Dallas — Walnut Hill to Galleria Relocation & Decommission).

Our system shows the project as "in progress" with a last update date of April 3. The scheduled completion was April 30. A few quick questions:

1. Were Phases 2 through 4 completed as planned?
   - Phase 2: IT install at Galleria Floors 11–14 (Apr 7–9)
   - Phase 3: Walnut Hill Floors 15–18 decommission (Apr 11–29)
   - Phase 4: Final punch/closeout (Apr 30)

2. Was a FastField form submitted for this project? Our system doesn't show one linked — if it was submitted under a different entry, can you let me know the reference?

3. What was the actual completion date? If Phase 4 ran a day or two late, that's fine — I just need the real date for the record.

4. Were there any items still open at close — specifically the Finance Group move and the docking station delivery?

Once I hear back from you I'll get the record updated. Thanks in advance.

[Alejandro]
```

---

## Project 7348 — Amtrust Cleveland (location on record: Princeton NJ)

### Background (for Alejandro's reference)
- DB shows `status = in_progress`, last updated **Apr 17** (2 days after the job).
- Scheduled date: **Apr 15, 2026** — 74 days ago.
- `fastfield_submitted = true` — strongest completion signal.
- **Data flag:** Project named "Amtrust Cleveland" but location recorded as **116 Village Blvd, Suite 303, Princeton NJ**. Must resolve before write.
- PM on record: **Pedro Martinez**.

---

### Internal Note (Alejandro's own reference — not for sending)

```
PROJECT 7348 STATUS CHECK — FOR MY RECORDS

Questions to answer before I ask Claude to update the DB:

1. Is this the Princeton NJ job, not Cleveland?
   - DB location: 116 Village Blvd, Suite 303, Princeton NJ
   - Project name says "Amtrust Cleveland"
   - Is "Cleveland" the Amtrust account/division name, or was the city entered wrong?

2. Was the Apr 15 visit completed?
   - Scope: punch list, furniture, artwork, electrical
   - Pedro Martinez PM
   - DB shows fastfield_submitted = true — does this confirm the job is done?

3. What is the actual completion date?
   - Expected: Apr 15 or Apr 16
   - DB was touched Apr 17 but status was never advanced

4. Is there a separate project for a Cleveland OH Amtrust location,
   or is this the only Amtrust project from that period?

Once I answer these, I tell Claude to run the write with my approval.
```

---

### Teams-Style Message (to Pedro Martinez)

```
Hey Pedro — quick records check on project 7348, Amtrust, Apr 15.

Our DB has it listed as "Amtrust Cleveland" but the address is Princeton NJ — can you confirm that's the right location? Also still showing as in-progress. FastField shows submitted, so I'm guessing the job is done?

Just need:
1. Princeton NJ confirmed (or correct location if wrong)
2. Confirm Apr 15 visit completed with no open items
3. Actual close date if different from Apr 15

Thanks
```

---

### Email-Style Draft (to Pedro Martinez, cc Alejandro)

```
Subject: Project 7348 — Amtrust Status Confirmation + Location Check

Hi Pedro,

Doing a quick records cleanup on project 7348 (Amtrust, Apr 15). A couple of things I need your help with before I update the record:

1. Location clarification — the project is listed as "Amtrust Cleveland" but the address on file is 116 Village Blvd, Suite 303, Princeton NJ. Can you confirm whether the Apr 15 work was in Princeton NJ? If the city in the name is wrong I'll correct it.

2. Job completion — our system shows FastField as submitted, which I'm taking as a good sign. Can you confirm the Apr 15 visit is fully closed with no outstanding punch items?

3. Actual close date — was everything wrapped up Apr 15, or did it run into Apr 16?

Once I hear from you I'll close the record out. Thanks.

[Alejandro]
```

---

## Fields Pending Confirmation (do not write until approved)

### Project 7060
| Field | Current | Will change to | Requires |
|-------|---------|---------------|----------|
| `status` | `in_progress` | `completed` | Frank/Alejandro confirm all phases done |
| `actual_end_at` | NULL | Confirmed close date | Frank/Alejandro provide date |
| `fastfield_submitted` | false | true | Only if FastField submission confirmed |
| `completion_report_sent` | false | true | Only if report was actually sent |
| `ai_summary` | Phase 2 in progress (Apr 3) | Updated close summary | After status confirmed |

### Project 7348
| Field | Current | Will change to | Requires |
|-------|---------|---------------|----------|
| `status` | `in_progress` | `completed` | Pedro/Alejandro confirm Apr 15 job done |
| `actual_end_at` | NULL | Apr 15 or 16 (confirmed) | Pedro/Alejandro provide date |
| `location_city` | Princeton | Cleveland (if name is right) OR keep Princeton (if name is wrong) | Location clarification |
| `completion_report_sent` | false | true | Only if report was actually sent |

---

## Rollback Reminder

If any write is made in error, the rollback SQLs are:

```sql
-- 7060 rollback
UPDATE public.projects
SET status = 'in_progress',
    actual_end_at = NULL,
    fastfield_submitted = false,
    completion_report_sent = false
WHERE project_number = '7060';

-- 7348 rollback
UPDATE public.projects
SET status = 'in_progress',
    actual_end_at = NULL,
    completion_report_sent = false
WHERE project_number = '7348';
```

> Rollback requires Alejandro approval. Claude does not self-rollback.  
> Full procedure in `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`.

---

*Drafts only. Nothing sent. Nothing written to Supabase.*
