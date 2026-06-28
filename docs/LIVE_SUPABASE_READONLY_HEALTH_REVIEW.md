# Live Supabase Read-Only Health Review
**Date:** 2026-06-28  
**Time:** ~15:55 local  
**Source:** Supabase project `hskgrxhdtgowagkfkjsw` (interwork-command-center)  
**Mode:** Read-only — no writes, updates, or deletes performed  
**Performed by:** Claude Code (claude-sonnet-4-6)

---

## Queries Performed

| # | Query | Purpose |
|---|-------|---------|
| 1 | `projects WHERE status IN (approved, scheduled, in_progress, planning) AND pm_assigned = false` | Missing PM assignments |
| 2 | `projects WHERE status IN (approved, scheduled, in_progress, planning)` — all confirmation fields | Vendor/client/access gaps |
| 3 | `projects WHERE status = in_progress` — with created_at | In-progress age check |
| 4 | `projects WHERE scheduled_date < CURRENT_DATE AND status NOT IN (completed, cancelled, closed)` | Overdue / past-date projects |
| 5 | `projects WHERE fastfield_submitted = true AND completion_report_sent = false` | Completion report backlog |
| 6 | `SELECT COUNT(*) FROM communications` | Communications table population |
| 7 | `SELECT COUNT(*) FROM checklist_items` | Checklist items population |
| 8 | `SELECT COUNT(*) FROM fastfield_forms` | FastField forms population |

---

## Summary Snapshot

| Metric | Value |
|--------|-------|
| Total projects in DB | 140 |
| Completed | 77 |
| Scheduled | 54 |
| In-progress | 5 |
| Pending approval | 2 |
| On hold | 1 |
| Cancelled | 1 |
| Projects with no PM assigned (active) | 7 |
| Projects past scheduled date, not closed | 56 |
| fastfield=true, completion_report=false | 57 |
| `communications` rows | **0** |
| `checklist_items` rows | **2** |
| `fastfield_forms` rows | **1** |

---

## Finding 1 — Missing PM Assignment (Active/Scheduled)

7 active or scheduled projects have `pm_assigned = false`.

| Project # | Name | Scheduled Date | Days Overdue |
|-----------|------|----------------|-------------|
| 7370 | MMA Decom + Whiteboard Install — Bend OR | 2026-04-30 | 59 days past |
| 7418 | MMA Colleague Relocation + Decom — Columbia MD | 2026-05-20 | 39 days past |
| 7512 | Togetherwork Kesef Accounting Office Decom — Montvale NJ | 2026-05-28 | 31 days past |
| 7537 | CRC Walkthrough Client Checkin — Tampa FL | 2026-06-18 | 10 days past |
| 7304 | Montebello Install Acoustic Panels + Chairs — West Berlin NJ | 2026-07-02 | 4 days out |
| 7494 | MMA Furniture Move — San Diego to Walnut Creek CA | 2026-07-06 | 8 days out |
| 7546 | MMA Conference Room Table Replacement — Dallas TX | 2026-07-09 | 11 days out |

**Assessment:** Three of these are already past their scheduled dates with no PM on record. Two more are within 2 weeks. Requires Alejandro review — these may be PM-tracked externally and simply unbackfilled, or may genuinely lack assignment.

---

## Finding 2 — Confirmation Fields (vendor / client / access)

**Data-quality warning:** The vast majority of `vendor_confirmed`, `client_confirmed`, and `access_confirmed` fields read `false` across all 59 active/scheduled/in-progress projects. This matches the known backfill gap identified in the Jun 26 backfill review. These values should be treated as **unknown/untracked** unless supported by other evidence.

**Exception — projects with at least one `true` confirmation field (likely legitimately tracked):**

