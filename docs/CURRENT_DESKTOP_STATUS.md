# Current Desktop Status

Last updated: 2026-06-28
Prepared by: Claude Code (unattended local setup session)

---

## What Is Complete

| Component | Status | Notes |
|-----------|--------|-------|
| Repo migrated to D: | Done | `D:\ai-workstation`, branch `master` |
| `rag/config.yaml` paths | Done | All point to D: only |
| `uv sync` dependencies | Done | 105 packages in `rag\.venv` |
| `ingest.py` index | Done | 24 files, 68 chunks in ChromaDB |
| `search.py` smoke tests | Done | 8 queries, all passed |
| `search.py` cp1252 fix | Done | Committed |
| Helper scripts | Done | `scripts\rag_search.ps1`, `rag_reindex.ps1`, `rag_status.ps1` |
| Docs | Done | `DESKTOP_RAG_VERIFICATION.md`, `COMMANDS_INVENTORY.md`, this file |
| AI cache on D: | Done | `D:\ai-cache\huggingface` (in use, no symlinks warning) |
| Memory files (24 .md) | Done | Indexed and searchable |

---

## What Is NOT Connected Yet

| Integration | Status | Blocker |
|------------|--------|---------|
| Supabase (interwork-command-center) | NOT connected | Needs `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` recreated manually |
| OpenAI / ChatGPT API | NOT connected | Needs `OPENAI_API_KEY` recreated manually |
| M365 / Outlook / Teams Graph API | NOT connected | Needs OAuth re-authorization in Claude Code |
| Read AI MCP | NOT connected | Visible in claude.ai app; not yet in Claude Code CLI |
| Make.com (FastField webhook) | NOT connected | Webhook URL not yet restored; integration was Phase 2 complete on laptop |
| FastField direct API | NOT connected | No API available — manual/file intake only |
| Smartsheet MCP | NOT connected | Needs re-authorization |
| Gmail MCP | NOT connected | Personal account only; no project data |

---

## Secrets That Need to Be Recreated Manually

These must be set by Alejandro. Claude will never request or store them.

| Secret | Where to set | Purpose |
|--------|-------------|---------|
| `SUPABASE_URL` | Windows user env var or `.env` | Supabase project connection |
| `SUPABASE_SERVICE_ROLE_KEY` | Windows user env var or `.env` | Supabase write access |
| `OPENAI_API_KEY` | Windows user env var | `/ask-openai-review` command |
| `HF_TOKEN` | Windows user env var (optional) | Faster HuggingFace downloads; non-blocking |
| Make.com webhook URL | Restore in FastField settings | FastField submission intake |
| M365 OAuth | Claude Code `/mcp` panel | Teams + Outlook integration |
| Read AI OAuth | Claude Code MCP CLI setup | Meeting intake automation |

**Policy:** Do not paste secrets into chat. Set as Windows user-level environment variables via System Properties or PowerShell `[System.Environment]::SetEnvironmentVariable(...)`.

---

## What Should NOT Be Touched Unattended

- Any Supabase writes (INSERT, UPDATE, DELETE) — require Alejandro approval
- Any Smartsheet writes — never write, read-only
- `vendor_confirmed`, `client_confirmed`, `access_confirmed` fields — never auto-set
- Email sends (Outlook/Teams/Gmail) — always require approval
- RLS policy changes — require explicit approval
- `status` field changes on projects — require approval
- Old C: archive copy at `C:\Users\Owner\.claude\` — do not delete yet
- Any file outside `D:\ai-workstation` and `D:\ai-cache`
- Docker, WSL, Windows system config, drivers, firewall

---

## Command Path Issue (Action Needed)

The imported slash commands in `D:\ai-workstation\commands\` still reference old laptop paths:

- `C:\Users\1\.claude\rag\search.py` (should be `D:\ai-workstation\rag\search.py`)
- `C:\Users\1\.claude\rag\ingest.py` (should be `D:\ai-workstation\rag\ingest.py`)
- `C:\Users\1\scripts\` (should be `D:\ai-workstation\scripts\`)
- `C:\Users\1\.claude\projects\C--Users-1\memory\` (should be `D:\ai-workstation\memory\`)

See `COMMANDS_INVENTORY.md` for full list of which commands need updates.
The helper scripts in `D:\ai-workstation\scripts\` use correct D: paths and can be used now.

---

## Exact Next Step for Alejandro When He Returns

**Step 1 — Review this file and `COMMANDS_INVENTORY.md`**
Confirm the command path update plan (safe local edits, no secrets involved).

**Step 2 — Recreate secrets as Windows user env vars**
Set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY` via PowerShell:
```powershell
[System.Environment]::SetEnvironmentVariable("SUPABASE_URL", "<value>", "User")
[System.Environment]::SetEnvironmentVariable("SUPABASE_SERVICE_ROLE_KEY", "<value>", "User")
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "<value>", "User")
```

**Step 3 — Test Supabase connection**
Run `/dashboard-status` and confirm it reads the interwork-command-center database.

**Step 4 — Re-authorize M365 / Read AI / Smartsheet MCPs**
Use Claude Code MCP panel to reconnect OAuth integrations.

**Step 5 — Update command paths (safe, local)**
Say: "Update command files to use D: paths" — Claude will do this in one pass.

**Step 6 — Run `/brief-me` for first full morning briefing on the new workstation**
