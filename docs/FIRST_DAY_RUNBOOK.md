# First Day Runbook

For: Alejandro Acosta
When: First session back on the desktop workstation after migration
Last updated: 2026-06-28

This runbook is the exact step-by-step sequence for returning to full
operational status on the new workstation. Follow in order.

---

## Pre-checks (before opening Claude Code)

### Step 1 -- Confirm repo location

Open PowerShell and confirm:

```powershell
Set-Location D:\ai-workstation
git status
git log -3 --oneline
```

Expected: `nothing to commit, working tree clean` at `b3c805d` or later.

### Step 2 -- Confirm C: archive is intact (do not delete yet)

```powershell
Test-Path "C:\Users\Owner\.claude"
```

Expected: `True`. Leave the C: archive untouched until you are fully operational on D:.

---

## Local Systems (no secrets required)

### Step 3 -- Run RAG status

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1
```

Expected:
- Memory files: 24
- ChromaDB: Found
- Index: Healthy

If unhealthy: run `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_reindex.ps1`

### Step 4 -- Test a local search

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "InterWork project status"
```

Expected: results with `score=` values above 0.5 referencing command-center or project files.

### Step 5 -- Check env var readiness

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1
```

Expected at this point: all vars MISSING. This is fine -- you set them in the next step.

---

## Secret Setup (manual, local PowerShell only)

### Step 6 -- Set required environment variables

**DO NOT paste secret values into Claude chat.**

Run the interactive setup script in a local PowerShell window:

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1
```

Set at minimum:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `OPENAI_API_KEY`

See `docs/ENV_SETUP_GUIDE.md` for where to find each value.

### Step 7 -- Verify env vars are set

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1
```

Expected: `PRESENT (value hidden)` for SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY.

### Step 8 -- Restart Claude Code

Close and reopen Claude Code so the new env vars are loaded.
Open from: `D:\ai-workstation` as the working directory.

---

## Integration Restoration (in Claude Code)

### Step 9 -- Test Supabase connection

In Claude Code chat:

```
/dashboard-status
```

Expected: project counts by status, list of active/scheduled projects.
If error: check that env vars are set and session was restarted.

### Step 10 -- Reauthorize M365 / Outlook / Teams

In Claude Code, open the MCP panel. Reconnect:
- Microsoft 365 (Outlook + Teams)

Work email: `alejandroa@interworkoffice.com`

After reconnecting, test:
```
/teams-brief
```

### Step 11 -- Reauthorize Read AI

In Claude Code MCP panel, reconnect Read AI connector.

Test:
```
/readai-brief
```

If Read AI MCP is not yet available in Claude Code CLI, use Mode B (manual paste).

### Step 12 -- Reauthorize Smartsheet

In Claude Code MCP panel, reconnect Smartsheet.

**Rule: Never write to Smartsheet. Read-only only.**

### Step 13 -- Restore feedback_loop/ (optional)

If you want /ask-openai-review to work:

```powershell
# From a PowerShell window
Copy-Item "C:\Users\Owner\.claude\feedback_loop" "D:\ai-workstation\feedback_loop" -Recurse
```

Verify the files copied correctly before using /ask-openai-review.

---

## First Operational Run

### Step 14 -- Run morning brief

```
/brief-me
```

Expected: open loops, recent memory updates, suggested next actions.

### Step 15 -- Review completion backlog

```
/completion-backlog
```

Review the stalled projects list. Do not update any Supabase fields without review.

**Held approvals from previous session (require explicit "approve"):**
- 6-project batch: 7374, 7499, 7498, 7347, 7472, 7482 -- proposed status = completed
- Project 7447: invalid actual_end_at correction
- RLS policies
- Communications table changes

### Step 16 -- Project health check

```
/project-health
```

Review red projects. Confirm any proposed updates before applying.

---

## What NOT to Do

- Do not write to Smartsheet (ever from Claude)
- Do not auto-apply project status changes -- always review proposals
- Do not set vendor_confirmed / client_confirmed / access_confirmed without explicit evidence
- Do not send emails or Teams messages without saying "send it"
- Do not delete the C: archive until fully confident on D:
- Do not activate the Make.com FastField scenario until a test payload is confirmed

---

## Useful Local Commands (always available, no secrets needed)

| Command | How to Run |
|---------|-----------|
| RAG status | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1` |
| RAG search | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "your query"` |
| RAG reindex | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_reindex.ps1` |
| Env check | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1` |
| Set env vars | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1` |

## Support Documents

| Doc | Purpose |
|-----|---------|
| `docs/ENV_SETUP_GUIDE.md` | Full guide to setting env vars |
| `docs/EXTERNAL_INTEGRATION_GATES.md` | Per-integration status and unlock requirements |
| `docs/COMMAND_ACTIVATION_PLAN.md` | Which commands are safe now vs. need secrets |
| `docs/NEXT_ACTION_QUEUE.md` | Prioritized action queue for return day |
| `docs/INTEGRATION_RESTORE_PLAN.md` | Step-by-step integration restore order |
