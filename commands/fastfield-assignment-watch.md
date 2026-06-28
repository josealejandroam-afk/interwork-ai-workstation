# /fastfield-assignment-watch

Check whether FastField has been assigned/sent for a given project or set of projects.
Read-only. Never sets `fastfield_submitted`, never updates project records.

Usage: `/fastfield-assignment-watch <project_number>`
       `/fastfield-assignment-watch --all`  (scans all active projects missing fastfield_submitted)

---

## What this command does

Detects whether Alejandro sent FastField instructions to a PM — using the priority chain below.

**This is not the same as FastField being submitted.**

| What it detects | What it does NOT do |
|---|---|
| Whether FF was dispatched to a PM | Set `fastfield_submitted = true` |
| Which PM it was sent to | Update project status |
| When it was sent | Trigger any Supabase write |
| Whether an open loop already exists | Close any loop automatically |

`fastfield_submitted = true` is only proposed when the PM submits the completed form (FastField webhook → `fastfield_webhook_events` table → `/completion-intake`).

---

## Detection Priority Chain

### Priority 1 — M365 / Graph API (preferred)
If Outlook/M365 Graph API is authorized:
- Search Alejandro's sent email for the project number or PM name
- Look for keywords: "FastField", "FF", "form", "field report", plus the project number
- Extract: PM name, date sent, any attached instructions
- Confidence: high if project number found in subject/body

**If M365 OAuth is not complete:** note "Integration gap: Outlook/M365 Graph API not authorized" and fall through to Priority 2.

### Priority 2 — Microsoft Teams
If Teams MCP or Graph API is available:
- Search Teams messages for the project number
- Look for Alejandro sending FF instructions to a PM
- Extract: PM name, channel/chat, date, message text
- Confidence: high if project number + PM name confirmed

**If Teams is unavailable:** fall through to Priority 3.

### Priority 3 — Playwright (Outlook Web) — requires approval
Only if:
1. API access is unavailable
2. Alejandro explicitly approves browser-based reading in this session

Steps:
1. Open `https://outlook.office.com` in browser
2. Search sent mail for project number + "FastField"
3. Extract PM name, date, subject line
4. Screenshot for audit trail
5. Close browser

**Do not run Playwright without explicit approval.**

### Priority 4 — Memory / Open Loops
Check `memory/open_loops/` for any file matching `fastfield_<project_number>_*.md` with status `waiting`.

Also check `fastfield_webhook_events` in Supabase for any row where `project_number_detected` matches:
```sql
SELECT id, form_name, submitter_name, submitted_at, processing_status
FROM public.fastfield_webhook_events
WHERE project_number_detected = '<number>'
ORDER BY received_at DESC
LIMIT 5;
```

### Priority 5 — Manual fallback
If no signal found in any source:
- Report: "No FF assignment evidence found via Outlook, Teams, or memory. Use `/ff-sent <number> <pm_name> <date>` to record manually."

---

## Output

```
## FastField Assignment Watch — Project <number>
Sources checked: M365 (❌ not authorized) | Teams (❌ not authorized) | Memory (✅)

### Result
Status: FF sent evidence: ✅ / ❌ / ⚠️ (uncertain)
Source: [Outlook sent mail / Teams message / memory open loop / not found]
PM: [name or unknown]
Date sent: [date or unknown]
Confidence: high / medium / low / none

### Open loop status
- memory/open_loops/fastfield_<number>_<date>.md: [exists / not found]

### FastField submission status (Supabase)
- fastfield_submitted: true / false / null
- fastfield_webhook_events: [N rows / none]

### Next steps
[if no evidence found]: Use `/ff-sent <number> <pm_name> <date>` to record manually.
[if evidence found, fastfield_submitted = false]: PM has not yet submitted. Open loop stands.
[if webhook event found, fastfield_submitted = false]: Propose `fastfield_submitted = true` via `/completion-intake`.
```

---

## Rules

- Do not set `fastfield_submitted`, `status`, or any confirmation boolean
- Do not send emails or Teams messages
- Playwright requires explicit approval before each use
- Gmail is not checked — personal account only, no project data
- If M365 is not authorized: note as integration gap, do not force auth, use manual fallback
- All Supabase proposals require explicit Alejandro approval
