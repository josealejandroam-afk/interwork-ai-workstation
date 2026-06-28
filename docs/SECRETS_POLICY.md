# Secrets Policy

This policy applies to all work done on this workstation and any files committed to this repository.

---

## Never Commit

The following must **never** appear in any committed file, log, or document:

- API keys (Anthropic, OpenAI, Supabase, etc.)
- Bearer tokens or auth tokens
- Webhook URLs that contain secrets or signing keys
- `.env` files of any kind
- Browser profiles or session cookies
- Cached credentials (Windows Credential Manager exports, keyring dumps)
- Supabase service role keys or JWT secrets
- Private SSH keys or PEM files
- Database connection strings with embedded passwords

---

## Local .env Only

- All secrets live in a `.env` file at the project root
- `.env` is listed in `.gitignore` and must never be staged or committed
- Before committing, always run `git diff --staged` and `git status` to verify no `.env` or secret file is included

---

## Cloud Storage

- Do **not** sync `.env` files or secrets folders to OneDrive, Google Drive, or any auto-sync location unless explicitly approved and the files are encrypted
- GitHub is for code only — no secrets, even in private repos
- If a secret accidentally gets committed: rotate it immediately, then remove it from git history

---

## Per-Machine Setup

- Each machine (laptop, desktop, server) has its own local `.env`
- Secrets are never transferred across machines via cloud sync, USB, or copy-paste in plaintext
- When setting up a new machine, recreate secrets manually from your password manager or secrets vault

---

## Pre-Commit Checklist

Before every commit:

- [ ] `git status` — no `.env`, no `secrets/`, no `tokens/` in staged files
- [ ] `git diff --staged` — no API keys, tokens, or connection strings visible in diff
- [ ] `.gitignore` includes `.env`, `*.env`, `secrets/`, `tokens/`, `*.key`, `*.pem`

---

## .gitignore Reference

The following patterns are already in this repo's `.gitignore`:

```
.env
*.env
secrets/
tokens/
*.key
*.pem
*.sqlite
*.db
chroma/
__pycache__/
.venv/
logs/*.log
```

---

*Last updated: 2026-06-28*
