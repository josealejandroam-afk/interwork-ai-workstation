# Return-Day Checklist

For: Alejandro Acosta
Purpose: Confirm all local systems are ready before connecting live integrations.
Full sequence with commands: see `docs/FIRST_DAY_RUNBOOK.md`

---

## Before Opening Claude Code

- [ ] Confirm you are on the desktop workstation (not the laptop)
- [ ] Confirm the C: archive is still intact -- do NOT delete yet
      `Test-Path "C:\Users\Owner\.claude"` should return `True`
- [ ] Confirm any laptop temporary network share or user account created during
      migration has been removed or locked (manual check -- desktop network settings)

---

## Open Claude Code

- [ ] Open Claude Code from `D:\ai-workstation` as working directory
      (not from C:, not from a shortcut pointing to the old laptop path)

---

## Confirm Local Systems (run before anything else)

- [ ] Run RAG status check:
      `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1`
      Expected: Memory files 24, ChromaDB Found, Index Healthy

- [ ] Run overall workstation status:
      `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\workstation_status.ps1`
      Expected: branch master, RAG healthy, env vars MISSING (that is correct at this point)

- [ ] Run env var check (values never shown):
      `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1`
      Expected at this point: all 4 MISSING -- that is fine

---

## Set Environment Variables (local PowerShell only)

- [ ] Open a local PowerShell window (not Claude Code chat)
- [ ] Run:
      `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1`
- [ ] Enter values when prompted (input is masked):
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_SERVICE_ROLE_KEY
  - [ ] OPENAI_API_KEY
  - [ ] HF_TOKEN (optional -- press Enter to skip)
- [ ] Confirm script reports `PRESENT (value hidden)` for each required var
- [ ] Do NOT paste any secret values into Claude Code chat

---

## Restart Claude Code

- [ ] Close Claude Code completely
- [ ] Reopen from `D:\ai-workstation`
      (new session picks up the env vars set above)

---

## Test Supabase Connection

- [ ] In Claude Code chat:
      `/dashboard-status`
      Expected: project counts by status, list of active/scheduled projects
- [ ] If error: run `check_env_readiness.ps1` again and confirm PRESENT before debugging

---

## Reauthorize External MCPs (in Claude Code MCP panel)

- [ ] Microsoft 365 -- log in as `alejandroa@interworkoffice.com`
      Test after: `/teams-brief`
- [ ] Smartsheet -- reconnect (read-only; NEVER write to Smartsheet)
      Test after: part of `/brief-me`
- [ ] Read AI -- reconnect if available as CLI MCP connector
      Fallback if not available: `/meeting-intake --paste` (Mode B)

---

## First Operational Run

- [ ] `/brief-me` -- open loops, recent memory, suggested next actions
- [ ] `/completion-backlog` -- review stalled projects list (no updates without approval)
- [ ] Review held approvals before any Supabase write:
  - Projects 7374, 7499, 7498, 7347, 7472, 7482 -- proposed status = completed
  - Project 7447 -- invalid actual_end_at correction

---

## Permanent Rules (never need re-checking -- always apply)

- [ ] Never write to Smartsheet (ever, regardless of context)
- [ ] Never set `vendor_confirmed`, `client_confirmed`, `access_confirmed` without explicit evidence
- [ ] Never send Teams messages or emails without saying "send it" explicitly
- [ ] Never auto-apply project status changes -- always review proposals first
- [ ] Never paste secret values into Claude Code chat
- [ ] Never activate Make.com FastField scenario 5506328 until test payload is confirmed
- [ ] Never delete the C: archive until fully confident on D:
