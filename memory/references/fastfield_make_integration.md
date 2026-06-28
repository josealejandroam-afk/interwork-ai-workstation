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

## Status: BLOCKED — raw_payload mapping broken, hands-off repair exhausted

**Updated 2026-06-28 after controlled test:**
- `fastfield_webhook_events` now has 5 rows (4 original shell rows + 1 controlled test row)
- Make reaches Supabase ✅ — rows are created, source/processing_status/processed are correct
- FastField reaches Make ✅ — webhook channel is open
- `raw_payload` mapping is broken ❌ — both attempted fixes failed:
  - `{{1.body}}` → resolves to nothing (no `body` key at root) → raw_payload = `{}`
  - `{{1}}` → resolves to literal number `1` in Make's raw string template → raw_payload = `1` (jsonb number)
- No native Supabase connection exists in Make (connections_list = [])
- Make MCP/API does not expose webhook bundle field names programmatically

**Hands-off repair is BLOCKED. Remaining paths:**
1. Make UI: manually register a real FastField webhook sample in module 1 ("Run once" + real FastField submit), then map explicit root fields — Alejandro does not want this now
2. Replace Make with a direct receiver / Supabase Edge Function (future option)
3. Wait until Alejandro is ready to do the manual Make UI sample registration

**Do not continue FastField troubleshooting until Alejandro explicitly resumes.**
**Do not run more tests. Do not modify Make. Do not ask for screenshots.**

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
