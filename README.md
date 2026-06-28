# AI Workstation — Desktop

This is Alejandro's desktop AI workstation project. It is a clean bootstrap and does not yet contain the laptop workstation memory, secrets, or live integrations.

## Current Status (2026-06-28)

| Item | Status |
|------|--------|
| Desktop bootstrap | ✅ Complete |
| Steam cleanup (Batch 1 + 2) | ✅ Complete — 250+ GB recovered on C: |
| Steam Batch 3 (RE Requiem, AoM, Buckshot → E:) | 🔄 In progress |
| AI caches configured on D: | ✅ Done (`D:\ai-cache\*`, env vars set) |
| Repo location | ⏳ Temporarily at `C:\Users\Owner\Documents\ai-workstation` |
| Final repo target | `D:\ai-workstation` — move after Steam finishes |
| Laptop migration | Not started — see `docs/MIGRATION_MANIFEST_TEMPLATE.md` |

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

- Receive portable workstation files from laptop
- Set up .env with API keys (not committed)
- Connect integrations (Supabase, Make, Gmail, etc.)
- Initialize RAG pipeline
