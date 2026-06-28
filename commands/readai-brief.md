# /readai-brief

Pull recent meetings from Read AI and surface what needs Alejandro's attention.
Read-only. Never writes to Supabase, Smartsheet, Outlook, or Teams.

---

## Mode detection

**Check whether Read AI MCP is available before running.**

Try calling `list_meetings`. If it errors or returns an auth failure:
- Announce: "Read AI MCP unavailable — running in Mode B (manual input)"
- Switch to Mode B below

If it succeeds: run Mode A.

---

## Mode A — Live Read AI MCP

### Step 1 — List recent meetings

```
list_meetings(limit=10, expand=["summary","action_items","key_questions","topics"])
```

Do NOT request `transcript` by default.

### Step 2 → Step 5 — same as shared steps below

---

## Mode B — Manual input (MCP unavailable)

Accept any of the following as input. Process whichever is provided:

| Input type | How to use |
|-----------|-----------|
| Pasted meeting summary | User pastes Read AI summary text directly into the prompt |
| Read AI email digest | User forwards the Read AI email; parse subject + body |
| Exported JSON / CSV | User provides file path or pastes content |
| Manual transcript | User pastes raw transcript text |

Parse the provided content to extract:
- Meeting title (from subject line, heading, or filename)
- Date/time (from header or content)
- Participants (attendees list or From/To fields)
- Summary (body or summary section)
- Action items (look for "Action Items", "Next Steps", "TODO" sections)
- Key questions (look for "Questions", "Decisions", "Open Items" sections)
- Topics (infer from headings or summary)

If any field is missing, note it as `not provided` — do not invent content.

---

## Shared steps (both modes)

### Step 2 — Project matching (per meeting)

Attempt to match each meeting to a Supabase project using this priority:

1. **Project number** — 4-digit number in title, notes, or participant context → high confidence
2. **Client / title / location / date** — fuzzy match against `projects.name`; known client names → medium confidence
3. **Participant email domain** — match domain against known client organizations → medium/low confidence
4. **Name similarity only** → low confidence, flag as uncertain

Query to check Supabase (Mode A and B):
```sql
SELECT project_number, name, status, scheduled_date
FROM public.projects
WHERE status NOT IN ('completed','closed','cancelled')
ORDER BY scheduled_date ASC;
```

### Step 3 — Needs-attention scan

Flag a meeting if:
- Action item assigned to Alejandro or unassigned
- Key question has no answer in the summary
- Participant mentioned a deadline ≤7 days away
- Matched project is in the completion backlog (past scheduled date, no signal)
- Meeting has no matched project (potential ungoverned work)

### Step 4 — Output

```
## Read AI Brief — [date]
Source: Read AI [Mode A: live MCP / Mode B: manual input] | [N] meetings

---

### [Meeting Title]
**Date:** [datetime] | **Duration:** [N min if known]
**Participants:** [names / emails]
**Project match:** [#XXXX name] — confidence: high/medium/low | unmatched

**Summary:**
[summary]

**Topics:** [topic1, topic2]

**Action Items:**
- [ ] [action] — [person] — due: [date or "unspecified"]

**Key Questions (open):**
- [question]

**Needs Alejandro attention:** ✅ / —
[reason if flagged]

---

### Flags
- [meeting]: [reason]

### Unmatched Meetings
- [title] — [date] — no project found; check manually

### Next step
Run `/meeting-intake <meeting_id>` (Mode A) or `/meeting-intake --paste` (Mode B)
to go deep, save notes, and create open loops for any meeting.
```

---

## Rules

- Read AI is read-only
- Do not write to Smartsheet
- Do not change any Supabase project fields
- Do not change confirmed fields (vendor_confirmed, client_confirmed, access_confirmed)
- Do not send emails or Teams messages
- All Supabase proposals require explicit Alejandro approval
- See `memory/references/interwork-command-center.md` for full permission policy
