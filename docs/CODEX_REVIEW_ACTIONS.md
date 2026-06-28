# Codex Review Actions
**Date:** 2026-06-28
**Triggered by:** Codex read-only review of local documentation drafts
**Scope:** Documentation fixes only — no Supabase writes, no sends, no external connections

---

## Codex Findings Summary (12 items)

| # | Finding | Severity | Applied? |
|---|---------|----------|----------|
| 1 | Approval checklist lacked write safety controls (snapshot, UUID, concurrency guard, transaction, row assertion, activity_log, post-write verify, snapshot-based rollback) | High | YES |
| 2 | Invented timestamps in rollback SQL (e.g. `17:00:00+00`) | High | YES |
| 3 | Fields treated as bundled decisions rather than independent evidence-based approvals | High | YES |
| 4 | `ai_summary` silently overwritten rather than versioned | Medium | YES |
| 5 | Phone discrepancy for Brent Lee (7060) mixed into closure checklist — unrelated concern | Low | YES |
| 6 | EXTERNAL_INTEGRATION_GATES.md stale — showed Supabase/OpenAI as disconnected | Medium | YES |
| 7 | SAFE_COMMANDS_REFERENCE.md stale — Tier 3/5 showed as blocked | Medium | YES |
| 8 | Webhook token suggested as storable in repo file | High | YES |
| 9 | Health review recommended activating Make/M365 without framing as future step | Medium | YES |
| 10 | Operational phone numbers/emails in committed docs | Medium | Partial — see note |
| 11 | Confirmation drafts promised to "close/update the record" rather than request approval | Medium | YES |
| 12 | Approval checklist missing: written confirmation source, pre-write snapshot, field-by-field approval, transaction controls, activity_log, post-write verify, snapshot rollback | High | YES |

---

## What Was Changed

### `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` — Full rewrite
- Added required 6-step write procedure: pre-write SELECT snapshot → field-by-field proposal → SQL review → row count assertion → post-write verify → rollback from snapshot
- WHERE clause now requires immutable UUID, not project_number alone
- Added `AND updated_at = '[snapshot value]'` concurrency guard
- Added transaction structure with `activity_log` INSERT in same transaction
- Added exactly-one-row assertion (ROLLBACK on 0 rows)
- Removed all invented timestamps (no assumed `17:00:00+00` or similar)
- Each field (status, actual_end_at, fastfield_submitted, completion_report_sent, invoiced, location, ai_summary) is now an independent evidence-based decision
- Added ai_summary versioning policy — prior entry preserved, not silently overwritten
- Brent Lee phone discrepancy moved to a separate note; no longer listed as a closure blocker
- Added explicit note: git commit history is NOT a Supabase audit trail
- Rollback procedure now references pre-write snapshot values only

### `PROJECT_STATUS_CONFIRMATION_DRAFTS.md` — Full rewrite
- Removed "Once I hear back I'll close/update the record" — replaced with "I'll review the evidence and request approval for any appropriate update"
- For 7060: field completion and administrative closure are now asked as separate questions
- For 7060: Finance Group and docking station threads asked as "resolved or tracked separately" — not treated as blocking
- For 7348: Teams and email drafts now ask for FastField submission reference/project number and address, not merely confirmation that a submission exists
- For 7348: removed any promise to "correct" location until authoritative record is identified
- Internal notes now clarify: "completed" for DB purposes means fieldwork AND administrative closure, or explicit deferral
- Contact details (phone numbers, email addresses) removed from committed draft text — redirected to Outlook/Teams/local contacts
- Rollback SQL removed from this file — redirected entirely to APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md

### `EXTERNAL_INTEGRATION_GATES.md` — Targeted edits
- Supabase: status updated from "NOT connected -- env vars missing" to "CONNECTED — read-only queries active"
- SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY: MISSING → PRESENT
- OpenAI: status updated from "NOT connected" to "CONNECTED — OPENAI_API_KEY present"
- FastField/Make: removed suggestion that webhook credentials should be stored in a repo file. Added explicit rule: credentials must be in local env vars, Make.com secret storage, or a secure secret manager only — never committed to the repo
- FastField/Make activation rephrased as a future step requiring explicit approval after current review work is complete
- Summary table updated to reflect current connection status

### `SAFE_COMMANDS_REFERENCE.md` — Targeted edits
- Tier 3 (Supabase): changed from "Blocked Until Env Vars Set" to "CONNECTED" with note that reads are available immediately and writes follow the approval checklist
- Tier 5 (OpenAI): changed from "Needs OpenAI Key + feedback_loop/ Migration" to "CONNECTED"
- Quick Decision Guide updated to reflect Supabase as currently connected

### `CODEX_REVIEW_ACTIONS.md` — New file (this file)

---

## What Was Intentionally Not Changed

| Item | Reason not changed |
|------|--------------------|
| `PROJECT_STATUS_REVIEW_7060_7348.md` contact details (Jane Bae email, Sergio Rios phone, etc.) | These were extracted directly from Supabase `internal_notes` which already contains this data. Removing from the doc while the DB retains it provides limited value. Flagged as remaining decision point — see below. |
| `LIVE_SUPABASE_READONLY_HEALTH_REVIEW.md` "next steps" section | Report is a historical snapshot; changing it retroactively would reduce its value as an audit record. Future health reviews will use the revised framing. |
| Project status fields in Supabase | No writes performed — read-only session. |
| Any other operational commands or memory files | Out of scope for this Codex review pass. |

---

## Remaining Decision Points (before any writes)

### Projects 7060 and 7348
- [ ] Frank Barrett confirmation received for 7060 (field completion, admin closure, FastField reference, actual close date)
- [ ] Pedro Martinez confirmation received for 7348 (Princeton NJ vs. Cleveland, FastField submission reference, close date, open items)
- [ ] Alejandro reviews confirmations and decides which fields to approve for write
- [ ] Write session opened per `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` procedure

### Contact details in `PROJECT_STATUS_REVIEW_7060_7348.md`
- **RESOLVED 2026-06-28.** Direct phone numbers and email addresses removed from the Assignment & Contacts table for project 7060. Replaced with name/role references and pointer to Supabase `internal_notes` and Outlook/Teams for live contact details.
- Project 7348 contacts were already NULL in the DB — no change needed.

### Webhook credential storage
- **RESOLVED 2026-06-28.** Searched `D:\ai-workstation` recursively — `fastfield_webhook_config.txt` does not exist on disk. No live token found in repo files. No escalation required.

### Make.com / M365 activation
- Both are explicitly deferred until the current read-only review and project status confirmation work is complete and Alejandro gives an explicit go-ahead.
- Do not activate Make.com scenario 5506328 or reconnect M365 OAuth as part of this session.

---

*This file documents the Codex review pass. It does not authorize any writes.*
