# Environment Variable Setup Guide

Last updated: 2026-06-28

---

## Overview

The D:\ai-workstation system requires several environment variables to connect
external integrations. These must be set manually by Alejandro. They are never
stored in git, never pasted into Claude chat, and never printed by any script.

---

## Required Variables

| Variable | Purpose | Where to Find It |
|----------|---------|-----------------|
| `SUPABASE_URL` | Supabase project URL for interwork-command-center | Supabase dashboard > Settings > API > Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key for write access | Supabase dashboard > Settings > API > service_role (keep secret) |
| `OPENAI_API_KEY` | OpenAI API key for /ask-openai-review | platform.openai.com > API Keys |
| `HF_TOKEN` | HuggingFace token (optional -- faster model downloads) | huggingface.co > Settings > Access Tokens |

**DO NOT** paste any of these values into Claude chat. Claude should never see or
handle secret values directly.

---

## How to Set Variables (Method 1: Interactive Script)

Run this script locally in PowerShell. It uses secure input (values are masked):

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1
```

The script will:
- Prompt for each variable using masked input (like a password field)
- Skip any variable you press Enter on (leaves existing value unchanged)
- Never print the values
- Set at User scope (not Machine -- no admin required)
- Automatically run the readiness check when done

---

## How to Set Variables (Method 2: Manual PowerShell)

If you prefer to set variables directly, open PowerShell and run:

```powershell
# Set each one -- replace <value> with the actual secret
[System.Environment]::SetEnvironmentVariable('SUPABASE_URL', '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('HF_TOKEN', '<value>', 'User')
```

**Important:** Type these commands directly in PowerShell. Do not paste the commands
with real values into Claude chat, Teams, email, or any text field that may be logged.

---

## How to Verify

After setting, run the readiness check (reports present/missing only, never values):

```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1
```

Expected output when ready:
```
SUPABASE_URL               PRESENT  (value hidden)
SUPABASE_SERVICE_ROLE_KEY  PRESENT  (value hidden)
OPENAI_API_KEY             PRESENT  (value hidden)
HF_TOKEN                   PRESENT  (value hidden)
All required env vars present. Ready to connect integrations.
```

---

## After Setting Variables

1. **Restart Claude Code** -- env vars are loaded at startup; an open session will not see them.
2. Run `/dashboard-status` to test Supabase connectivity.
3. If Supabase works, proceed to reconnect M365 and other MCPs.

---

## What Requires Alejandro Manual Action

| Action | Why Manual |
|--------|-----------|
| Setting `SUPABASE_URL` | Secret -- never automated |
| Setting `SUPABASE_SERVICE_ROLE_KEY` | Secret -- never automated |
| Setting `OPENAI_API_KEY` | Secret -- never automated |
| Reauthorizing M365 OAuth | Requires browser login as Alejandro |
| Reauthorizing Read AI connector | Requires browser login |
| Reauthorizing Smartsheet MCP | Requires browser login |
| Activating Make.com FastField scenario | Requires Make.com login and test payload confirmation |
| Any Supabase write (INSERT/UPDATE/DELETE) | Requires explicit "approve" in chat |

---

## What Claude Can Do Without Secrets

- Run local RAG searches (rag-search, rag-status, find-open-loops)
- Read and update memory files
- Create local docs and scripts
- Run local smoke tests
- Show env var readiness (present/missing only, no values)

---

## Security Reminders

- Do not commit `.env` files
- Do not share `SUPABASE_SERVICE_ROLE_KEY` with non-admin parties
- The service role key bypasses Row Level Security -- treat like a root password
- If a key is ever accidentally exposed, rotate it immediately in the provider dashboard
- See `docs/SECRETS_POLICY.md` for full policy
