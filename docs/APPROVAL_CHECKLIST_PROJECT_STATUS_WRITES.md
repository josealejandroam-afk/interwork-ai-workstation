# Approval Checklist — Project Status Writes
**Scope:** Projects 7060 and 7348 (template for all future project writes)
**Date created:** 2026-06-28
**Revised:** 2026-06-28 (Codex safety review applied)
**Rule:** No writes to Supabase without explicit Alejandro approval, field by field, project by project.

---

> **STOP. Read this before asking Claude to write anything.**
> This checklist exists because confirmation fields and status fields in the InterWork Command Center are partially unbackfilled. An incorrect status write can corrupt reporting, trigger automation, or create a false paper trail.
>
> **Git commit history is NOT a Supabase audit trail.** Only `activity_log` entries written inside the same transaction as the data change serve as an authoritative Supabase record.

---

## Required Write Procedure (applies to every project write)

All writes must follow this sequence exactly. No shortcuts.

### Step 1 — Pre-Write SELECT Snapshot
Before any UPDATE, Claude runs and Alejandro reads:

```sql
SELECT id, project_number, status, actual_end_at, fastfield_submitted,
       completion_report_sent, invoiced, ai_summary, updated_at
FROM public.projects
WHERE id = '<immutable-uuid>';
```

- **Use the immutable UUID (`id`), not `project_number` alone**, in all WHERE clauses.
- Alejandro reads and verbally confirms the snapshot matches what he expects.
- The snapshot values become the rollback targets — not assumed prior values.

### Step 2 — Exact Field-by-Field Proposal
Claude presents each proposed change as a separate line for separate approval:

```
Field:         status
Current value: in_progress
Proposed:      completed
Evidence:      [source of confirmation — PM name, date, form reference]
Approved?      [ ] YES / [ ] NO
```

Alejandro approves or rejects each field individually. Approval of one field does not imply approval of any other.

### Step 3 — Alejandro Reads the Full UPDATE SQL Before It Runs
Claude shows the exact SQL, including:
- WHERE clause using the UUID
- AND updated_at = '[snapshot value]' (concurrency guard — prevents overwriting a concurrent change)
- All fields being changed listed explicitly

Example structure (values filled only after confirmation):

```sql
BEGIN;

UPDATE public.projects
SET
    status          = '[approved value]',
    actual_end_at   = '[confirmed timestamp — date and time from PM, not assumed]',
    -- only fields explicitly approved above are included
    updated_at      = NOW()
WHERE id = '[immutable-uuid]'
  AND updated_at = '[snapshot updated_at value]';  -- concurrency guard

-- Assert exactly one row was affected before proceeding
-- (Claude checks rowcount; if 0 rows, ROLLBACK immediately)

INSERT INTO public.activity_log (project_id, actor, source, action, notes, created_at)
VALUES (
    '[immutable-uuid]',
    'alejandro',
    'manual',
    'status_write',
    '[brief description of what was confirmed and by whom]',
    NOW()
);

COMMIT;
```

Alejandro reads the full SQL and says "run it" explicitly.

### Step 4 — Row Count Assertion
Immediately after the UPDATE and before COMMIT, Claude checks that exactly one row was affected. If the row count is 0 (concurrency guard fired or UUID mismatch), Claude issues ROLLBACK immediately and reports the failure. No COMMIT on 0-row UPDATE.

### Step 5 — Post-Write Verification SELECT
After COMMIT, Claude runs:

```sql
SELECT id, project_number, status, actual_end_at, fastfield_submitted,
       completion_report_sent, invoiced, updated_at
FROM public.projects
WHERE id = '[immutable-uuid]';
```

Alejandro reads the result and confirms the fields changed as expected. If anything is wrong, the rollback procedure begins.

### Step 6 — Rollback (if needed)
Rollback targets come **only from the pre-write snapshot** captured in Step 1, not from assumed or remembered values.

```sql
BEGIN;

UPDATE public.projects
SET
    status          = '[snapshot value]',
    actual_end_at   = '[snapshot value]',
    -- restore all changed fields to snapshot values
    updated_at      = NOW()
WHERE id = '[immutable-uuid]';

INSERT INTO public.activity_log (project_id, actor, source, action, notes, created_at)
VALUES (
    '[immutable-uuid]',
    'alejandro',
    'manual',
    'rollback',
    'Rollback after write error — fields restored to pre-write snapshot.',
    NOW()
);

COMMIT;
```

Rollback requires Alejandro approval. Claude does not self-rollback.

---

## Timestamp Policy

- **No invented timestamps.** Claude never supplies a time like `17:00:00+00` or assumes a timezone.
- `actual_end_at` must come from one of: explicit PM confirmation, FastField submission metadata, or Alejandro stating the exact date and time he approves.
- If only a date is confirmed (not a time), the field is written as `'YYYY-MM-DD'::date` cast, or left NULL until the full timestamp is available.
- Alejandro explicitly approves the timestamp value before it is written.

---

## Field Independence Policy

Each field below is an independent evidence-based decision. Approving one does not imply approval of others.

| Field | What it means | Evidence required before write |
|-------|--------------|-------------------------------|
| `status` | Operational lifecycle state | PM or Alejandro explicit confirmation of fieldwork AND admin closure |
| `actual_end_at` | When work physically ended | Confirmed date (and time if available) from PM or field record |
| `fastfield_submitted` | Whether a FastField form was submitted | FastField submission reference/ID confirmed |
| `completion_report_sent` | Whether a completion report was sent to client | Evidence report was sent (email record, PM confirmation) |
| `invoiced` | Whether an invoice was issued | Alejandro confirms invoice was generated |
| `ai_summary` | Short operational summary | See ai_summary policy below |
| Location fields | Address, city, state | Authoritative project record identified; mismatch resolved |