| Project # | Name | Vendor | Client | Access |
|-----------|------|--------|--------|--------|
| 7060 | MMC Dallas — Walnut Hill to Galleria | ✅ | ❌ | ❌ |
| 7053 | Strategic Education — Washington DC | ❌ | ✅ | ✅ |
| 7431 | MMC Walkthrough for Internal Move | ✅ | ❌ | ✅ |
| 7348 | Amtrust Cleveland | ✅ | ❌ | ✅ |
| 7322 | Goldberg Segalla May 5 | ✅ | ❌ | ✅ |
| 7354 | MMA Retrieve Tech — Alpharetta GA | ✅ | ❌ | ✅ |
| 7516 | UiPath Service Call — Dallas TX | ✅ | ❌ | ✅ |
| 7407 | MMC Install Service Call — Phoenix AZ | ✅ | ❌ | ✅ |
| 7364 | MMC Allentown Move & Workstation Setup | ❌ | ❌ | ✅ |
| 7440 | Rothman Move — King of Prussia PA | ❌ | ❌ | ✅ |

**Pattern:** `client_confirmed` is almost universally false, even for projects that appear operationally active. This field is most likely unbackfilled across the board and should not be treated as a real signal without manual verification.

---

## Finding 3 — In-Progress Projects Past Their Scheduled Date

All 5 in-progress projects are past their scheduled start date. These may be multi-day/multi-phase projects that are legitimately still open, or they may need status updates.

| Project # | Name | Scheduled Date | Days Since Start | Created |
|-----------|------|----------------|-----------------|---------|
| 7060 | MMC Dallas — Walnut Hill to Galleria Relocation & Decom | 2026-04-03 | **86 days** | 2026-03-25 |
| 7348 | Amtrust Cleveland | 2026-04-15 | **74 days** | 2026-03-17 |
| 7381 | Resintech Deliver Install Monitor Arms — Camden NJ | 2026-04-21 | **68 days** | 2026-04-21 |
| 7435 | MMA Colleague Relocation | 2026-04-23 | **66 days** | 2026-04-13 |
| 7440 | Rothman Move — King of Prussia PA | 2026-05-04 | **55 days** | 2026-04-13 |

**Assessment:** Projects 7060 and 7348 are the oldest at 74–86 days in-progress. These either need to be marked completed, or there is an active multi-phase or unresolved issue. Requires Alejandro to confirm actual status.

---

## Finding 4 — Projects Past Scheduled Date, Not Closed

**56 projects** have a `scheduled_date` before 2026-06-28 and are not in `completed`, `cancelled`, or `closed` status.

Breakdown by status:
- `scheduled`: 48 projects
- `in_progress`: 5 projects (covered in Finding 3)
- `pending_approval`: 2 projects (7395 Dallas Office Restack, 7497 Radian TierPoint Navy Yard Decom)
- `on_hold`: 1 project (7484 MMA Service Call Raleigh NC)

**Oldest overdue scheduled (not in-progress):**

| Project # | Name | Scheduled Date |
|-----------|------|----------------|
| 7364 | MMC Allentown Move & Workstation Setup Support | 2026-03-19 |
| 7053 | Strategic Education — Washington DC | 2026-03-21 |
| 7434 | MMA Paint Scope / Furniture Decom | 2026-04-07 |
| 7454 | Vecos Commissioning — Tallahassee FL | 2026-04-16 |
| 7391 | Premier Orthopedics Multi-Phase — Newtown Square PA | 2026-04-24 |
| 7467 | Dropbox Seattle Studio Move | 2026-04-27 |
| 7370 | MMA Decom + Whiteboard Install — Bend OR | 2026-04-30 |

**Data-quality note:** Many of these may be complete in reality but never had their status updated to `completed` in Supabase. The backfill review from 2026-06-26 noted this pattern (38 red / 9 yellow with `status = scheduled` but past their dates). Do not mass-update statuses without Alejandro approval.

**Pending approval projects past their dates:**
- **7395** Dallas Office Restack — scheduled 2026-04-11, still `pending_approval`
- **7497** Radian TierPoint Navy Yard Decom — scheduled 2026-05-18, `pending_approval` but `fastfield_submitted = true` (anomaly — field work appears to have occurred before formal approval was recorded)

