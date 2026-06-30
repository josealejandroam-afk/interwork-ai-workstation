# AI Memory Sync Runbook

_Last updated: 2026-06-30_

---

## Purpose

Step-by-step procedures for keeping the AI memory system in sync across Claude Code sessions, Claude Chat sessions, and ChatGPT peer reviews.

---

## When to Run a Sync

- After any Claude Code session that updated project data or memory files
- Before starting a Claude Chat session on a new machine
- After pulling the repo on a new machine (like this work laptop)
- After a major project milestone (completion, phase change, new client)
- After adding a new client or vendor

---

## Procedure 1 — End of Claude Code Session

```
1. Run: git status
2. Review changed files — scan for secrets (no tokens, URLs with keys, .env content)
3. Commit changed memory/docs/scripts files:
   git add memory/ docs/ scripts/ claude_project_packs/
   git commit -m "Memory sync: <brief description>"
   git push origin main
4. Regenerate handoff:
   Tell Claude Code: "Regenerate memory/inbox/claude_chat_start_handoff.md from current state"
5. Commit and push the updated handoff
```

---

## Procedure 2 — Start Claude Chat Session

```
1. Pull latest repo on the machine you're on:
   git pull --ff-only
2. Open: memory/inbox/claude_chat_start_handoff.md
3. Copy the full file contents
4. Open Claude Chat (target project or new conversation)
5. Paste with prefix:
   "Read the following handoff as your current source of truth for the InterWork AI workstation.
   Follow the operating rules, blocked-access notes, and current work queue exactly.
   [paste contents]"
6. Wait for Claude Chat to confirm it has read and summarize active/blocked/available
```

---

## Procedure 3 — Upload Client Knowledge Pack to Claude Chat Project

```
1. Pull latest repo
2. Navigate to: claude_project_packs/
3. Identify the pack file: <client>_knowledge_pack.md
4. In Claude Chat:
   - Open the target client Project (or create one)
   - Click "Add content" or "Upload file"
   - Upload the .md pack file
5. Start chat — Claude Chat will have client context loaded
6. To refresh: regenerate the pack in Claude Code, push, re-upload
```

---

## Procedure 4 — New Machine Setup (Work Laptop / Desktop Switch)

```
1. Clone repo:
   git init <target_folder>
   git remote add origin https://github.com/josealejandroam-afk/interwork-ai-workstation.git
   git fetch origin
   git checkout -b main origin/main
2. Confirm: git status (should show clean + untracked .claude/)
3. Add .claude/ to .gitignore if not already there (it should be)
4. Proceed with normal session start
```

---

## Procedure 5 — Regenerate Client Knowledge Pack

```
Tell Claude Code:
"Regenerate the client knowledge pack for <client> at
claude_project_packs/<client>_knowledge_pack.md
using memory/clients/<client>/CLIENT_CONTEXT.md and all project cards."

Claude Code will:
1. Read the client context and all project cards
2. Write a single-file knowledge pack
3. Commit and push

You then upload the pack file to the Claude Chat Project for that client.
```

---

## Procedure 6 — ChatGPT Peer Review

```
1. Write a structured brief to: feedback_loop/to_chatgpt.md
   Include: what you want reviewed, the output, and specific questions
   Never include: raw emails, Supabase dumps, tokens, or full transcripts
2. Send to ChatGPT (desktop app or Chrome — not Claude Code auto-send)
3. Save response to: feedback_loop/from_chatgpt.md
4. If action items result: create an open loop or update memory
```

---

## Secret Scan Checklist (Before Any Commit)

Run mentally or use grep:

```powershell
# In repo root — flag any of these patterns:
Select-String -Path ".\**\*" -Pattern "sk-|Bearer |SUPABASE_SERVICE|webhook.*token|password\s*=" -Recurse -Exclude ".git"
```

Never commit if any of the following are present in changed files:
- [ ] API keys (sk-, anth-, anything resembling a token)
- [ ] Bearer tokens or Authorization headers with values
- [ ] Supabase service role keys or JWT secrets
- [ ] Webhook URLs containing tokens or signing keys
- [ ] Passwords or credentials in plain text
- [ ] `.env` file content
- [ ] Raw email body text
- [ ] Full meeting transcripts
- [ ] Screenshots or binary attachments
- [ ] `local_sources/` file paths with data

---

## Repo Structure Reference

```
ai-workstation/
├── memory/
│   ├── MEMORY.md              ← index, always loaded
│   ├── clients/               ← one folder per client
│   ├── company_knowledge/     ← operating rules, START_HERE
│   ├── inbox/                 ← handoff files for Chat sessions
│   ├── procedures/            ← approval rules, comms rules, lifecycle
│   ├── references/            ← people map, schema, project types
│   └── projects/              ← per-project memory files
├── docs/                      ← architecture, runbooks, policy docs
├── claude_project_packs/      ← standalone packs for Claude Chat Projects
├── scripts/                   ← safe PowerShell and Python scripts
├── plans/                     ← implementation and migration plans
├── rag/                       ← RAG index config (stores excluded from git)
└── feedback_loop/             ← ChatGPT review exchange files
```
