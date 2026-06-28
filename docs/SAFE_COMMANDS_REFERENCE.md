# Safe Commands Reference

Last updated: 2026-06-28
Purpose: Which Claude Code slash commands can be used now vs. what they need first.

---

## Tier 1 -- Local Only: Safe Now (no secrets, no network)

These commands work immediately on the desktop workstation.

| Command | What It Does | How to Invoke |
|---------|-------------|---------------|
| `/rag-search` | Hybrid BM25 + vector search across memory files | `/rag-search "your query"` |
| `/rag-status` | Shows RAG index health, file count, ChromaDB status | `/rag-status` |
| `/find-open-loops` | Surfaces unresolved items, decisions, and follow-ups from memory | `/find-open-loops` |

Underlying scripts (usable outside Claude Code):

| Script | Command |
|--------|---------|
| RAG status | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1` |
| RAG search | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "query"` |
| RAG reindex | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_reindex.ps1` |
| Env var check | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1` |
| Env var setup | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1` |
| Workstation status | `powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\workstation_status.ps1` |

---

## Tier 2 -- Local Fallback: Usable Now (degrade gracefully without live data)

These commands work locally but give richer output when integrations are connected.

| Command | What Works Now | What's Missing Until Integration |
|---------|---------------|----------------------------------|
| `/brief-me` | Memory-based open loops and context | Smartsheet schedule, Teams messages, Outlook emails |
| `/meeting-intake --paste` | Manual paste of Read AI summary | Auto-fetch from Read AI MCP |
| `/readai-brief` | Mode B (paste) | Mode A (direct Read AI MCP pull) |
| `/project-brief` | Local memory context only | Supabase project data, Smartsheet schedule |
| `/fastfield-assignment-watch` | Local webhook config review | Live Supabase `fastfield_webhook_events` reads |

---

## Tier 3 -- Needs Supabase: Blocked Until Env Vars Set + Session Restarted

| Command | What It Does | Requires |
|---------|-------------|---------|
| `/dashboard-status` | Project counts by status, active/scheduled list | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| `/project-health` | Red projects, stalled workflows, risk flags | Same |
| `/completion-backlog` | Projects with completion reports pending | Same |
| `/completion-intake` | Process a completion document into Supabase | Same + Alejandro approval for any write |
| `/ff-sent` | Log FastField submission confirmation | Same + Alejandro approval |
| `/fastfield-intake` | Full mode -- match webhook to project | Same + Make.com test payload confirmed |

How to unblock: run `set_required_env_vars_interactive.ps1` locally, then restart Claude Code.

---

## Tier 4 -- Needs MCP Reauth: Blocked Until OAuth Reconnected

| Command | What It Does | Requires |
|---------|-------------|---------|
| `/teams-brief` | Summarize Teams messages, surface questions | M365 MCP reconnected (alejandroa@interworkoffice.com) |
| `/brief-me` (full) | All signal sources combined | M365 + Smartsheet + Supabase |
| `/project-brief` (full) | Schedule + DB + communications | Smartsheet + Supabase + M365 |
| `/readai-brief` (Mode A) | Auto-pull from Read AI | Read AI MCP reconnected |
| `/meeting-intake` (Mode A) | Auto-fetch meeting, process, propose update | Read AI + Supabase |

How to unblock: open Claude Code MCP panel, reconnect each integration manually.

---

## Tier 5 -- Needs OpenAI Key + feedback_loop/ Migration

| Command | What It Does | Requires |
|---------|-------------|---------|
| `/ask-openai-review` | Build and send review packet to OpenAI | OPENAI_API_KEY + D:\ai-workstation\feedback_loop\ |
| `/feedback-status` | Show status of recent OpenAI review requests | Same |

How to unblock:
1. Set `OPENAI_API_KEY` via `set_required_env_vars_interactive.ps1`
2. Copy `C:\Users\Owner\.claude\feedback_loop\` to `D:\ai-workstation\feedback_loop\`
3. Restart Claude Code

---

## Always Requires Alejandro Approval -- No Exceptions

These actions are never taken automatically regardless of which integrations are connected.

| Action | Rule |
|--------|------|
| Any Supabase INSERT, UPDATE, DELETE | Explicit "approve" required in chat |
| Project status field changes | Same -- no batch auto-apply |
| Setting `vendor_confirmed` | Never auto-set; requires explicit evidence |
| Setting `client_confirmed` | Same |
| Setting `access_confirmed` | Same |
| Sending any Teams message | "Send it" confirmation required |
| Sending any Outlook email | Same |
| Activating Make.com scenario 5506328 | Requires test payload confirmed + approval |
| Any write to Smartsheet | PERMANENTLY BLOCKED regardless of approval |
| Any ChatGPT browser automation send | Requires review of packet before sending |
| Deleting C: archive | Requires explicit instruction after D: confirmed stable |

---

## Quick Decision Guide

```
Is the command local-only (RAG, memory, file reads)?
  Yes → Safe to run now (Tier 1/2)

Does it query Supabase?
  Yes → Check env vars first: check_env_readiness.ps1
         If MISSING → run set_required_env_vars_interactive.ps1 first
         If PRESENT → restart Claude Code first, then proceed (Tier 3)

Does it read Teams, Outlook, Smartsheet, or Read AI?
  Yes → Reconnect that MCP in the MCP panel first (Tier 4)

Does it WRITE to Supabase, send a message, or update a status field?
  Yes → Stop. Present the proposed change and wait for "approve" (Always-Approval tier)

Does it write to Smartsheet?
  Yes → Block unconditionally. Not allowed under any circumstance.
```
