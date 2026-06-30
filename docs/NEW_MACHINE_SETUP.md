# New Machine Setup Guide

Use this guide when setting up interwork-ai-workstation on a new computer.

---

## Prerequisites

Install these before cloning:

| Tool | Purpose | Install |
|------|---------|---------|
| Git | Version control | https://git-scm.com |
| Python 3.11+ | Scripts and RAG | https://python.org |
| uv | Python package manager | `pip install uv` |
| GitHub CLI (`gh`) | Repo management | https://cli.github.com |
| Claude Code CLI | AI workstation shell | `npm install -g @anthropic-ai/claude-code` |

---

## Step 1 — Authenticate GitHub CLI

```powershell
gh auth login
# Choose: GitHub.com → HTTPS → Authenticate with browser
```

---

## Step 2 — Clone the Repo

```powershell
git clone https://github.com/<org>/interwork-ai-workstation.git D:\ai-workstation
cd D:\ai-workstation
```

---

## Step 3 — Set Environment Variables

Secrets live in the Windows Registry (User scope). Set them now:

```powershell
[System.Environment]::SetEnvironmentVariable('SUPABASE_URL',              '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY',            '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('HF_TOKEN',                  '<value>', 'User')  # optional
```

Get the values from your password manager or from the original machine (registry).  
**Never write values into a file in the repo.**

Verify they are set:

```powershell
.\scripts\check_env_readiness.ps1
```

---

## Step 4 — Install Python Dependencies

```powershell
cd D:\ai-workstation
uv sync
```

If `uv` is not available: `pip install -r requirements.txt`

---

## Step 5 — Rebuild the RAG Index

The vector store is not in the repo. Rebuild it from source documents:

```powershell
cd D:\ai-workstation\rag
uv run python ingest.py
```

Verify:

```powershell
.\scripts\rag_search.ps1 "FastField Make integration"
```

---

## Step 6 — Verify Workstation Status

```powershell
.\scripts\workstation_status.ps1
```

Expected output: all env vars present, RAG store populated, no errors.

---

## Step 7 — Connect Supabase MCP in Claude Code

In Claude Code settings, add the Supabase MCP server and point it at the  
`interwork-command-center` project. See `docs/CLOUD_REPO_MIGRATION_PLAN.md` for details.

---

## What Is NOT in the Repo

These must be recreated or sourced separately on each machine:

| Item | How to recreate |
|------|----------------|
| `.env` files | Do not create — use registry instead |
| `rag/stores/` (vector DB) | Run `uv run python ingest.py` |
| `.venv/` | Run `uv sync` |
| `D:\ai-cache\` | HuggingFace downloads automatically on first use |
| `backups/`, `ai-workstation_imports/` | Restore from external backup if needed |
| Make.com webhook config | Recreate in Make.com; see `docs/FASTFIELD_MAKE_REPAIR.md` |

---

## Security Reminders

- **Never commit `.env` files or secret values.**
- Run `git status` before every `git push` and verify no secret files are staged.
- All API keys and tokens stay in the Windows Registry or a secrets manager only.
- If you suspect a secret was committed: rotate the key immediately, then remove it from git history.
