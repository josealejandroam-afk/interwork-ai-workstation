# /ask-openai-review

Send the current review packet to OpenAI and receive a structured review with action plan.
Never executes recommendations automatically. All Supabase writes, status changes, and
message sends still require Alejandro approval.

---

## Roles (always include in every packet)

| Role | Party | Responsibility |
|------|-------|----------------|
| Builder / Operator | Claude Code | Builds commands, queries data, drafts SQL, proposes actions |
| Reviewer / Advisor | OpenAI / ChatGPT | Reviews work, identifies gaps, advises on priorities |
| Approval Authority | Alejandro | Final say on all Supabase writes, status changes, sends |

OpenAI only knows what Claude includes in the packet. Always prepend the Review Context
Summary so the reviewer has full system context without asking for it.

---

## Step 0 — Build the packet

The script handles this automatically. It:

1. Reads the `## Review Context Summary` section from:
   `memory/references/interwork_ai_ops_master_context.md`

2. Prepends it to `feedback_loop/to_chatgpt.md` under the heading `## Review Packet`

3. Runs a secret scrubber — aborts if any of the following appear in outbound text:
   - JWT tokens (`eyJ...`)
   - OpenAI API keys (`sk-...`)
   - Supabase service role keys or `SUPABASE_KEY`
   - PEM blocks (`-----BEGIN`)
   - Any key assignment strings

The assembled packet always contains:

### System role summary
- Claude Code = builder/operator
- OpenAI/ChatGPT = reviewer/advisor
- Alejandro = final approval authority

### Current architecture
- Supabase = canonical write target
- Smartsheet = read-only scheduling source
- Memory/RAG = historical context, decisions, procedures
- Outlook/M365/Teams/Read AI = live signal sources (read-only); Gmail = personal account only, not a work signal source
- Claude Code = operations engine

### Command inventory
/dashboard-status, /project-health, /completion-backlog, /completion-intake,
/readai-brief, /meeting-intake, /teams-brief, /rag-status, /rag-search,
/ask-openai-review, /feedback-status

### Database objects
- open_loops table — applied
- v_project_health view — applied
- activity_log — pre-existing
- RLS policies — NOT applied
- communications schema changes — NOT applied

### Current blockers
- M365/Teams OAuth not complete
- Read AI visible in app, not available in Claude Code MCP CLI
- FastField direct API not connected; manual/file intake only
- Work email is Outlook/M365 (alejandroa@interworkoffice.com); Gmail MCP = personal account only, no project data
- Health alerts noisy until completion/status backfill done

### Held approvals (never apply without explicit "approve")
- 6-project batch: 7374, 7499, 7498, 7347, 7472, 7482 → status = completed
- 7447 actual_end_at correction (invalid date)
- RLS policies
- Communications table changes
- vendor_confirmed / client_confirmed / access_confirmed updates
- Any Smartsheet insert requests

### Permission model
Claude may do automatically:
- read-only queries, status reports
- memory/RAG writes, local file updates
- parser improvements, script updates
- review-only SQL drafts

Claude must ask Alejandro before:
- Any Supabase write (INSERT, UPDATE, DELETE)
- Status field changes
- RLS changes
- Confirmation boolean updates (vendor_confirmed, client_confirmed, access_confirmed)
- Sending Outlook emails or Teams messages
- Any client or vendor commitments
- Smartsheet inserts
- Deleting or overwriting production data

### Current priority
Data reliability first:
1. Clean completion backlog (status backfill)
2. Build completion signal intake (WC report, FastField email/export)
3. Verify evidence before proposing updates
4. Reduce false health alerts
5. Only then expand Outlook/Teams/Read AI automation (Gmail is personal-only, never a work signal)

### Recent key decisions
- 7053: hold until June 30 (final punchlist in scope)
- 7447: invalid actual_end_at (April 15 before June 16 start); fix awaits approval
- activity_log source='manual' for Claude-initiated writes
- vendor_confirmed/client_confirmed/access_confirmed: never auto-set

---

## Step 1 — Verify input file

Check that `to_chatgpt.md` has content:
```
D:\ai-workstation\feedback_loop\to_chatgpt.md
```

If the file hasn't changed since the last response in `from_chatgpt.md`, warn before
sending to avoid duplicate loops.

If the file is empty or missing: prompt Alejandro to describe what to review, then write it.

For complex questions, pull additional context from RAG before writing the file:
```powershell
# example: search for relevant decisions or architecture notes
uv run python D:\ai-workstation\rag\search.py "completion signal intake"
```

---

## Step 2 — Run the script

```powershell
$env:OPENAI_API_KEY = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User")
python D:\ai-workstation\scripts\ask_openai_review.py
```

Optional model override:
```powershell
python D:\ai-workstation\scripts\ask_openai_review.py --model o4-mini
```

The script prints:
- `Context: N chars prepended from master context file.`
- `Packet: N chars total`
- The extracted action plan on stdout

---

## Step 3 — Read and present the response

Read `from_chatgpt.md` and `action_plan.md` and present:

```
## OpenAI Review — [timestamp]
Model: gpt-4o | Packet: N chars

### Analysis summary
[3-5 bullet points from the Review & Analysis section]

### Action Plan
[numbered items from action_plan.md, with priority labels]

---
> None of these items have been executed.
> Say "do item N" to proceed with a specific step.
> Supabase writes and status changes require explicit Alejandro approval.
```

---

## Step 4 — Log the loop

Append to `feedback_loop/loop_log.md`:
```
- [2026-06-26 18:30 UTC] Model: gpt-4o | Packet: 2400 chars | Action items: 5 | Topic: completion backlog review
```

---

## Step 5 — Update master context if new decisions made

If the response includes a new decision or confirmed direction, update the
`## Key decisions` section in:
`memory/references/interwork_ai_ops_master_context.md`

Then re-index RAG:
```powershell
uv run python D:\ai-workstation\rag\ingest.py
```

---

## Rules

- Never execute action plan items automatically
- Never expose OPENAI_API_KEY, Supabase service role key, JWT tokens, or any secret in output
- Abort if secret scrubber detects a secret in outbound content
- If API fails: print error, suggest fix, do not retry automatically
- If input file unchanged since last response: warn before sending
- If master context file is missing: warn but still send (with packet only)
