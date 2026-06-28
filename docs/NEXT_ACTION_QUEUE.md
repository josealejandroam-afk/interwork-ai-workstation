# Next Action Queue

Last updated: 2026-06-28
For: Alejandro Acosta -- first session back on desktop workstation

Actions are grouped by what is needed to unblock them.
See `docs/FIRST_DAY_RUNBOOK.md` for the exact step sequence.

---

## READY NOW -- No secrets, no MCPs, no network required

| # | Action | How |
|---|--------|-----|
| 1 | Verify RAG is healthy | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1` |
| 2 | Run a local search query | `/rag-search "your topic"` or `rag_search.ps1 "query"` |
| 3 | Review open loops from memory | `/find-open-loops` |
| 4 | Review first-day sequence | `docs/FIRST_DAY_RUNBOOK.md` |
| 5 | Review what integrations need | `docs/EXTERNAL_INTEGRATION_GATES.md` |
| 6 | Review which commands are live | `docs/COMMAND_ACTIVATION_PLAN.md` |
| 7 | Reindex RAG (if files changed) | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_reindex.ps1` |
| 8 | Check env var status | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1` |

---

## NEEDS ALEJANDRO PRESENT -- Manual steps, no delegation

| # | Action | Where |
|---|--------|-------|
| 1 | Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY | Run `set_required_env_vars_interactive.ps1` in local PowerShell |
| 2 | Set OPENAI_API_KEY | Same script |
| 3 | Restart Claude Code after setting env vars | Close and reopen from D:\ai-workstation |
| 4 | Reauthorize M365 / Outlook / Teams OAuth | Claude Code MCP panel > Microsoft 365 > Log in as alejandroa@interworkoffice.com |
| 5 | Reauthorize Smartsheet MCP | Claude Code MCP panel > Smartsheet |
| 6 | Reauthorize or connect Read AI MCP | Claude Code MCP panel (check if available) |
| 7 | Set ChatGPT browser conversation URL | Save URL to `D:\ai-workstation\scripts\chatgpt_target_url.txt` |
| 8 | Confirm C: archive is intact before deleting | `Test-Path "C:\Users\Owner\.claude"` -- leave until fully operational on D: |

---

## NEEDS SECRETS -- Do not proceed until Alejandro has set env vars

| # | Action | Blocker |
|---|--------|---------|
| 1 | `/dashboard-status` | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| 2 | `/project-health` | Same |
| 3 | `/completion-backlog` | Same |
| 4 | `/completion-intake` | Same |
| 5 | `/ff-sent` | Same |
| 6 | `/ask-openai-review` | OPENAI_API_KEY + feedback_loop/ migration |
| 7 | Supabase 6-project batch approval (7374, 7499, 7498, 7347, 7472, 7482) | Supabase connected + Alejandro explicit "approve" |
| 8 | Project 7447 actual_end_at fix | Supabase connected + Alejandro explicit "approve" |

---

## NEEDS MCP REAUTHORIZATION -- Held since laptop migration

| # | Integration | Action Waiting |
|---|-------------|---------------|
| 1 | Microsoft 365 | Read Teams messages and Outlook emails |
| 2 | Smartsheet | Read schedule rows, match to Supabase projects |
| 3 | Read AI (if available as CLI MCP) | Auto-ingest meeting summaries |

Workaround while MCP is offline:
- Teams/Outlook: paste content manually, then use `/brief-me` or `/meeting-intake --paste`
- Read AI: use `/meeting-intake --paste` (Mode B)
- Smartsheet: not readable without MCP -- use known project context from memory

---

## NEEDS TEST PAYLOAD CONFIRMED -- Do not activate until tested

| # | Action | Blocker |
|---|--------|---------|
| 1 | Activate Make.com FastField scenario 5506328 | Test FastField submission must land in `fastfield_webhook_events` table first |
| 2 | Set `fastfield_submitted = true` on any project | FastField/Make confirmed working + Alejandro approval |
| 3 | Set `vendor_confirmed`, `client_confirmed`, `access_confirmed` | NEVER auto-set -- explicit evidence required |

---

## DO NOT TOUCH UNATTENDED -- Held approvals from prior session

These actions were proposed before the migration. They are ready to execute but require
Alejandro to say "approve" explicitly in chat after reviewing.

| # | Action | Status |
|---|--------|--------|
| 1 | Set status = completed for projects 7374, 7499, 7498, 7347, 7472, 7482 | HELD -- proposed 2026-06-26, not yet approved |
| 2 | Fix project 7447 actual_end_at (invalid date: April 15 before June 16 start) | HELD -- fix draft ready, awaiting approval |
| 3 | RLS policy changes on Supabase | HELD -- requires explicit approval |
| 4 | Communications table schema changes | HELD -- requires explicit approval |
| 5 | Delete C: archive (`C:\Users\Owner\.claude`) | HELD -- do not delete until fully operational on D: |
| 6 | Send any Teams message or Outlook email | NEVER auto-send -- always requires "send it" |
| 7 | Write to Smartsheet | PERMANENTLY BLOCKED -- read-only forever |

---

## Integration Restore Order (condensed)

Full details in `docs/INTEGRATION_RESTORE_PLAN.md`.

```
1. Set env vars (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY)
2. Restart Claude Code
3. /dashboard-status  -- confirms Supabase live
4. Reconnect M365 MCP in MCP panel
5. Reconnect Smartsheet MCP in MCP panel
6. Check Read AI MCP availability
7. Copy feedback_loop/ from C: to D: (for OpenAI review)
8. Confirm FastField webhook config file at D:\ai-workstation\scripts\fastfield_webhook_config.txt
9. Test FastField submission (before activating Make.com scenario)
```

---

## Held Approvals Reference

These are carried forward from before the migration. Confirm they are still current
before applying any of them.

| Project | Proposed Change | Proposed By |
|---------|----------------|-------------|
| 7374, 7499, 7498, 7347, 7472, 7482 | status = completed | Claude (2026-06-26) |
| 7447 | Fix actual_end_at (invalid date) | Claude (2026-06-26) |
