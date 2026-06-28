# AI Workstation — Desktop

This is Alejandro's desktop AI workstation project.

## Current Status (2026-06-28) — Post-return, live Supabase read-only active

| Item | Status |
|------|--------|
| Desktop bootstrap | Complete |
| Repo location | D:\ai-workstation (master branch) |
| Path audit (C: to D:) | Complete — 0 operational C:\Users\1 references remaining |
| Secret scan | Clean — no secret values in repo |
| RAG index | Healthy — 24 memory files, ChromaDB + BM25 indexed |
| Local commands installed | rag-search, rag-status, find-open-loops |
| Env vars (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY) | **PRESENT** — set and loaded |
| Supabase connection | **CONNECTED** — read-only confirmed 2026-06-28 |
| Dashboard frontend | https://interwork-command-center.vercel.app/ |
| Supabase writes | Blocked — require explicit Alejandro approval per field |
| M365 / Teams / Smartsheet / Read AI | Not yet reconnected — OAuth re-auth pending |
| Make.com FastField webhook | Not active — pending test payload + explicit approval |
| C: archive | Intact at C:\Users\Owner\.claude — do not delete yet |

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

## Current Focus (2026-06-28)

Steps 1–4 complete. Supabase is live and read-only review is done.

Immediate next actions:
1. Send confirmation drafts to Frank Barrett (7060) and Pedro Martinez (7348) — see `docs/PROJECT_STATUS_CONFIRMATION_DRAFTS.md`
2. Reconnect M365, Smartsheet, and Read AI MCPs in the MCP panel (when ready)
3. Review held approvals before any Supabase writes — see `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`

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
| `docs/DASHBOARD_URL.md` | Vercel dashboard URL and architecture clarification |
| `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` | Required procedure for any Supabase write |
| `docs/CODEX_REVIEW_ACTIONS.md` | Codex safety review log and remaining decision points |

## Permanent Rules

- Never write to Smartsheet (read-only, always)
- Never auto-apply Supabase status changes -- always present for approval first
- Never set vendor_confirmed / client_confirmed / access_confirmed without explicit evidence
- Never send Teams messages or emails without explicit "send it" confirmation
- Never paste secret values into Claude Code chat
