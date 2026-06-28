---
name: fastfield-make-integration
description: "FastField → Make.com webhook integration: scenario IDs, payload mapping, setup status, and next steps"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  updated: 2026-06-26
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# FastField → Make.com Integration

## Status: PARTIAL — webhook channel open, payload not being parsed

**Verified 2026-06-28 (read-only Supabase query):**
- `fastfield_webhook_events` has 4 rows, all received 2026-06-26 ~23:04–23:08 UTC
- All 4 rows: processed=false, processing_status=pending, all parsed fields null (form_name, submission_id, project_number_detected, submitter_name, submitted_at)
- Only `source='fastfield'` and `received_at` are populated — Make is writing shell rows
- Payload field names unknown — never confirmed via test submission
- Normalization responsibility: local `/fastfield-intake` command (downstream processor), not Make
- Make's role per design: store raw_payload; downstream processor reads and extracts
- Failure point: raw_payload content unknown — either Make is not writing it, or the field path mappings in Make's Supabase module are incomplete
- Do NOT claim body mapping is definitively the cause without inspecting Make execution history
- Do NOT trigger a test submission without Alejandro approval (creates a new DB event)

---

## Make.com Resources

| Item | Value |
|------|-------|
| Scenario name | FastField Submission Intake |
| Scenario ID | 5506328 |
| Webhook name | FastField Completed Submission |
| Hook ID | 2508004 |
| Scenario active? | No — activate after test payload confirmed |
| Webhook URL | stored in `D:\ai-workstation\scripts\fastfield_webhook_config.txt` |
| Token secret | stored in `D:\ai-workstation\scripts\fastfield_webhook_config.txt` |

**Do not store the webhook URL or token secret in this file or RAG.**

---

## Webhook Configuration

- Type: `gateway-webhook` (Make.com custom webhook)
- Headers captured: yes (`headers: true`)
- HTTP method captured: yes (`method: true`)
- JSON pass-through: no (payload parsed as JSON, not string)
- Auth: token in query string `?token=<secret>` — filter to be added in Phase 2

---

## Supabase Schema Decision

`fastfield_forms` **cannot** be used as an intake buffer:
- `project_id` column is `UUID NOT NULL` (FK to projects)
- Raw unmatched submissions have no project_id yet
- Using it would require project matching before storage — defeats the purpose

**Proposed table:** `fastfield_webhook_events`
- Draft SQL: `D:\ai-workstation\scripts\sql\draft_create_fastfield_webhook_events.sql`
- Status: **awaiting Alejandro approval** — say "apply fastfield events table"

---

## fastfield_webhook_events Fields (proposed)

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| received_at | timestamptz | When Make received it |
| source | text | Default 'fastfield' |
| form_name | text | Form name from payload |
| submission_id | text | FastField submission ID |
| project_number_detected | text | Extracted 4-digit project number |
| submitter_name | text | Field PM name from payload |
| submitted_at | timestamptz | When FF form was completed |
| raw_payload | jsonb | Full webhook body |
| processed | boolean | false until reviewed |
| processing_status | text | pending / matched / unmatched / error / skipped |
| matched_project_id | uuid | Nullable FK to projects |
| matched_project_confidence | text | high / medium / low |
| error_message | text | Any processing errors |

---

## FastField Integration Setup (FastField side — not yet done)

1. In FastField admin, go to: Settings → Integrations → HTTP/HTTPS
2. Enter the webhook URL (from `fastfield_webhook_config.txt`)
3. Add query param: `?token=<secret>` (from `fastfield_webhook_config.txt`)
4. Trigger: "On form submission" or "On completion"
5. Method: POST
6. Content-Type: application/json

**FastField header support unknown** — if FastField supports custom headers, add `x-make-apikey` header as well (Make.com native auth). Check FastField docs or test.

---

## Expected Payload Fields (unknown until first test submission)

Mapping to be confirmed after first real test payload. Expected fields based on typical FastField exports:

| FastField field | Expected Make.com path | Maps to |
|----------------|----------------------|---------|
| Form name | `{{1.form_name}}` or similar | form_name |
| Submission ID | `{{1.id}}` or `{{1.submission_id}}` | submission_id |
| Submitted by | `{{1.submitted_by}}` or `{{1.user}}` | submitter_name |
| Submitted at | `{{1.submitted_at}}` or `{{1.created_at}}` | submitted_at |
| Project number | `{{1.project_number}}` or from form fields | project_number_detected |
| PDF report URL | `{{1.report_url}}` or `{{1.pdf}}` | inside raw_payload |
| Photos | `{{1.photos}}` or `{{1.attachments}}` | inside raw_payload |

**Confirm actual field names after first test payload.**

---

## Phase Plan

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Make.com scenario + webhook created | ✅ Done |
| 1 | fastfield_webhook_events SQL drafted | ✅ Done |
| 1 | Supabase table creation | ✅ Applied 2026-06-26 |
| 2 | Token rotated (old token was in terminal) | ✅ Done 2026-06-26 |
| 2 | Token filter added to Make scenario | ✅ Done — checks {{1.query.token}} |
| 2 | Make → Supabase insert module added | ✅ Done — HTTP POST to fastfield_webhook_events |
| 2 | FastField HTTP integration configured | ⏳ Alejandro action needed — see setup instructions |
| 3 | ONE controlled test submission | ⏳ Next step — scenario still inactive |
| 3 | Payload field names mapped | ⏳ After test submission |
| 3 | Scenario activated for production | ⏳ After payload confirmed |
| 4 | /completion-intake updated to read fastfield_webhook_events | Not started |

---

## Rules

- Make.com scenario **must not** update any project fields automatically
- Never flip: `fastfield_submitted`, `completion_report_sent`, `actual_end_at`, `status`, `vendor_confirmed`, `client_confirmed`, `access_confirmed`
- All project updates from FastField evidence go through `/completion-intake` → Alejandro approval
- `fastfield_webhook_events` is a staging buffer only — not a trigger for downstream automation
