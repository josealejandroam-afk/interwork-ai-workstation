# Approval Checklist — Project Status Writes
**Scope:** Projects 7060 and 7348  
**Date created:** 2026-06-28  
**Rule:** No writes to Supabase without explicit Alejandro approval, item by item.

---

> **STOP. Read this before asking Claude to write anything.**  
> This checklist exists because confirmation fields and status fields in the InterWork Command Center are partially unbackfilled. An incorrect status write can corrupt reporting, trigger automation, or create a false paper trail. Every checkbox below must be confirmed before Claude is given permission to write.

---

## Project 7060 — MMC Dallas Relocation

### Pre-Write Confirmation Checklist

- [ ] **Alejandro confirms** that Phases 2, 3, and 4 were executed as planned (IT install Apr 7–9, Walnut Hill decom Apr 11–29, final punch Apr 30).
- [ ] **Alejandro or Frank Barrett confirms** the project is fully complete — no open punch items, no outstanding docking station or Finance Group threads.
- [ ] **FastField explained** — either a FastField form was submitted (under what submission ID?) or confirm that no field report was required for this project type.
- [ ] **Brent Lee phone number discrepancy resolved** — DB has 469-383-6012; notes reference 972-342-2190. Confirm correct number for record.
- [ ] **actual_end_at date confirmed** — what date did Phase 4 (final punch) actually close? Required before writing `actual_end_at`.

### Fields That Would Change If Approved

| Field | Current Value | Proposed Value | Requires Approval |
|-------|--------------|----------------|-------------------|
| `status` | `in_progress` | `completed` | YES — Alejandro only |
| `actual_end_at` | NULL | e.g. `2026-04-30T17:00:00+00` | YES — date must be confirmed |
| `fastfield_submitted` | false | true (if applicable) | YES — only if confirmed submitted |
| `completion_report_sent` | false | true (if applicable) | YES — only if report was actually sent |
| `invoiced` | false | true (if applicable) | YES — only if invoiced |

### Rollback Plan
If a write is made in error:
1. Claude runs: `UPDATE projects SET status='in_progress', actual_end_at=NULL WHERE project_number='7060';`
2. Any other changed fields restored to their pre-write values (noted above as "Current Value").
3. Rollback requires Alejandro approval to execute — Claude does not self-rollback.
4. Git commit history and this document serve as the audit trail.

---

## Project 7348 — Amtrust Cleveland (Princeton NJ)

### Pre-Write Confirmation Checklist

- [ ] **Name/location mismatch resolved** — project is named "Amtrust Cleveland" but location is Princeton NJ. Alejandro confirms: is this the Princeton NJ job, or is "Cleveland" the client account name?
- [ ] **Alejandro or Pedro Martinez confirms** Apr 15 work in Princeton NJ was completed successfully.
- [ ] **FastField submission verified** — `fastfield_submitted = true` in DB. Alejandro confirms this reflects a real submission (not a manual flag). Submission reference/ID noted if available.
- [ ] **actual_end_at date confirmed** — what date did the job close? Apr 15 or Apr 16?
- [ ] **No open punch items** — Pedro Martinez confirms no remaining items from the Apr 15 visit.

### Fields That Would Change If Approved

| Field | Current Value | Proposed Value | Requires Approval |
|-------|--------------|----------------|-------------------|
| `status` | `in_progress` | `completed` | YES — Alejandro only |
| `actual_end_at` | NULL | e.g. `2026-04-15T17:00:00+00` | YES — date must be confirmed |
| `completion_report_sent` | false | true (if applicable) | YES — only if report was actually sent |
| `invoiced` | false | true (if applicable) | YES — only if invoiced |
| `location_city` | Princeton | Cleveland (if mismatch is an error) | YES — only if confirmed wrong |

### Rollback Plan
If a write is made in error:
1. Claude runs: `UPDATE projects SET status='in_progress', actual_end_at=NULL WHERE project_number='7348';`
2. Any other changed fields restored to their pre-write values.
3. Rollback requires Alejandro approval to execute.
4. This document and git history serve as the audit trail.

---

## General Rules (apply to all future project status writes)

1. **One project at a time.** Never batch-update statuses across multiple projects in a single session without a separate approval for each.
2. **No mass confirmation field updates.** `vendor_confirmed`, `client_confirmed`, `access_confirmed` must be updated per-project with a known source (email, PM confirmation, Smartsheet record).
3. **No completion_report_sent = true without evidence** the report was actually sent (email record, PM confirmation).
4. **No invoiced = true without confirmation** from Alejandro.
5. **Smartsheet is source of truth for scheduled dates.** If Supabase and Smartsheet disagree on a date, Smartsheet wins until reconciled.
6. **Claude must confirm the exact SQL before executing.** Alejandro reads and approves the SQL text, then says "run it."
7. **Writes happen in a separate session** clearly labeled as a write session. This document must be open during that session.
8. **After any write, Claude runs a SELECT** on the updated row and pastes the result for Alejandro to verify.

---

*This document is read-only guidance. It does not authorize any writes. Writes require explicit Alejandro approval in a live session.*
