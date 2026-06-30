# InterWork AI Information Architecture — Final

_Last updated: 2026-06-30_

---

## Purpose

This document defines how information flows between the human operator (Alejandro), the AI systems (Claude Code, Claude Chat, ChatGPT), the data sources (Supabase, memory repo, FastField, Teams/Read AI), and the output channels (client confirmations, vendor dispatches, project updates).

---

## System Roles

| System | Role | Access |
|---|---|---|
| **Claude Code** | Repo operator — reads/writes memory, generates packs, runs safe scripts | Local repo + Supabase MCP (read-heavy) |
| **Claude Chat (Projects)** | Client/project intelligence — answers questions, drafts comms | Client knowledge packs uploaded per project |
| **ChatGPT** | Peer review and second opinion on plans and outputs | Receives structured briefs via temp file, never raw data |
| **Supabase** | Source of truth for project index, status, open loops | Read freely; writes require Alejandro approval |
| **Memory repo** | Source of truth for operating rules, client context, procedures | Read/write via Claude Code; committed to GitHub |
| **FastField** | Field form dispatch and completion signals | Webhook → Make.com → Supabase |
| **Teams/Read AI** | Inbound project signals, meeting notes, action items | Read-only via Graph API / Read AI MCP |

---

## Information Flow Diagram

```
[ Alejandro ] ──────────────────────────────────────────┐
      │                                                  │
      ▼                                                  ▼
[ Claude Code ]  ←── reads ──  [ Memory repo (GitHub) ] 
      │                              ↑ commits / pushes
      │ reads                        │
      ▼                         [ Claude Code writes ]
[ Supabase DB ]                      │
  - projects                    [ memory/clients/ ]
  - open_loops                  [ memory/inbox/ ]
  - v_project_health            [ docs/ ]
  - fastfield_webhook_events    [ claude_project_packs/ ]
      │                              │
      │                              ▼
[ FastField ]               [ Claude Chat Projects ]
  webhooks via Make.com       ← packs uploaded manually
      │                              │
      ▼                              ▼
[ Field PMs ]             [ Alejandro uses Chat for ]
  - receive forms            - client Q&A
  - complete work            - draft confirmations
  - return signals           - project briefings
                             - vendor comms
```

---

## Data Tiers

### Tier 1 — Always Available (Repo Memory)
Committed to GitHub. Accessible in any Claude Code or Chat session.
- `memory/clients/<client>/CLIENT_CONTEXT.md`
- `memory/procedures/`
- `memory/company_knowledge/`
- `claude_project_packs/<client>_knowledge_pack.md`

### Tier 2 — Live Data (Supabase)
Available when Supabase MCP is connected. Never auto-written without approval.
- Project index (`projects` table)
- Open loops (`open_loops` table)
- FastField events
- Project health view

### Tier 3 — Signal Sources (Read-only, Gated)
Require explicit session setup. Never stored raw in repo.
- Microsoft Teams (Graph API — read-only)
- Read AI meeting notes (MCP)
- Outlook/M365 (blocked unless Alejandro provides paste)

---

## AI Session Types

### Claude Code Session (this repo)
- Purpose: repo maintenance, memory updates, pack generation, safe script runs
- What it writes: memory files, docs, scripts, client packs
- What it never writes: .env, secrets, raw emails, Supabase writes without approval

### Claude Chat Session (Projects)
- Purpose: operational intelligence, client/vendor drafts, project Q&A
- Loaded with: client pack + company knowledge + current handoff
- What it never does: push to repo, modify Supabase, send messages

### ChatGPT Review Session
- Purpose: peer review of AI outputs, second opinion on plans
- Fed via: `feedback_loop/to_chatgpt.md` temp file
- What it never receives: raw project data, client emails, Supabase dumps

---

## Memory Sync Protocol

1. Claude Code session ends → run `/regenerate-handoff` equivalent
2. Updated files committed and pushed to GitHub
3. Before Claude Chat session → copy new `memory/inbox/claude_chat_start_handoff.md` as project context
4. Before ChatGPT review → write brief to `feedback_loop/to_chatgpt.md`
5. After ChatGPT review → save response to `feedback_loop/from_chatgpt.md`

---

## Approval Gates

| Action | Automatic | Requires Approval |
|---|---|---|
| Read Supabase | ✓ | — |
| Write memory files | ✓ | — |
| Commit and push to repo | ✓ (safe docs only) | If secrets scan flags anything |
| Write to Supabase | — | Always |
| Send client email/Teams | — | Always |
| Dispatch FastField | — | Always |
| Install new tools globally | — | Always |

---

## File Ownership Map

| Path | Owned By | Updated When |
|---|---|---|
| `memory/clients/` | Claude Code | After any client project update |
| `memory/inbox/claude_chat_start_handoff.md` | Claude Code | After each session |
| `claude_project_packs/` | Claude Code | On demand / after major updates |
| `docs/` | Claude Code | On architecture changes |
| `scripts/` | Claude Code | When new automation is added |
| `memory/MEMORY.md` | Claude Code | When memory files are added/removed |
