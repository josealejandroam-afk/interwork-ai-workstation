# AI Workstation — Desktop

This is Alejandro's desktop AI workstation project.

## Current Status (2026-06-28) -- Phase 4 Complete

| Item | Status |
|------|--------|
| Desktop bootstrap | Complete |
| Steam cleanup (Batch 1 + 2) | Complete -- 250+ GB recovered on C: |
| Steam Batch 3 (RE Requiem, AoM, Buckshot to E:) | In progress |
| AI caches configured on D: | Done (D:\ai-cache\*, env vars set) |
| Repo location | Moved to D:\ai-workstation (master branch) |
| Laptop portable files imported | memory, commands, scripts, rag, feedback_loop, plans |
| Path audit (C: to D:) | Complete -- 0 operational C:\Users\1 references remaining |
| Secret scan | Clean -- no secret values in repo |
| RAG index | Healthy -- 24 memory files, ChromaDB + BM25 indexed |
| Local commands installed | rag-search, rag-status, find-open-loops (C:\Users\Owner\.claude\commands) |
| Env vars (SUPABASE_URL, etc.) | Not set -- run set_required_env_vars_interactive.ps1 locally |
| Live integrations | Not connected -- Supabase, M365, Smartsheet, Read AI all pending |
| C: archive | Intact at C:\Users\Owner\.claude -- do not delete yet |

## Installed and Verified

- Git 2.54.0
- Python 3.12.10 (use `py` launcher on Windows)
- uv 0.11.25

## Folder Structure

| Folder | Purpose |
|--------|---------|
| `memory/` | Persistent Claude memory files |
| `commands/` | Custom slash commands and scripts |
| `scripts/` | Utility and automation scripts |
| `rag/` | RAG pipeline and document ingestion |
| `docs/` | Documentation and reference material |
| `sql/` | SQL queries and schema files |
| `config/` | Configuration files (non-secret) |
| `logs/` | Log output (excluded from git) |

## Next Steps (when Alejandro returns)

See `docs/RETURN_CHECKLIST.md` for the short checklist and `docs/FIRST_DAY_RUNBOOK.md` for the full sequence.

Quick path to full operational status:

1. Run `workstation_status.ps1` to confirm local systems healthy
2. Run `set_required_env_vars_interactive.ps1` in a local PowerShell to set secrets
3. Restart Claude Code so env vars are loaded
4. Run `/dashboard-status` to confirm Supabase is live
5. Reconnect M365, Smartsheet, and Read AI MCPs in the MCP panel
6. Review held approvals before any Supabase writes (see `docs/NEXT_ACTION_QUEUE.md`)

## Key Documents

| Doc | Purpose |
|-----|---------|
| `docs/RETURN_CHECKLIST.md` | Short return-day checklist |
| `docs/FIRST_DAY_RUNBOOK.md` | Full 16-step return sequence |
| `docs/NEXT_ACTION_QUEUE.md` | Categorized action queue (ready now / blocked / held) |
| `docs/SAFE_COMMANDS_REFERENCE.md` | Which commands are safe now vs. need secrets/MCP |
| `docs/ENV_SETUP_GUIDE.md` | Where to find each secret and how to set it |
| `docs/EXTERNAL_INTEGRATION_GATES.md` | Per-integration status and unlock requirements |
| `docs/COMMAND_ACTIVATION_PLAN.md` | All 17 commands with activation tier |
| `docs/INTEGRATION_RESTORE_PLAN.md` | Step-by-step integration restore order |

## Permanent Rules

- Never write to Smartsheet (read-only, always)
- Never auto-apply Supabase status changes -- always present for approval first
- Never set vendor_confirmed / client_confirmed / access_confirmed without explicit evidence
- Never send Teams messages or emails without explicit "send it" confirmation
- Never paste secret values into Claude Code chat
