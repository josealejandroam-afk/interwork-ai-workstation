# /fastfield-intake

Read raw FastField webhook events from `fastfield_webhook_events` and propose project matches.
Read-only analysis. Never auto-updates projects, fastfield_submitted, or any confirmation boolean.

---

## What this command does

1. Queries all `pending` events from `fastfield_webhook_events`
2. Inspects each raw payload to extract key fields
3. Attempts to match each event to a Supabase project
4. Proposes `fastfield_submitted = true` updates for high-confidence matches
5. Flags low-confidence or unmatched events for Alejandro review

All proposals require explicit Alejandro approval before any Supabase write.

---

## Step 1 — Query unprocessed events

```sql
SELECT
    id,
    received_at,
    form_name,
    submission_id,
    project_number_detected,
    submitter_name,
    submitted_at,
    raw_payload,
    processing_status,
    matched_project_id,
    matched_project_confidence
FROM public.fastfield_webhook_events
WHERE processing_status = 'pending'
ORDER BY received_at ASC;
```

Also pull recently matched/error events for context:
```sql
SELECT id, received_at, form_name, project_number_detected,
       processing_status, matched_project_confidence, error_message
FROM public.fastfield_webhook_events
WHERE processing_status != 'pending'
ORDER BY received_at DESC
LIMIT 10;
```

---

## Step 2 — Extract fields from raw_payload

For each `pending` event, inspect `raw_payload` and extract:

| Field to find | Where to look in payload |
|---|---|
| Project number | Form name, field labeled "Project #", "Job #", "Project Number"; or any 4-digit number |
| Form name | Top-level `form_name`, `formName`, or `name` key |
| Submitter name | `submitter`, `submittedBy`, `user`, `technician` field |
| Submitted timestamp | `submittedAt`, `submitted_at`, `completedAt`, `timestamp` |
| Report/PDF links | Any URL containing `.pdf`, `report`, `fastfield`, or labeled `reportUrl`, `pdfUrl` |
| Photo links | Any URL containing `.jpg`, `.png`, `.jpeg`, or labeled `photos`, `images`, `attachments` |

Note: **exact field names are unknown until the first test submission**. After the first real payload lands, update this table with the confirmed field paths.

---

## Step 3 — Match to Supabase project

For each event, attempt a project match using this priority:

1. **project_number_detected already set** (populated by Make.com or prior run) → query directly
2. **4-digit number in form_name** → regex extract, query `projects.project_number`
3. **Form name fuzzy match** → match against `projects.name` (case-insensitive LIKE)
4. **Submitter name match** → match against `projects.pm_assigned` or known field PM list

```sql
SELECT id, project_number, name, status, scheduled_date,
       fastfield_submitted, pm_assigned
FROM public.projects
WHERE project_number = '<extracted_number>'
   OR name ILIKE '%<keyword>%';
```

Confidence rules:
- `high` — 4-digit project number found in payload AND matches a project
- `medium` — project matched by name or submitter, no explicit project number
- `low` — partial name match only
- `unmatched` — no match found

---

## Step 4 — Output

```
## FastField Intake — [datetime]
Events pending: N | Matched: N | Unmatched: N | Errors: N

---

### Event [id] — [form_name]
Received: [received_at]
Submitter: [submitter_name]
Submitted at: [submitted_at]
Project # detected: [value or "not found"]

**Extracted fields:**
- Form name: [value]
- Submitter: [value]
- Submitted at: [value]
- Report URL: [value or "none"]
- Photos: [count or "none"]

**Project match:**
- Matched: #[number] [name] — confidence: high/medium/low/unmatched
- Current fastfield_submitted: true/false
- Current status: [status]

**Proposed action** (requires approval):
- Set fastfield_submitted = true on project [number]
- Update fastfield_webhook_events.id=[id]: processing_status = 'matched', matched_project_id = [uuid], matched_project_confidence = 'high'

---

### Unmatched Events
- [id]: [form_name] — no project found; review manually

### Proposed Updates (not applied)
> Say "apply fastfield match [event_id]" to approve a specific update.
> Say "apply all fastfield matches" to approve all high-confidence proposals.
> Supabase writes require explicit approval — none of the above have been executed.
```

---

## Step 5 — After approval: update records

When Alejandro approves a specific match:

```sql
BEGIN;

-- Update the project
UPDATE public.projects
SET fastfield_submitted = true,
    updated_at = now()
WHERE project_number = '<number>'
  AND fastfield_submitted = false;

-- Update the event record
UPDATE public.fastfield_webhook_events
SET processing_status = 'matched',
    matched_project_id = (SELECT id FROM public.projects WHERE project_number = '<number>'),
    matched_project_confidence = 'high',
    processed = true,
    updated_at = now()
WHERE id = '<event_uuid>';

-- Activity log
INSERT INTO public.activity_log (project_id, actor, action, detail, source, before_state, after_state, occurred_at)
SELECT id, 'alejandro', 'fastfield_submitted_confirmed',
       'FastField submission received via webhook. Event ID: <event_uuid>. Approved by Alejandro.',
       'fastfield',
       jsonb_build_object('fastfield_submitted', false),
       jsonb_build_object('fastfield_submitted', true),
       now()
FROM public.projects WHERE project_number = '<number>';

COMMIT;
```

**Do not run this SQL without explicit "apply" approval from Alejandro.**

---

## Restrictions

- Do not set `fastfield_submitted = true` automatically
- Do not change `status`, `completion_report_sent`, `actual_end_at`
- Do not change `vendor_confirmed`, `client_confirmed`, `access_confirmed`
- Do not apply RLS changes
- All proposals shown to Alejandro before any write