---

## Finding 5 — FastField Submitted, Completion Report Not Sent

**57 projects** have `fastfield_submitted = true` AND `completion_report_sent = false`.

Breakdown:
- `completed` status: ~40 projects — historical backlog, work is done but reports were never sent or logged
- `in_progress`: 5 projects (7060, 7348, 7381, 7435, 7440)
- `scheduled` (fastfield already submitted): 5 projects (7364, 7053, 7391, 7352, 7447)
- `pending_approval`: 1 (7497 — anomalous, work done before approval logged)
- `cancelled`: 1 (7485 MMC Huddle Room Conversion NYC — fastfield submitted on a cancelled project)

**Oldest completed projects with no report sent:**

| Project # | Name | Scheduled Date |
|-----------|------|----------------|
| 6682 | MMC Phoenix Decommission | 2024-12-23 |
| 6345 | Rothman Sheridan Building Decom | 2024-12-24 |
| 6629 | MediLink Hammonton Reception Install | 2025-01-06 |
| 6728 | Wasserman One Liberty Plaza Move | 2025-01-06 |
| 6747 | Seth Lehr Cylinder Swap | 2025-01-09 |

**Assessment:** The `completion_report_sent` field appears to be untracked or never populated from day one. Reports may have been sent via email (outside the DB), or the field was simply never updated. Do not mass-set to `true` without Alejandro review. However, this is a strong candidate for future automation once the M365 email pipeline is active.

**Notable anomaly — 7447 MMA Tech Install Move Clearwater Tampa FL:**  
Status = `scheduled`, scheduled_date = 2026-06-16 (12 days ago), `fastfield_submitted = true`. This project has a FastField submission but is still listed as `scheduled`. Likely completed — needs status confirmation.

---

## Finding 6 — Table Population Status

### `communications` — 0 rows
Completely empty. No email/comms data has been ingested. The M365 pipeline (Outlook via Graph API or Make.com webhook) has not run or has not been connected yet. This is expected given MCP reauthorization has not started.

### `checklist_items` — 2 rows
Nearly empty. Only 2 checklist items exist in the entire database. The checklist system is present in schema but not operationally populated. No pending items were returned when joined against active projects.

### `fastfield_forms` — 1 row
Only 1 FastField form record exists. The FastField → Make.com → Supabase webhook pipeline (scenario 5506328) exists and has been configured, but has not delivered data at scale. Either the scenario was never activated, or only one test submission came through.

---

## Data-Quality Warnings

1. **Confirmation fields (vendor/client/access) are unreliable as-is.** With 54 of 54 scheduled projects showing `client_confirmed = false` and ~48 showing `vendor_confirmed = false`, these fields are presumed unbackfilled, not truly unconfirmed. Do not build automation or alerts on these fields until a backfill pass is done.

2. **`completion_report_sent` is never `true`.** A field that is never populated provides no signal. This is a data entry gap, not a real operational gap (reports may have been sent).

3. **`status = scheduled` for projects 3+ months past their date** is likely a historical migration artifact. These should be audited against Smartsheet source of truth before any status transitions.

4. **`fastfield_submitted` on `scheduled` projects** (7364, 7053, 7391, 7352) suggests either multi-phase projects where a partial submission was made, or the field was set forward-looking and doesn't reflect actual submission timing.

5. **Project 7497 (Radian TierPoint):** Status = `pending_approval`, scheduled 2026-05-18 (41 days ago), but `fastfield_submitted = true`. Work appears to have occurred before approval was formally recorded. Flag for review.

6. **Project 7485 (MMC Huddle Room Conversion NYC):** Status = `cancelled`, but `fastfield_submitted = true`. A FastField submission exists for a cancelled project. Verify if this was a mistaken submission or if partial work occurred.

---

## Projects Requiring Alejandro Review

