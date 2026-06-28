---
name: interwork-approval-rules
description: What Claude can do automatically vs. what requires Alejandro approval — the InterWork permission model
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Approval Rules
_Last updated: 2026-06-26_

---

## Approval Authority

**Alejandro Acosta** is the final approval authority for all risky or irreversible actions.

OpenAI/ChatGPT recommendations are advisory only. ChatGPT cannot approve production changes.
Claude cannot treat an OpenAI action plan as authorization to write to Supabase, send messages, or change project data.

---

## Allowed Automatically (No Approval Needed)

Claude may perform the following without asking:

- Read-only queries (Supabase, Smartsheet, Outlook/M365, Teams, Read AI)
- Project briefs and status summaries
- Dashboard mismatch reports
- Completion backlog reports
- Open loop proposals (memory `.md` files only)
- Draft emails, Teams messages, or communications
- Memory and RAG updates (local `.md` files)
- Local script updates and parser improvements
- Review-only SQL drafts (with ROLLBACK wrapper)
- Status reports and health checks
- RAG re-indexing
- Saving meeting notes to memory
- Identifying missing fields or gaps in project data

---

## Requires Alejandro Approval

Claude must stop and ask before performing any of the following:

### Supabase writes
- INSERT, UPDATE, or DELETE on any table
- Applying SQL migrations
- Schema changes (DDL)
- Enabling or modifying RLS policies

### Project status changes
- `status` field on any project (inquiry, scheduled, in_progress, completed, closed, cancelled)
- Marking a project completed or closed

### Confirmation booleans — never auto-set, ever
- `vendor_confirmed`
- `client_confirmed`
- `access_confirmed`

### Completion signal fields — require approval or confirmed evidence
- `fastfield_submitted`
- `completion_report_sent`
- `actual_end_at`

### Communications — draft is free, send requires approval
- Sending any email
- Sending any Teams message
- Any message that commits InterWork to a date, price, scope, or responsibility

### External commitments
- Pricing or quote decisions
- Client or vendor commitments of any kind
- Scope changes
- Scheduling commitments

### Data management
- Deleting or overwriting production data
- Clearing fields unless drafting a review-only SQL change

### Smartsheet
- Any insert or update to Smartsheet (Claude prepares; human applies)

---

## Special Rules

### ChatGPT / OpenAI
- ChatGPT provides strategic advice and risk review — it is not an approval authority.
- Claude cannot execute ChatGPT action plan items automatically.
- Every ChatGPT recommendation must be surfaced to Alejandro before implementation.
- The feedback loop is: Claude builds → ChatGPT reviews → Alejandro approves.

### Activity logging
- Every approved Supabase write should include an `activity_log` INSERT.
- Use `source = 'manual'` for Claude-initiated writes (no 'ai' enum value currently).
- Include `before_state` and `after_state` in jsonb where practical.

### Drafts vs. sends
- Drafting any communication is always allowed.
- Sending any communication always requires approval.
- "Draft ready" is not the same as "approved to send."

### Scope uncertainty
- If scope, dates, or commitments are unclear, ask Alejandro before surfacing anything to a client or vendor.
- Phrase uncertain information as "pending confirmation" in drafts.

---

## Quick Reference Card

| Action | Auto | Needs Approval |
|--------|------|---------------|
| Read any data source | ✅ | |
| Draft message or SQL | ✅ | |
| Memory/RAG write | ✅ | |
| Local script update | ✅ | |
| Status report | ✅ | |
| Send email | | ✅ |
| Send Teams message | | ✅ |
| Supabase INSERT/UPDATE/DELETE | | ✅ |
| Apply SQL migration | | ✅ |
| Change project status | | ✅ |
| Set vendor_confirmed | | ✅ |
| Set client_confirmed | | ✅ |
| Set access_confirmed | | ✅ |
| Set fastfield_submitted | | ✅ |
| Set completion_report_sent | | ✅ |
| Set actual_end_at | | ✅ |
| Enable RLS | | ✅ |
| Smartsheet write | | ✅ |
| Delete/overwrite production data | | ✅ |
| Commit to date/price/scope | | ✅ |
