# Cloud Repo Migration Plan

**Repo name:** interwork-ai-workstation  
**Visibility:** Private only  
**Date prepared:** 2026-06-29

---

## What Is Safe to Push

- All files tracked by git (`git ls-files`) — commands, scripts, memory, docs, config
- `.gitignore`, `README.md`, `CLAUDE.md`
- Secret *names* referenced in scripts (env var names, not values) — these are safe

## What Must Stay Local (Never Committed)

| Item | Why |
|------|-----|
| `.env` / `*.env` / `.env.*` | Contains API keys and connection strings |
| `secrets/`, `tokens/` | Sensitive credential files |
| `*.key`, `*.pem`, `*.p12`, `*.pfx` | Private keys and certificates |
| `local_settings*`, `webhook*` | May contain tokens or webhook URLs |
| `.venv/`, `venv/` | Python virtual environment (reproducible, not secret) |
| `node_modules/` | NPM packages (reproducible) |
| `rag/stores/`, `chroma/` | Local RAG vector database (rebuilt from source docs) |
| `*.sqlite`, `*.db` | Local databases |
| `cache/`, `.local/`, `credentials/` | Local state and credentials |
| `backups/`, `ai-workstation_imports/`, `*.zip` | Archive files |
| `D:\ai-cache\` | HuggingFace model weights (large, not secret) |

**Rule:** If in doubt, check `.gitignore` first. If not listed, do not commit until reviewed.

---

## Secret Scan Result (2026-06-29)

**CLEAN** — No actual secret values found in any tracked file.  
All keyword matches were env var *name* references in scripts and docs (not values).

Patterns checked: JWT tokens (`eyJ...`), OpenAI keys (`sk-...`), bearer tokens,  
key assignment patterns (`API_KEY=<value>`), service role strings with values.

---

## How to Clone on Another Computer

```powershell
# 1. Install prerequisites (see NEW_MACHINE_SETUP.md)

# 2. Clone the repo
git clone https://github.com/<org>/interwork-ai-workstation.git D:\ai-workstation

# 3. Set environment variables (see below — do NOT clone .env)

# 4. Rebuild local environment
cd D:\ai-workstation
uv sync          # Python deps from pyproject.toml / requirements
```

---

## How to Recreate Local Environment Variables

Secrets are stored in the **Windows Registry** (User scope), not in files.  
Set them on each new machine:

```powershell
[System.Environment]::SetEnvironmentVariable('SUPABASE_URL',              '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY',            '<value>', 'User')
[System.Environment]::SetEnvironmentVariable('HF_TOKEN',                  '<value>', 'User')  # optional
```

Retrieve current values **only on the original machine** before migrating:

```powershell
[System.Environment]::GetEnvironmentVariable('SUPABASE_URL',              'User')
[System.Environment]::GetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', 'User')
[System.Environment]::GetEnvironmentVariable('OPENAI_API_KEY',            'User')
```

**Never write these values into any file in the repo.**

---

## How to Rebuild the RAG Index Locally

The RAG vector store (`rag/stores/`) is excluded from git. Rebuild it from source docs:

```powershell
cd D:\ai-workstation\rag
uv run python ingest.py    # or the project ingest script
```

Verify with:

```powershell
.\scripts\rag_search.ps1 "FastField Make integration"
```

---

## How to Run Workstation Status Checks

```powershell
# Check env vars are set
.\scripts\check_env_readiness.ps1

# Full workstation status
.\scripts\workstation_status.ps1

# Supabase connection test (requires SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY)
# Run /dashboard-status in Claude Code
```

---

## Warnings

> **SECRETS ARE NEVER COMMITTED.**  
> `.env` files, API keys, tokens, webhook URLs, and service role keys must never appear in any committed file. Use Windows Registry or a secrets manager instead.

> **`.env` STAYS LOCAL ONLY.**  
> If a `.env` file exists locally, it is covered by `.gitignore`. Confirm with `git status` before every push.

> **Before every push, run:**
> ```powershell
> git status
> git diff --cached --name-only
> ```
> Verify no secret files appear in the output.
