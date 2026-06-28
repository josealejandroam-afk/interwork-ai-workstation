# External Integration Gates

Last updated: 2026-06-28
Purpose: Per-integration status, unlock requirements, and permission boundaries.

---

## Supabase (interwork-command-center)

**Project ID:** hskgrxhdtgowagkfkjsw
**Current status:** CONNECTED — read-only queries active. Writes require explicit Alejandro approval.

| Gate | Status |
|------|--------|
| `SUPABASE_URL` env var | PRESENT |
| `SUPABASE_SERVICE_ROLE_KEY` env var | PRESENT |
| Supabase MCP in Claude Code | Connected (confirmed 2026-06-28) |
| Read-only test | PASSED — /dashboard-status and health review succeeded |
| Supabase writes | BLOCKED until explicit Alejandro approval, field by field |

**What Claude may do automatically:**
- Read-only SQL queries (SELECT)
- Status reports, health checks, backlog views

**What requires Alejandro approval:**
- Any INSERT, UPDATE, DELETE
- Status field changes (`status`, `fastfield_submitted`, `completion_report_sent`, `actual_end_at`)
- Setting `vendor_confirmed`, `client_confirmed`, `access_confirmed` (NEVER auto-set)
- RLS policy changes
- Schema migrations
- All writes must be executed in a transaction that includes an `activity_log` entry

**Held approvals (pending since 2026-06-26):**
- 6-project batch: 7374, 7499, 7498, 7347, 7472, 7482 -- proposed status = completed
- Project 7447: invalid actual_end_at (April 15 before June 16 start) -- fix draft ready
- Projects 7060, 7348: awaiting PM confirmation before status write (see review packet)

**Commands now available:**
`/dashboard-status`, `/project-health`, `/completion-backlog`, `/completion-intake`,
`/ff-sent`, `/fastfield-intake`

---

## OpenAI (ChatGPT review loop)

**Current status:** CONNECTED — `OPENAI_API_KEY` present (confirmed 2026-06-28).

| Gate | Status |
|------|--------|
| `OPENAI_API_KEY` env var | PRESENT |
| `feedback_loop/` directory on D: | Present (migrated) |

**What is needed before use:**
- Env var is set. `/ask-openai-review` and `/feedback-status` are available.

**What Claude may do automatically:**
- Build review packet from memory files
- Run secret scrubber on outbound content

**What requires Alejandro approval:**
- Any action items recommended by OpenAI review
- Sending packet if `to_chatgpt.md` is unchanged since last response

**Role clarification:** OpenAI/ChatGPT = reviewer/advisor only. Claude Code = builder.
Alejandro = final approval authority for all Supabase writes, status changes, sends.

**Commands unlocked:**
`/ask-openai-review`, `/feedback-status`

---

## FastField / Make.com Webhook

**Current status:** NOT active — scenario 5506328 inactive by design, pending test payload confirmation.

| Gate | Status |
|------|--------|
| Make.com scenario 5506328 | Inactive (by design — awaiting test payload) |
| Webhook credentials | Must be stored in local env vars, Make.com secret storage, or a secure secret manager — NOT in any repo file |
| Supabase connection | PRESENT (prerequisite met) |

**What is needed before activation (future step — requires explicit approval):**
1. Send a test FastField submission from the field
2. Verify the webhook payload lands in `fastfield_webhook_events` table
3. Review payload structure with Alejandro
4. Alejandro explicitly approves activating scenario 5506328

**Activation is a future step.** Do not activate Make.com scenario or configure webhooks until after the current read-only review and project status confirmation work is complete and Alejandro gives explicit go-ahead.

**What Claude may do automatically:**
- Read `fastfield_webhook_events` table (read-only)
- Propose project matches for incoming events

**What requires Alejandro approval:**
- Activating the Make.com scenario
- Setting `fastfield_submitted = true` on any project
- Any update to `fastfield_webhook_events` processing status

**Commands unlocked (read mode):**
`/fastfield-intake`, `/fastfield-assignment-watch`

**ACTIVATION BLOCKED UNTIL:** Test payload confirmed + Alejandro explicit approval

---

## Gmail (Personal Account)

**Current status:** NOT connected as Claude Code MCP

**IMPORTANT RULE:** Gmail (`jose.alejandro.a.m@gmail.com`) is a personal account.
It contains NO work project emails. Do NOT use Gmail as a work signal source.

**What Gmail is for:**
- Personal correspondence only
- NOT for WC reports, BOLs, vendor/client confirmations, FastField alerts
- Work email lives at Outlook/M365 (`alejandroa@interworkoffice.com`)

**What requires Alejandro approval:**
- Connecting Gmail MCP (optional -- was connected on laptop but is not a project signal source)

**Claude will never:**
- Search Gmail for project data
- Use Gmail emails to update Supabase project fields

---

