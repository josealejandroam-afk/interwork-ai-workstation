# InterWork Office Solutions — Company Knowledge Base Bootstrap
_Upload this file to the "InterWork Office Solutions Knowledge Base" Claude Project._
_This is a company-level bootstrap — not a client project bootstrap._
_Last updated: 2026-07-01_

---

## What This Claude Project Is

This Claude Project is the **company-level knowledge base** for InterWork Office Solutions.

Use it for:
- Operational status across all projects (who's working today, what's at risk)
- Company rules — communication, approvals, access, safety
- Cross-client questions — open loops, schedule overview, escalations
- Drafting emails and messages before routing to the right client project
- General questions about how InterWork operates

For client-specific project work, use the appropriate **client Claude Project** instead.

---

## Company Overview

InterWork Office Solutions is a commercial moving, decommissioning, and technology installation company based in the Philadelphia area. Alejandro Acosta is the primary operator and sole approval authority.

---

## At the Start of Each Chat — Fetch These Files

0. **AI index (fast lookup):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md`

   Lookup flow, source priority, client roster pointer, and project index pointer. Start here.

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Live dashboard API (operational status — use this first):**
   `https://interwork-command-center.vercel.app/api/ai/dashboard-summary`

   Returns live counts and today/tomorrow/at-risk rows from Supabase. No auth needed. Confirmed live 2026-06-30.
   Fallback if unavailable: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Open loops (cross-client pending items):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/OPEN_LOOPS_SUMMARY.md`

4. **Communication rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/COMMUNICATION_RULES.md`

---

## Additional Company Knowledge — Fetch When Relevant

| File | When to fetch |
|---|---|
| `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md` | Approvals, what's blocked, what requires Alejandro sign-off |
| `memory/company_knowledge/KEY_PEOPLE.md` | Who is who at InterWork |
| `memory/company_knowledge/OPERATING_WORKFLOW.md` | How a project moves from quote to closeout |
| `memory/company_knowledge/INTERWORK_OVERVIEW.md` | Company background and service capabilities |
| `memory/company_knowledge/GLOBAL_OPEN_LOOPS.md` | System-level unresolved items affecting all projects |

Raw GitHub base for all files:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Live APIs — Use Before Fetching Repo Files

**Dashboard summary** (counts + today/tomorrow/at-risk rows):
`GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary`

**Search** (project/client/location/PM/scope lookup, max 25 results):
`GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>`

Examples: `?q=at_risk`, `?q=Dallas`, `?q=7553`, `?q=Frank+Barrett`, `?q=decom`

---

## Navigating to Client Projects

1. Use search API first: `GET .../api/ai/search?q=<project number or client name>`
2. Client roster: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/CLIENT_ROSTER.md`
3. Project index: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/PROJECT_INDEX.md`
4. Then fetch: `memory/clients/<client_slug>/CLIENT_CONTEXT.md` + relevant project card

---

## What This Claude Project Can Do

- Answer operational questions (who's working today, what's at risk, counts by category)
- Look up company rules, communication format, approval requirements
- Draft emails and Teams messages (Alejandro approves all sends)
- Identify cross-client open loops and what needs resolution
- Route to the right client folder via the AI index

## What This Claude Project Cannot Do

- Send emails or Teams messages without Alejandro saying "send it"
- Write to Supabase or Smartsheet without approval
- Invent project numbers, dates, contacts, or statuses
- Push changes to the repo (Claude Code only)

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the relevant file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

When new durable facts appear in this session:

```
Claude Code Handoff — [Client / Project or Company-level]

New confirmed facts:
- [fact 1]
- [fact 2]

Update:
memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md
  --- OR ---
memory/company_knowledge/<file>.md
```

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan client folders without a specific client identified — use search or index first.
- Do not send emails or Teams messages — draft only, Alejandro approves all sends.
- Do not write to Supabase or Smartsheet without approval.
- Alejandro Acosta is the sole approval authority for all actions affecting shared systems.