### ai_summary Policy
`ai_summary` must not be silently overwritten. When updating:
- Preserve the prior summary as a dated entry within the field, or
- Claude presents the proposed new summary alongside the current value, and Alejandro approves the replacement explicitly.

Example of versioned update:
```
[2026-04-03] Multiphase MMC Dallas. Phase 0-1 complete. Phase 2 in progress.
[2026-06-28 — updated per Alejandro confirmation] All phases complete. Closed Apr 30.
```

---

## Project 7060 — MMC Dallas Relocation: Pre-Write Checklist

**Immutable UUID:** `d08dabdf-9490-41e2-aede-061912574d71`
**Current status:** `in_progress` | Last updated: 2026-04-03

### Confirmations Required (each is a separate checkbox)

- [ ] **Field completion confirmed** — Alejandro or Frank Barrett confirms Phases 2, 3, and 4 were executed. (Field completion = all crew work done on-site.)
- [ ] **Administrative closure confirmed** — All reporting, invoicing, and client sign-off either complete or explicitly deferred.
- [ ] **FastField status confirmed** — Either: (a) a FastField submission exists with a known reference/ID, or (b) confirmed that no FastField was required for this project type.
- [ ] **Actual end date confirmed** — Exact date provided by PM or Alejandro. Time and timezone required only if available; not assumed.
- [ ] **Finance Group and docking station threads confirmed resolved** — Or explicitly noted as separate open items not blocking closure.
- [ ] **Pre-write SELECT snapshot taken and read by Alejandro.**
- [ ] **Each field change presented and approved individually.**
- [ ] **Full UPDATE SQL read and approved by Alejandro before execution.**

> Note: The Brent Lee phone number discrepancy (469-383-6012 vs. 972-342-2190) is a contact record issue unrelated to project closure. It should be resolved as a separate data cleanup task and does not block status write.

### Fields Under Consideration (no values written until approved)

| Field | Current (snapshot) | Under consideration | Evidence needed |
|-------|-------------------|--------------------|-----------------|
| `status` | `in_progress` | `completed` | Field + admin closure confirmed |
| `actual_end_at` | NULL | Confirmed date/time from PM | PM states actual date |
| `fastfield_submitted` | false | true | FastField reference ID confirmed |
| `completion_report_sent` | false | true | Evidence report was sent |
| `invoiced` | false | true | Alejandro confirms invoice issued |
| `ai_summary` | Apr 3 entry | Versioned addition | Status confirmed |

---

## Project 7348 — Amtrust (Princeton NJ): Pre-Write Checklist

**Immutable UUID:** `1d21f563-ee9f-4d6d-a86b-7183f26c4dac`
**Current status:** `in_progress` | Last updated: 2026-04-17

### Confirmations Required (each is a separate checkbox)

- [ ] **Name/location mismatch resolved** — Authoritative project record identified. "Amtrust Cleveland" name vs. Princeton NJ address explained with a definitive answer. Location fields only corrected after the authoritative record is confirmed — not based on assumption.
- [ ] **Field completion confirmed** — Pedro Martinez or Alejandro confirms Apr 15 Princeton NJ work was completed on-site.
- [ ] **FastField submission verified** — Submission reference number or project link confirmed. `fastfield_submitted = true` in DB must be traced to a specific submission, not assumed to be correct.
- [ ] **Actual end date confirmed** — Exact date from PM. Apr 15 or Apr 16 — PM states which.
- [ ] **No open punch items confirmed** — Pedro Martinez explicitly states no remaining items.
- [ ] **Administrative closure confirmed** — Reporting, invoicing, and client sign-off either complete or explicitly deferred.
- [ ] **Pre-write SELECT snapshot taken and read by Alejandro.**
- [ ] **Each field change presented and approved individually.**
- [ ] **Full UPDATE SQL read and approved by Alejandro before execution.**

### Fields Under Consideration (no values written until approved)

| Field | Current (snapshot) | Under consideration | Evidence needed |
|-------|-------------------|--------------------|-----------------|
| `status` | `in_progress` | `completed` | Field + admin closure confirmed |
| `actual_end_at` | NULL | Confirmed date from PM | PM states Apr 15 or 16 |
| `completion_report_sent` | false | true | Evidence report was sent |
| `invoiced` | false | true | Alejandro confirms invoice issued |
| `location_city` | Princeton | Corrected value if wrong | Authoritative record identified |
| `ai_summary` | Apr 15 / Princeton NJ entry | Versioned addition | Status confirmed |

---

## General Rules (all future project writes)

1. **One project at a time.** Each project requires its own separate approval sequence.
2. **One field at a time.** Approving status does not approve timestamps, completion flags, or summaries.
3. **UUID in WHERE clause.** `project_number` may not be unique across time; UUID is immutable.
4. **Concurrency guard required.** `AND updated_at = '[snapshot value]'` in every UPDATE.
5. **Exactly one affected row.** If UPDATE affects 0 rows, ROLLBACK immediately.
6. **activity_log entry in every transaction.** Written in the same transaction as the data change.
7. **Post-write SELECT required.** Alejandro reads and confirms the result before session closes.
8. **Rollback from snapshot only.** Never from assumed or documented prior values.
9. **No invented timestamps.** Date and time must come from confirmed source or be left NULL.
10. **Smartsheet is source of truth for scheduled dates.** Supabase defers to Smartsheet on date conflicts.
11. **Writes happen in a dedicated write session** explicitly labeled as such before any SQL runs.
12. **Git history is not a Supabase audit trail.** Only `activity_log` entries serve that purpose.

---

*This document is read-only guidance. It does not authorize any writes. Writes require explicit Alejandro approval, field by field, in a live session with this document open.*
