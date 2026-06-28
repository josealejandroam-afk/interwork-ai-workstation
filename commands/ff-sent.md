# /ff-sent

Manual fallback command. Records that Alejandro sent FastField instructions to a PM when Outlook/M365 Graph API is unavailable.

Usage: `/ff-sent <project_number> <pm_name> <date>`

Example: `/ff-sent 7374 "Frank Barrett" 2026-07-01`

---

## What this command does

**FF Sent ≠ FF Submitted.**

This command records that FastField was *dispatched* to the PM. It does NOT mean the PM has submitted the form yet.

| What it does | What it does NOT do |
|---|---|
| Creates open loop: "Waiting for PM to submit FastField" | Set `fastfield_submitted = true` |
| Logs the assignment in project memory | Update project status |
| Notes the source as `manual` | Trigger any Supabase write without approval |

`fastfield_submitted = true` is only set when the PM submits the form (confirmed via FastField webhook → `fastfield_webhook_events` table).

---

## Steps

### 1. Parse the input
Extract:
- `project_number` — must match an existing Supabase project
- `pm_name` — full name of the field PM assigned
- `date` — date FF was sent (or today if not specified)

### 2. Look up the project
Query Supabase: `SELECT id, name, status FROM public.projects WHERE project_number = '<number>'`

If not found: stop and report. Do not create a record.

### 3. Create an open loop in memory

Write `memory/open_loops/fastfield_<project_number>_<date>.md`:

```markdown
---
name: fastfield-sent-<project_number>-<date>
source: manual
project: <project_number>
person: <pm_name>
status: waiting
priority: medium
created: <datetime>
updated: <datetime>
---

FastField sent to <pm_name> for project <project_number> on <date>. Waiting for PM to submit the form.

**Action needed:** Monitor for FastField webhook submission in `fastfield_webhook_events`. When received, propose `fastfield_submitted = true` via `/completion-intake`.
```

### 4. Propose activity_log entry (do not apply without approval)

Draft for Alejandro's approval:
```sql
INSERT INTO public.activity_log (project_id, actor, action, detail, source, before_state, after_state, occurred_at)
SELECT id, 'alejandro', 'ff_sent', 'FastField dispatched to <pm_name> on <date>. Awaiting submission.', 'manual', '{}', '{}', '<datetime>'
FROM public.projects WHERE project_number = '<number>';
```

### 5. Confirm

Report:
- Project found: ✅ / ❌
- Open loop created: ✅ path/to/file.md
- Proposed activity_log insert: show draft, wait for "approve"
- Reminder: `fastfield_submitted` is NOT changed by this command

---

## When Outlook/M365 is available

This command becomes optional. Preferred flow:
1. M365 Graph API reads Alejandro's sent email to detect FF dispatch automatically
2. Teams messages are checked as a secondary source
3. `/ff-sent` is the manual fallback when API is unavailable

If M365 Graph API is not authorized: note the integration gap and use `/ff-sent` until OAuth is complete.

---

## Permission boundary
- Creating memory open-loop file: auto-allowed
- activity_log INSERT: requires Alejandro approval
- Any update to `fastfield_submitted`, `status`, or other project fields: never from this command
