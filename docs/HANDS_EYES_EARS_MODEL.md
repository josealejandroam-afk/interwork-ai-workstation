# Hands, Eyes, and Ears Model — InterWork AI System
_Created: 2026-06-30_

---

## Purpose

This document defines what each AI system can perceive (Eyes), receive (Ears), and act on (Hands).
It is the operating model for the InterWork AI layer.

---

## The Three Roles

### Eyes — What AI Can See

Perception without action. Read-only access.

| Source | What it contains | Access method | Latency |
|---|---|---|---|
| Supabase / live dashboard | Project index, status, open loops, FastField events | Supabase MCP (Claude Code) or `GET /api/ai/dashboard-summary` (any AI) | Live |
| **Live AI API — dashboard-summary** | Counts + today/tomorrow/at-risk rows from `v_project_card` | `https://interwork-command-center.vercel.app/api/ai/dashboard-summary` — no auth | Live |
| **Live AI API — search** | Project/client/location/PM/scope lookup (max 25 rows) from `v_project_card` | `https://interwork-command-center.vercel.app/api/ai/search?q=<term>` — no auth | Live |
| Dashboard snapshot | Summary counts + today's rows at snapshot time | Raw GitHub URL: `memory/dashboard/CURRENT_DASHBOARD_STATUS.md` | Stale (manual refresh) |
| AI index files | Client roster, project index, open loops summary, dashboard mirror | Raw GitHub URL: `memory/ai_index/` | Stale (refresh on repo push) |
| Client context | Client background, key contacts, rules | Raw GitHub URL: `memory/clients/<slug>/CLIENT_CONTEXT.md` | Stale (refresh on repo push) |
| Project cards | Project scope, schedule, contacts, notes, open loops | Raw GitHub URL: `memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md` | Stale (refresh on repo push) |
| Bootstrap files | Routing map — how to reach the repo, project slugs | Uploaded to Claude Project once | Stable |
| Knowledge packs | Full snapshot at generation time | Uploaded to Claude Project (fallback only) | Very stale |
| Microsoft Teams | Inbound project signals, action items | Graph API read-only (gated) | Requires session setup |
| Read AI notes | Meeting notes, action items | Read AI MCP | Requires session setup |
| Outlook / M365 | Email threads (no direct access) | Requires Alejandro to paste excerpt | Manual |
| FastField forms | Field completion signals | Webhook → Make → Supabase | Live (via Supabase) |
| Screenshots / uploads | Visual confirmation of emails, dashboard, forms | Uploaded by Alejandro | Per-session |

---

### Ears — What AI Receives

Inbound signals that trigger action or capture new facts.

| Source | What it carries | How it arrives |
|---|---|---|
| Teams message snippet | Client/PM update, schedule change, scope clarification | Alejandro pastes into chat |
| Email excerpt | Client confirmation, reschedule, new scope | Alejandro pastes or uploads screenshot |
| FastField submission | Field work completion signal | Webhook → Supabase → Claude Code query |
| Read AI meeting note | Decisions, action items from calls | Read AI MCP fetch |
| Alejandro's verbal update | Confirmed fact, decision, correction | Direct chat input |
| Claude Chat handoff | Structured fact update for Claude Code to execute | Handoff format in Claude Chat output |
| ChatGPT review | Second opinion, plan feedback | `feedback_loop/from_chatgpt.md` |

---

### Hands — What AI Can Act On

Actions that change state. All non-repo writes require Alejandro approval.

| Action | Who can do it | Approval required |
|---|---|---|
| Edit memory files (PROJECT_CARD, OPEN_LOOPS, etc.) | Claude Code | No — repo writes are automatic |
| Commit and push to GitHub | Claude Code | No — except if secret scan flags anything |
| Run PowerShell scripts (read-only) | Claude Code | No |
| Draft client-facing email | Claude Chat or Claude Code | Yes — Alejandro must say "send it" |
| Draft Teams message | Claude Chat or Claude Code | Yes — Alejandro must say "send it" |
| Write to Supabase | Claude Code (MCP) | Yes — always |
| Deploy to Vercel | Claude Code | Yes — always |
| Dispatch FastField form | Claude Code | Yes — always |
| Write to Smartsheet | Claude Code | Yes — always |
| Send emails programmatically | Not available in current setup | N/A |
| Install global tools | Claude Code | Yes — always |

