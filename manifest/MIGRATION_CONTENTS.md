# AI Workstation Migration — Export Manifest
**Created:** 2026-06-28
**Source laptop:** PersonalGaming
**Export staging path:** `C:\Users\1\Documents\ai-workstation-migration-export\`
**Recommended desktop import path:** `D:\ai-workstation\`

---

## What Was Copied (71 files)

### memory/ (24 files)
Source: `C:\Users\1\.claude\projects\C--Users-1\memory\`
All `.md` files copied recursively, preserving subfolder structure.

Subfolders included:
- `memory/` (root files: MEMORY.md, feedback_*.md, project_workstation_setup.md)
- `memory/clients/` (_template.md)
- `memory/open_loops/` (_template.md, backfill_review_2026-06-26.md, teams_2026-07-01_001.md)
- `memory/procedures/` (interwork_approval_rules.md, interwork_communication_rules.md, interwork_project_lifecycle.md)
- `memory/profile/` (user_profile.md)
- `memory/projects/` (_template.md, project-7492.md)
- `memory/references/` (fastfield_make_integration.md, interwork_ai_ops_master_context.md, interwork_command_center_schema.md, interwork_people_map.md, interwork_project_types.md, interwork-command-center.md)
- `memory/vendors/` (_template.md, just4wheels.md, sunset.md)

### commands/ (17 files)
Source: `C:\Users\1\.claude\commands\`
All slash command `.md` files:
ask-openai-review.md, brief-me.md, completion-backlog.md, completion-intake.md,
dashboard-status.md, fastfield-assignment-watch.md, fastfield-intake.md,
feedback-status.md, ff-sent.md, find-open-loops.md, meeting-intake.md,
project-brief.md, project-health.md, rag-search.md, rag-status.md,
readai-brief.md, teams-brief.md

### scripts/ (9 files + 5 SQL drafts)
Source: `C:\Users\1\scripts\`
Safe scripts copied:
- ask_openai_review.py
- bring_teams_to_front.ps1
- chatgpt_target_url.txt
- click_at.ps1
- parse_completion_email.py
- screenshot_screen.ps1
- send_to_chatgpt.py
- type_message.ps1
- ui.py

SQL drafts (`scripts/sql/`):
- draft_batch_complete_fastfield.sql
- draft_create_fastfield_webhook_events.sql
- draft_fix_7447_actual_end.sql
- draft_open_loops_table.sql
- draft_v_project_health.sql

### rag/ (8 files)
Source: `C:\Users\1\.claude\rag\` (source files only — no .venv, no stores)
- config.yaml ⚠️ contains absolute paths — update paths on destination before running
- ingest.py, rebuild.py, search.py, status.py, watch.py
- pyproject.toml, uv.lock

### feedback_loop/ (4 files)
Source: `C:\Users\1\.claude\feedback_loop\`
- action_plan.md, from_chatgpt.md, loop_log.md, to_chatgpt.md

### plans/ (1 file)
Source: `C:\Users\1\.claude\plans\`
- mighty-tickling-brooks.md

### claude_root/ (3 files)
Source: `C:\Users\1\.claude\`
- settings.json (feature flags and UI settings)
- settings.local.json (allowed permissions list)
- AGENT_PERMISSIONS.md

---

## What Was Excluded (12 items)

| Item | Location | Reason |
|------|----------|--------|
| fastfield_webhook_config.txt | scripts/ | Contains TOKEN_SECRET and full webhook URL — active credential |
| .credentials.json | .claude/ | MCP/API credentials |
| history.jsonl | .claude/ | Full Claude Code session history (44KB) — personal/sensitive |
| daemon.lock | .claude/ | Runtime process lock |
| daemon.log | .claude/ | Runtime log |
| daemon.status.json | .claude/ | Runtime status |
| mcp-needs-auth-cache.json | .claude/ | Cached auth state |
| .last-cleanup | .claude/ | Runtime marker |
| .last-update-result.json | .claude/ | Runtime marker |
| .venv/ | rag/ | Virtual environment — ~500MB, not portable; must run `uv sync` on destination |
| stores/ | rag/ | Chroma DB + SQLite index — machine-specific; must run `uv run python ingest.py` on destination |
| logs/ | rag/ | Runtime logs |
| __pycache__/ | scripts/ | Compiled bytecode — not portable |

---

## Secret Scan Results
Scan ran against all staged text files (.md, .py, .ps1, .txt, .yaml, .toml, .json, .sql, .lock).
**5 pattern matches found — all confirmed false positives:**
- settings.local.json (×2): Commands that READ OPENAI_API_KEY from Windows env — no stored value
- ask-openai-review.md: Same — instructions to read from env
- feedback_token_handling.md: Rule saying to display "REDACTED" — not an actual token
- ask_openai_review.py: Secret scrubber regex checking for "service_role" — not a secret value

**No actual secret values found in staged files.**

---

## Missing Expected Folders
- `C:\Users\1\Documents\ai-workstation` — NOT FOUND (referenced in original request but does not exist on this machine)
- `C:\Users\1\rag` — NOT FOUND (RAG is at `C:\Users\1\.claude\rag\`)

---

## Recommended Desktop Import Steps

1. Copy zip to desktop, extract to `D:\ai-workstation\`
2. Place memory files: `D:\ai-workstation\memory\` → configure Claude Code memory root
3. Place commands: copy `commands\*.md` to `%USERPROFILE%\.claude\commands\`
4. Place scripts: `D:\ai-workstation\scripts\` (update any hardcoded paths inside .py files)
5. RAG setup on destination:
   a. Copy `rag\` folder to `D:\ai-workstation\rag\`
   b. Edit `config.yaml` — update all absolute paths from `C:/Users/1/` to the destination paths
   c. Run: `uv sync` (installs dependencies)
   d. Run: `uv run python ingest.py` (rebuilds index from memory files)
6. Secrets to re-configure on desktop (NOT in this zip):
   - `OPENAI_API_KEY` — set as Windows environment variable
   - FastField webhook token — re-create in Make.com and save to new config file

---

*Generated by Claude Code on PersonalGaming — 2026-06-28*
