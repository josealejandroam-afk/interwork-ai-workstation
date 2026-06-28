# AI Workstation — Desktop

This is Alejandro's desktop AI workstation project.

## Current Status (2026-06-28)

| Item | Status |
|------|--------|
| Desktop bootstrap | ✅ Complete |
| Steam cleanup (Batch 1 + 2) | ✅ Complete — 250+ GB recovered on C: |
| Steam Batch 3 (RE Requiem, AoM, Buckshot → E:) | 🔄 In progress |
| AI caches configured on D: | ✅ Done (`D:\ai-cache\*`, env vars set) |
| Repo location | ✅ Moved to `D:\ai-workstation` |
| Laptop portable files imported | ✅ memory, commands, scripts, rag, feedback_loop, plans |
| Secrets imported | ❌ Not imported — recreate `.env` locally per machine |
| RAG index rebuilt | ❌ Not yet — run `uv sync` then `uv run python ingest.py` |
| Integrations connected | ❌ Not yet — requires `.env` with API keys |

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

## Next Steps

1. Verify Steam Batch 3 complete (games on E:)
2. Create `.env` locally with API keys (not committed — see `docs/SECRETS_POLICY.md`)
3. Run `uv sync` inside `rag/` to install dependencies
4. Run `uv run python ingest.py` to rebuild RAG index
5. Connect integrations (Supabase, Make, Gmail, etc.)
6. Archive or remove `C:\Users\Owner\Documents\ai-workstation` C: copy
