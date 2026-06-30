# AI Shared Context — InterWork Office
_Last updated: 2026-06-29_

---

## What This Is

This is the shared source of truth for ChatGPT and Claude in the InterWork Office AI operations system.

Claude Code and ChatGPT do not automatically share memory. This GitHub repo is the bridge — both AIs read from and write to the same markdown files here.

---

## How the System Works

```
Claude Code  ──reads/writes──►  GitHub repo (this repo)  ◄──reads──  ChatGPT
                                        │
                              structured docs, project cards,
                              daily handoffs, decisions, loops
                                        │
                              Supabase  ──► canonical project DB (writes require Alejandro approval)
                              Smartsheet ──► schedule source (read-only forever)
                              Outlook/M365 ──► work email signals (alejandroa@interworkoffice.com)
                              FastField ──► completion form signals (no API yet)
                              Teams ──► real-time project mentions
                              Read AI ──► meeting summaries
```

---

## Roles

| Actor | Role |
|-------|------|
| Alejandro Acosta | Final approval authority. Operations Project Manager. |
| Claude Code | Reads all sources. Drafts. Proposes. Commits to repo. Never sends or writes to Supabase without Alejandro approval. |
| ChatGPT | Reads this repo. Reviews Claude's proposals. Advises strategy. Cannot approve production changes. |
| Supabase | Canonical project database — 140 projects (confirmed 2026-06-29). Writes require explicit approval. |
| Smartsheet | Schedule source only. Never write. |

---

## What Lives Here (in This Repo)

| Location | Content |
|----------|---------|
| `memory/shared/` | Shared context, daily handoffs, open loops, project index, decisions, access status |
| `memory/projects/` | One file per active project with known facts, gaps, drafts, next actions |
| `memory/inbox/` | Async handoff channel between Claude and ChatGPT |
| `memory/procedures/` | Approval rules, communication rules, project lifecycle |
| `memory/references/` | Architecture, schema, people map, project types, integrations |
| `docs/` | Runbooks, operating rules, capability matrix, work queue |
| `commands/` | Claude slash command definitions |

---

## What Does NOT Live Here

- API keys, tokens, passwords, service keys, webhook URLs
- `.env` file contents
- Raw email bodies or full private meeting transcripts
- Database exports or credential files
- Supabase connection strings

---

## Source of Truth Hierarchy

1. **Supabase** — canonical for project status, confirmation booleans, dates
2. **This repo** — canonical for procedures, decisions, context, drafts
3. **Smartsheet** — schedule reference only (may lag Supabase)
4. **Chat memory** — temporary; treat as session context only

---

## AI-to-AI Bridge

The repo is the memory system. The bridge is the working channel. Both are in use.

```
Claude ↔ ChatGPT bridge  →  fast live collaboration, quick drafts, second opinions
Claude → GitHub memory   →  decisions, project facts, open loops, daily handoffs
GitHub memory → both AIs →  shared context that persists across sessions
```

**Two bridge mechanisms:**
- **OpenAI API** (`ask_openai_review.py` / `/ask-openai-review`) — structured review packets, action plans, advisory. Runs a secret scrubber before sending. Response saved to `feedback_loop/`.
- **Playwright browser** (`send_to_chatgpt.py`) — live chat in a Chrome tab. Requires the ChatGPT conversation to be open in Chrome with the URL saved to `scripts/chatgpt_target_url.txt`.

**Rule:** Bridge output that matters (decisions, confirmed facts, flags) must be summarized into `memory/shared/` or `memory/inbox/` before the session ends. Bridge conversations are not persistent — GitHub is.

Full bridge documentation: `docs/AI_TO_AI_BRIDGE.md`

---

## Key Files to Read First

1. `memory/shared/DAILY_HANDOFF.md` — what happened today and what's next
2. `memory/shared/OPEN_LOOPS.md` — unresolved items needing action
3. `memory/shared/PROJECT_INDEX.md` — all active projects at a glance
4. `memory/shared/ACCESS_STATUS.md` — which integrations are live vs. blocked
5. `memory/inbox/claude_to_chatgpt.md` — Claude's latest update for ChatGPT

---

## Operating Rules Summary

- Claude executes and proposes. ChatGPT reviews and advises. Alejandro approves.
- Drafting is always free. Sending always requires "send it" from Alejandro.
- Supabase writes always require explicit "approve" or "apply" from Alejandro.
- Smartsheet is read-only forever.
- Gmail (jose.alejandro.a.m@gmail.com) is personal — never use for work signals.
- Work email is Outlook/M365 (alejandroa@interworkoffice.com).

Full rules: `docs/OPERATING_RULES_FOR_COMPANY_CLAUDE.md`
