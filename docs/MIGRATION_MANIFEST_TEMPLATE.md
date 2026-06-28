# Laptop → Desktop Migration Manifest

Use this checklist when transferring workstation files from the laptop to the desktop.
Complete the Steam cleanup and repo move to D: before starting this migration.

---

## Safe to Copy

These folders contain no secrets and can be transferred via GitHub, OneDrive, or USB:

- [ ] `memory/` — Claude persistent memory files
- [ ] `commands/` — Custom slash commands
- [ ] `scripts/` — Utility and automation scripts
- [ ] `rag/` — RAG pipeline source code (not the Chroma database files)
- [ ] `docs/` — Documentation and reference material
- [ ] `sql/` — SQL query drafts and schema files
- [ ] `templates/` — Prompt templates, config templates
- [ ] Non-secret config examples (e.g., `config/example.yaml` — no real values)

---

## Do NOT Copy

These must stay on the laptop or be recreated manually on the desktop:

- [ ] `.env` — API keys and secrets (recreate manually)
- [ ] `secrets/` — Any secrets folder
- [ ] `tokens/` — Auth tokens, bearer tokens
- [ ] Browser profiles — Chrome, Firefox, Edge saved passwords and sessions
- [ ] Cached credentials — Windows Credential Manager entries
- [ ] Supabase service role keys — Never share across machines
- [ ] Webhook URLs containing secrets — Regenerate per environment if needed
- [ ] `.venv/` or `venv/` — Virtual environments (recreate with `uv sync`)
- [ ] `chroma/` or `chroma_db/` — Chroma vector DB files (unless explicitly approved for transfer)
- [ ] Model weights (`.bin`, `.gguf`, `.safetensors`) — Unless explicitly approved; re-download to D:\ai-cache\models instead

---

## Transfer Method Options

| Method | When to Use | Notes |
|--------|-------------|-------|
| **GitHub private repo** | Preferred for code/docs | Push from laptop, pull on desktop. Safest — secrets already excluded by .gitignore |
| **OneDrive** | For non-secret files only | Disable sync for secrets folders. Confirm .env is excluded before enabling |
| **USB / external drive** | Offline fallback | Manual control — easy to accidentally copy excluded files. Double-check before copying |

---

## Recommended Transfer Sequence

1. On the laptop: run `git status` to confirm no untracked secrets are staged
2. Push all safe files to the private GitHub repo
3. On the desktop: `git pull` into `D:\ai-workstation`
4. Manually recreate `.env` on the desktop from your password manager
5. Run `uv sync` to recreate the virtual environment
6. Re-index Chroma only after confirming source documents are present on D:
7. Test that API connections work before closing the laptop setup

---

## Pre-Migration Blockers

- [ ] Steam Batch 3 complete (RE Requiem, AoM, Buckshot on E:)
- [ ] C: free space verified stable
- [ ] ai-workstation repo moved to D:\ai-workstation
- [ ] AI cache env vars active in new terminal sessions

---

## Post-Migration Verification

- [ ] `memory/` contents load correctly in Claude Code
- [ ] `commands/` slash commands are recognized
- [ ] Scripts run without missing dependency errors
- [ ] RAG pipeline connects to Supabase (after .env is set up)
- [ ] No `.env` or secrets file appears in `git status`

---

*Template created: 2026-06-28 — fill in actual file lists from laptop before migrating*
