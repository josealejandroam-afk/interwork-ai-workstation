# /completion-intake

Accept completion signals from any source and propose Supabase updates for review.
Never applies changes automatically. Always surfaces proposed updates for Alejandro approval.

Usage:
  `/completion-intake --paste`              paste a FastField note, email, or completion summary
  `/completion-intake --file <path>`        read from .csv, .txt, .md, .pdf, .docx
  `/completion-intake --folder <path>`      scan folder for completion evidence files
  `/completion-intake --email`              paste email text (WC report confirmation, FastField alert, etc.)

---

## Email parser script

For email input, run the parser first to extract structured evidence:

```powershell
# From a saved email file
python D:\ai-workstation\scripts\parse_completion_email.py --file path\to\email.txt

# Pasted inline
python D:\ai-workstation\scripts\parse_completion_email.py --paste

# Quick test string
python D:\ai-workstation\scripts\parse_completion_email.py --text "email body here"
```

Parser output is JSON with: `parsed`, `proposed_updates`, `confidence`, `source_type`.
Pass the output to Step 2 (project matching) and Step 3 (field state evaluation).

**Note:** Work email (WC reports, FastField notifications) lives in M365/Outlook at
`alejandroa@interworkoffice.com`. Gmail MCP (personal account) has no project emails.
Until M365 OAuth is connected, use `--file` or `--paste` to feed email content manually.

---

## What this command accepts

| Source type | What to look for |
|-------------|-----------------|
| FastField export (CSV) | project_number, form_name, submission_date, submitted_by |
| FastField email confirmation | Subject line with job # / project name, "submitted" or "completed" |
| WC report (PDF/DOCX/pasted) | Project name/number, completion date, signoff name |
| Email text | "work is complete", "job done", "final walkthrough", "punch list cleared" |
| Pasted note | Any text Alejandro pastes with project reference and completion claim |
| Folder scan | Looks for files containing project numbers + completion language |

---

## Step 1 — Parse input

Extract from whatever was provided:
- `project_number` — look for 4-digit number (e.g. 7364, #7053, "project 7499")
- `project_name_hint` — any name or location mentioned
- `completion_date` — parse any date mentioned as completion/submission/signoff date
- `submitted_by` — person name if present
- `source_type` — fastfield / wc_report / email / manual_note / folder_file
- `raw_evidence` — the relevant excerpt (max 500 chars) to attach to the record

---

## Step 2 — Match to Supabase project

```sql
SELECT id, project_number, name, status, scheduled_date,
       fastfield_submitted, completion_report_sent, actual_end_at, pm_assigned
FROM public.projects
WHERE project_number = '<parsed_number>'
   OR name ILIKE '%<name_hint>%'
ORDER BY project_number;
```

Assign match confidence:
- `high` — exact project_number match
- `medium` — name/location match, single result
- `low` — fuzzy match, multiple candidates → ask Alejandro to pick
- `none` — no match → write to open_loops as unmatched

---

## Step 3 — Evaluate current field state

For each matched project, check what's already set vs. what the evidence supports:

| Field | Proposed if |
|-------|-------------|
| `fastfield_submitted = true` | source_type = fastfield AND not already true |
| `completion_report_sent = true` | source_type = wc_report AND not already true |
| `actual_end_at = '<date>'` | completion_date parsed AND actual_end_at is NULL |
| `status = 'completed'` | fastfield_submitted OR completion_report_sent, AND status = 'scheduled' or 'in_progress', AND not a phase/scope-risk project |

**Never propose:**
- `vendor_confirmed`, `client_confirmed`, `access_confirmed` — these require explicit Alejandro action
- Status change if project name contains: Phase, Multi-Phase, Punch List, Walkthrough, Scope

---

## Step 4 — Flag exclusions

Do not propose status → completed for:
- Projects where `actual_end_at < scheduled_date` (suspicious date mismatch)
- Projects with open loops in `open_loops` table (status = 'open') or in `memory/open_loops/`
- Projects with "Phase", "Multi-Phase", "Punch List" in name
- Projects 7364 or 7447 (flagged by ChatGPT as possibly reopened — require manual review)

Surface these as flags, not proposals.

---

## Step 5 — Write open loop if no match or missing evidence

If project not matched OR evidence is insufficient:

Write to `memory/open_loops/intake_unmatched_<YYYYMMDD>_<slug>.md`:

```markdown
---
id: intake-<YYYYMMDD>-<NNN>
source: completion-intake
project:
person:
status: action-needed
priority: medium
created: <datetime>
updated: <datetime>
evidence_type: <fastfield|wc_report|email|manual_note>
---

Completion signal received but could not be matched to a project.

**Evidence excerpt:**
<raw_evidence>

**Parsed hints:** project_number=<N/A>, name_hint=<X>, date=<Y>

Review and link manually.
```

---

## Step 6 — Log to activity_log

For every proposed Supabase change (after Alejandro approves), insert:

```sql
INSERT INTO public.activity_log (project_id, actor, action, source, notes, created_at)
VALUES ('<project_id>', 'alejandro', 'status_update', 'completion-intake',
        'Source: <source_type>. Evidence: <evidence_excerpt>', NOW());
```

---

## Output format

```
## Completion Intake — [date] — [source_type]
Input: <file path or "pasted text"> | Source: <fastfield/wc_report/email/manual_note>

### Parsed
- Project number: 7053 (confidence: high)
- Project: Strategic Education Washington DC
- Completion date: 2026-03-21
- Submitted by: [name if found]
- Evidence: "[relevant excerpt]"

### Current field state
| Field | Current | Proposed |
|-------|---------|----------|
| fastfield_submitted | false | true |
| actual_end_at | NULL | 2026-03-21 |
| status | scheduled | completed |

### Flags
- ⚠️ actual_end_at matches scheduled_date exactly — verify this is real

### Proposed Supabase updates (NOT applied — require approval)
> Say "apply intake for 7053" to get the SQL for review.

UPDATE public.projects
SET fastfield_submitted = true,
    actual_end_at = '2026-03-21',
    status = 'completed',
    updated_at = NOW()
WHERE project_number = 7053;

### Open loops created (memory .md — automatic)
✅ memory/open_loops/intake_7053_fastfield_2026-06-26.md

### Unmatched signals
(none)
```

---

## Batch mode (--folder)

When scanning a folder:
1. List all files; show count
2. Process each file that contains a 4-digit project number reference
3. Group output by: matched (with proposals) / unmatched (with open loops)
4. Show summary table first, then per-project detail on request

---

## Rules

- **Never** auto-apply any Supabase update — all proposals require Alejandro approval
- **Never** set `vendor_confirmed`, `client_confirmed`, `access_confirmed`
- **Never** propose status = completed for phase/scope projects
- All Supabase writes must be logged to `activity_log`
- Memory open loop `.md` files are written automatically (Level 1)
- Supabase `open_loops` inserts require approval (Level 3)
- Every command output must label itself: `read-only` or `write-proposed`
- See `memory/references/interwork-command-center.md` for full permission policy
