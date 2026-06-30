# Start Here for AI — InterWork AI Memory Layer
_Last updated: 2026-06-30_

---

## What This Repo Is

This is the **durable AI memory layer** for InterWork Office Solutions.

It holds project cards, client context, open loops, operating rules, and procedures.
It is committed to GitHub so every AI session can read the same facts.

This is **not** the live dashboard. The dashboard lives in Supabase / Vercel.
The dashboard snapshot in this repo is a point-in-time copy and may be stale.

---

## How to Navigate This Repo

Use the files in this `memory/ai_index/` folder as fast lookup before going deeper.

| File | What it answers |
|---|---|
| `CLIENT_ROSTER.md` | What clients exist? What are their slugs? Which has a bootstrap or pack? |
| `PROJECT_INDEX.md` | What projects exist? Where is the project card? |
| `OPEN_LOOPS_SUMMARY.md` | What is currently pending across clients and projects? |
| `DASHBOARD_STATUS.md` | What does the dashboard show right now (snapshot)? |

---

## Lookup Flow

```
START_HERE_FOR_AI.md
        ↓
CLIENT_ROSTER.md → find client slug
        ↓
PROJECT_INDEX.md → find project slug + source path
        ↓
Fetch: memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md
       memory/clients/<client_slug>/projects/<project_slug>/OPEN_LOOPS.md
       memory/clients/<client_slug>/projects/<project_slug>/NOTES.md
```

---

## Raw GitHub URL Base

All files can be fetched via raw GitHub URL:

```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/<path>
```

Example — this file:
```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md
```

Example — a project card:
```
https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/uipath/projects/unknown_1450_broadway_move_out/PROJECT_CARD.md
```

---

## Source Priority

When multiple sources disagree, use this order:

1. **Supabase / live dashboard** — operational ground truth (requires live access)
2. **Dashboard snapshot** (`memory/ai_index/DASHBOARD_STATUS.md`) — stale if >1 day old
3. **Client knowledge pack** (`claude_project_packs/`) — use for contacts/routing; stale for status/dates
4. **Project card** (`memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md`) — best source for scope, contacts, notes
5. **Bootstrap file** (`claude_project_bootstraps/<slug>_bootstrap.md`) — routing only, not project facts

If dashboard and project card conflict → **flag the conflict**, do not silently pick one.

---

## What Claude Chat Can Do From This Repo

- Answer questions about project scope, contacts, schedule, location
- Draft client-facing emails and Teams messages (do not send without approval)
- Identify open loops and what needs resolution
- Propose a Claude Code handoff when repo updates are needed

## What Claude Chat Cannot Do

- Send emails or Teams messages without Alejandro saying "send it"
- Write to Supabase without approval
- Invent project numbers, dates, contacts, or statuses
- Push changes to the repo (that is Claude Code's job)

---

## How to Trigger a Repo Update

Draft a handoff in this format and tell Claude Code to execute:

```
Claude Code Handoff — <Client> [Project]

New confirmed facts:
- [fact 1]
- [fact 2]

Update:
memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md
```

---

## Key Company Context Files

| File | URL suffix |
|---|---|
| START_HERE (company rules) | `memory/company_knowledge/START_HERE.md` |
| Communication rules | `memory/company_knowledge/COMMUNICATION_RULES.md` |
| Access and safety rules | `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md` |
| Repo lookup rules | `memory/company_knowledge/REPO_LOOKUP_RULES.md` |

---

## Sole Approval Authority

**Alejandro Acosta** is the only person who can approve:
- Sending emails or Teams messages
- Writing to Supabase
- Deploying code to Vercel
- Any action that affects shared systems outside this repo

_When in doubt, draft and wait for "send it" or "approve"._
