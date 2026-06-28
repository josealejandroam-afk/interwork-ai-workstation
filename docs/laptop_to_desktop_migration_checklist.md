# Laptop → Desktop Migration Checklist

**Status:** Pending — do not copy files until Steam game moves finish and C: is fully clean.

---

## Safe to Copy from Laptop

These folders contain no secrets and can be transferred directly:

- `memory/` — Claude persistent memory files
- `commands/` — Custom slash commands and scripts
- `scripts/` — Utility and automation scripts
- `rag/` — RAG pipeline source code (not the Chroma database)
- `docs/` — Documentation and reference material
- `sql/` — SQL query drafts and schema files
- `templates/` — Prompt templates, config templates

---

## Do NOT Copy

These must stay on the laptop or be re-created manually per machine:

- `.env` files — API keys and secrets
- `tokens/` — Auth tokens, bearer tokens
- `secrets/` — Any secrets folder
- Browser profiles — Chrome, Firefox, Edge profiles with saved credentials
- Cached credentials — Windows Credential Manager entries, keyring entries
- Supabase service role keys — Never share across machines
- Webhook URLs containing secrets — Regenerate per environment
- `.venv/` or `venv/` — Local virtual environments (recreate with `uv sync`)
- `chroma/` or `chroma_db/` — Chroma vector database files (unless explicitly approved and re-indexed)
- `__pycache__/` — Python bytecode cache
- `logs/` — Session-specific log files

---

## Migration Options

| Method | Pros | Cons |
|--------|------|------|
| **OneDrive** | Already installed on both machines, syncs automatically | Avoid syncing `.env` — configure OneDrive selective sync |
| **GitHub private repo** | Clean version-controlled transfer, no secret risk | Requires secrets are already excluded from repo |
| **USB / external drive** | Works offline, full control | Manual, easy to accidentally copy excluded files |

---

## Recommended Path

1. Push portable files from laptop to a **private GitHub repo** (or use the existing ai-workstation repo if already on GitHub)
2. Pull on desktop into `C:\Users\Owner\Documents\ai-workstation\`
3. Recreate `.env` manually on the desktop — do not transfer it
4. Run `uv sync` to recreate the virtual environment from `pyproject.toml`
5. Re-index Chroma only after confirming source documents are present

### Secrets rule
Each machine gets its own `.env`. Never commit `.env`. Never transfer via cloud sync.

---

## Blockers Before Migration

- [ ] Steam game moves to E: must complete (RE Requiem, AoM, Buckshot Roulette)
- [ ] Verify C: free space is stable after Steam cleanup
- [ ] Move uv/pip caches to D: (env vars set — new installs will use D: automatically)
- [ ] Confirm ai-workstation repo is stable before pulling new content into it

---

*Created: 2026-06-28*