## Teams / Microsoft 365 (Outlook + Teams)

**Current status:** NOT connected -- OAuth not yet reauthorized

| Gate | Status |
|------|--------|
| M365 MCP in Claude Code | NOT reconnected |
| Outlook work email | alejandroa@interworkoffice.com |
| Teams access | Same OAuth as Outlook via Microsoft Graph |

**What is needed before use:**
1. Open Claude Code MCP panel
2. Reconnect Microsoft 365 connector
3. Log in as `alejandroa@interworkoffice.com` when prompted

**What Claude may do automatically (after connection):**
- Read Teams messages (summarize, surface open questions)
- Read Outlook emails (WC reports, BOLs, vendor/client comms)
- Draft replies for Alejandro's review

**What requires Alejandro approval:**
- Sending any Teams message ("send it" explicit confirmation)
- Sending any Outlook email
- Using email content to update Supabase project fields

**Commands unlocked:**
`/teams-brief`, `/brief-me` (full mode), `/project-brief` (Tier 3 signals)

---

## Read AI (Meeting Summaries)

**Current status:** NOT connected as Claude Code CLI MCP

| Gate | Status |
|------|--------|
| Read AI in claude.ai app | Connected (was working on laptop) |
| Read AI in Claude Code CLI | NOT yet available as a connector |

**What is needed before use:**
1. Check Claude Code MCP connector list for Read AI availability
2. If available: connect via MCP panel
3. If not available: use Mode B (manual paste) for now

**What Claude may do automatically:**
- Mode B: accept pasted meeting content and process it
- Parse summary, action items, participants, topics
- Match meeting to Supabase project

**What requires Alejandro approval:**
- Any Supabase project field updates based on meeting content
- Any `open_loops` INSERT to Supabase

**Current workaround:** `/meeting-intake --paste` and `/readai-brief` Mode B
both work without the MCP connection.

---

## Smartsheet (Schedule Source)

**Current status:** NOT connected -- MCP not yet reauthorized

| Gate | Status |
|------|--------|
| Smartsheet MCP in Claude Code | NOT reconnected |

**PERMANENT RULE: Never write to Smartsheet.**

**What is needed before use:**
1. Open Claude Code MCP panel
2. Reconnect Smartsheet connector

**What Claude may do automatically (after connection):**
- Read schedule rows
- Surface rows with recent changes
- Match Smartsheet rows to Supabase projects

**What requires Alejandro approval:**
- Nothing to approve for reads
- Any Smartsheet write is PERMANENTLY BLOCKED regardless of approval

**Commands unlocked:** `/brief-me` Smartsheet source, `/project-brief` schedule tier

---

## ChatGPT Browser Handoff (send_to_chatgpt.py)

**Current status:** NOT connected -- requires Playwright browser automation

| Gate | Status |
|------|--------|
| `scripts/send_to_chatgpt.py` | Script present, paths updated to D: |
| `scripts/chatgpt_target_url.txt` | Needs conversation URL set by Alejandro |
| Playwright profile | `C:\Users\Owner\.playwright-profile` (check if exists) |

**What is needed before use:**
1. Open a ChatGPT conversation in Chrome
2. Copy the conversation URL
3. Save it to `D:\ai-workstation\scripts\chatgpt_target_url.txt`
4. Test: `uv run python D:\ai-workstation\scripts\send_to_chatgpt.py "test message"`

**What requires Alejandro approval:**
- Any message sent to ChatGPT (Playwright automation sends on his behalf)
- Review packets built by `/ask-openai-review` (reviewed before sending)

**Note:** The API-based route (`ask_openai_review.py`) is preferred over browser
automation. The browser route is a fallback for when the API is unavailable.

---

## Summary Table

| Integration | Status | Blocker / Note | Commands Available |
|------------|--------|----------------|-------------------|
| **Supabase** | **CONNECTED (read-only)** | Writes require explicit approval per field | /dashboard-status, /project-health, /completion-backlog, /completion-intake, /ff-sent, /fastfield-intake |
| **OpenAI API** | **CONNECTED** | None | /ask-openai-review, /feedback-status |
| FastField/Make | NOT active | Future step — test payload + explicit approval required before activation | /fastfield-intake (read mode) |
| Gmail | NOT connected as work source | Personal account only — not a work signal source | N/A |
| M365/Teams | NOT connected | OAuth re-auth pending | /teams-brief, /brief-me (full), /project-brief |
| Read AI | NOT connected (CLI) | MCP connector pending | /meeting-intake (Mode A), /readai-brief (Mode A) |
| Smartsheet | NOT connected | OAuth re-auth pending | /brief-me (Smartsheet source) |
| ChatGPT browser | NOT connected | URL file + Playwright profile | Fallback only |
| **Local RAG** | **CONNECTED** | None | /rag-search, /rag-status, /find-open-loops |