---

## Capability Matrix by AI System

| Capability | Claude Code | Claude Chat | ChatGPT |
|---|---|---|---|
| Read repo files | Yes (direct) | Yes (raw GitHub URL fetch) | Yes (raw GitHub URL fetch) |
| Read Supabase live | Yes (MCP) | Yes (via `/api/ai/dashboard-summary`) | Yes (via `/api/ai/dashboard-summary`) |
| Read dashboard snapshot | Yes | Yes (raw GitHub URL) | Yes (raw GitHub URL) |
| Read AI index files | Yes | Yes (raw GitHub URL) | Yes (raw GitHub URL) |
| Write repo files | Yes | No | No |
| Write to Supabase | Yes (with approval) | No | No |
| Draft emails/messages | Yes | Yes | Yes |
| Send emails/messages | No (not set up) | No | No |
| Execute scripts | Yes | No | No |
| Push to GitHub | Yes | No | No |
| Deploy to Vercel | Yes (with approval) | No | No |

---

## The Three Layers of Current State

```
Layer 1 — Live
  Supabase projects table (Claude Code via MCP)
  Supabase open_loops table (Claude Code via MCP)
  FastField webhook events (Claude Code via MCP)
  GET /api/ai/dashboard-summary (any AI — live Supabase read, no auth required)
  GET /api/ai/search?q=<term> (any AI — live Supabase read, no auth required)
  → Claude Code reads directly via MCP; Claude Chat and ChatGPT read via /api/ai/...

Layer 2 — Near-live (raw GitHub, refreshed by Claude Code on update)
  memory/ai_index/
  memory/dashboard/CURRENT_DASHBOARD_STATUS.md
  memory/clients/<slug>/CLIENT_CONTEXT.md
  memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md
  → Any AI can read via raw GitHub URL

Layer 3 — Snapshot / Uploaded (fallback, stale)
  claude_project_bootstraps/<slug>_bootstrap.md  (stable routing, upload once)
  claude_project_packs/<slug>_knowledge_pack.md  (stale facts, fallback only)
  → Uploaded to Claude Projects manually
```

---

## How a Typical Claude Chat Session Works

```
1. Claude Chat opens → reads bootstrap (uploaded, stable)
2. Bootstrap says: fetch these URLs
3. Claude Chat fetches:
   - memory/ai_index/START_HERE_FOR_AI.md
   - GET /api/ai/dashboard-summary (live operational counts)
4. Alejandro provides project context
5. Claude Chat calls GET /api/ai/search?q=<term> for quick project/client lookup
6. Claude Chat fetches:
   - memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md
   - memory/clients/<slug>/projects/<slug>/OPEN_LOOPS.md
7. Claude Chat answers questions, drafts responses
8. Claude Chat outputs a Claude Code Handoff if facts need to be saved
9. Alejandro takes handoff to Claude Code session
10. Claude Code updates PROJECT_CARD.md, commits, pushes
11. Next Claude Chat session reads updated files
```

---

## Current State — Phase 2 Endpoints 1 and 2 Live (2026-06-30)

```
Layer 1 is now accessible to Claude Chat and ChatGPT via:
  GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary
  GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>
  → live Supabase data, no auth required

Claude Code still owns:
  Writing repo files
  Triggering Supabase writes (with approval)
  Deploying

Remaining Phase 2 endpoints (not yet built):
  /api/ai/project/[client_slug]/[project_slug]
  /api/ai/client/[client_slug]
  /api/ai/open-loops
```

---

## What Is Never Allowed

- Writing secrets, tokens, raw emails, or screenshots to the repo
- Sending client messages without Alejandro saying "send it"
- Writing to Supabase, Smartsheet, or Vercel without approval
- Inventing project numbers, dates, contacts, or statuses
- Scanning unrelated client folders without a cross-client search request
- Trusting old chat memory over the current project card
