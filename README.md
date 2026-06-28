# AI Workstation — Desktop

This is Alejandro's desktop AI workstation project. It is a clean bootstrap and does not yet contain the laptop workstation memory, secrets, or live integrations.

## Status

This repo was initialized on 2026-06-28 as a fresh desktop environment.
The following have been installed and verified:

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