| Priority | Project # | Issue |
|----------|-----------|-------|
| HIGH | 7060 | In-progress 86 days — MMC Dallas Relocation. Status unclear. |
| HIGH | 7348 | In-progress 74 days — Amtrust Cleveland. May be complete. |
| HIGH | 7370 | No PM, 59 days past date — MMA Bend OR |
| HIGH | 7418 | No PM, 39 days past date — MMA Columbia MD |
| HIGH | 7304 | No PM, due Jul 2 (4 days) — Montebello West Berlin NJ |
| MEDIUM | 7497 | pending_approval + fastfield_submitted — Radian TierPoint Philadelphia |
| MEDIUM | 7447 | scheduled + fastfield_submitted, 12 days past — MMA Tampa FL |
| MEDIUM | 7395 | pending_approval since Apr 11 — Dallas Office Restack |
| MEDIUM | 7512 | No PM, 31 days past date — Togetherwork Montvale NJ |
| MEDIUM | 7537 | No PM, 10 days past date — CRC Tampa FL |
| LOW | 7485 | Cancelled project with fastfield_submitted = true |
| LOW | All ~40 completed | fastfield_submitted = true, completion_report_sent = false (historical backlog) |

---

## Prioritized Next Actions

### HIGH PRIORITY
- [ ] **Confirm status of 7060 and 7348** — oldest in-progress projects (74–86 days). If complete, update status. If still active, document why.
- [ ] **Assign PMs to 7304, 7494, 7546** — due within 2 weeks, no PM on record.
- [ ] **Review 7370, 7418, 7512** — past date with no PM. May be complete or stalled.

### MEDIUM PRIORITY
- [ ] **Activate FastField → Make.com → Supabase pipeline** (scenario 5506328) to start populating `fastfield_forms` table.
- [ ] **Connect M365/Outlook pipeline** to start populating `communications` table. This is the highest-value data gap.
- [ ] **Confirm 7447 (MMA Tampa)** — scheduled + fastfield_submitted, 12 days past date. Likely completed.
- [ ] **Resolve 7497 (Radian TierPoint)** — work done before approval recorded.

### LOW PRIORITY
- [ ] **Backfill `completion_report_sent`** for completed projects where reports were actually sent. Start with recent completions (2026) before going back to late 2024.
- [ ] **Confirm 7485 (cancelled + fastfield_submitted)** — document whether partial work occurred.
- [ ] **Review 7395 (Dallas Office Restack)** — pending approval since Apr 11.

### DATA CLEANUP ONLY (requires Alejandro approval before any action)
- [ ] **Do not mass-update confirmation fields** — backfill must be done per-project with verified data.
- [ ] **Do not mass-set `status = completed`** for past-date scheduled projects — verify against Smartsheet first.
- [ ] **Consider a structured backfill session** where Smartsheet is queried for actual project completion dates and used to reconcile Supabase status fields.

---

## Items Safe to Automate Later

Once pipelines are live and backfill is clean:
- Auto-flag projects approaching scheduled date with no vendor confirmed
- Auto-flag in-progress projects >30 days with no fastfield submission
- Auto-log communications from M365 into `communications` table via Make.com
- Auto-set `fastfield_submitted = true` when FastField webhook delivers to Supabase
- Generate weekly completion report backlog list

## Items Requiring Human Approval Before Automation

- Any status transition (scheduled → completed, etc.)
- Any `completion_report_sent` field update
- Any PM assignment change
- Any confirmation field update (vendor/client/access)
- Sending completion reports to clients

---

## Recommended Next Steps (in order)

1. **Alejandro reviews the 7 no-PM projects** and confirms which are assigned externally.
2. **Alejandro confirms status** of in-progress 7060 and 7348 (oldest, possibly complete).
3. **Activate Make.com scenario 5506328** (FastField webhook) — low-risk, adds data.
4. **Begin MCP reauthorization** for Outlook/M365 to unlock `communications` table population.
5. **Run structured backfill session** for project statuses using Smartsheet as source of truth — with Alejandro present to approve each transition.

---

*Report generated read-only. No data was written, updated, or deleted in Supabase during this session.*
