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
| Supabase / live dashboard | Project index, status, open loops, FastField events | Supabase MCP (Claude Code) or Vercel API (Phase 2) | Live |
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
| Read Supabase live | Yes (MCP) | No | No |
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
Layer 1 — Live (requires Supabase MCP or Phase 2 Vercel API)
  Supabase projects table
  Supabase open_loops table
  FastField webhook events
  → Claude Code can read directly; Claude Chat cannot (yet)

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
   - memory/dashboard/CURRENT_DASHBOARD_STATUS.md
   - memory/clients/<slug>/CLIENT_CONTEXT.md
4. Alejandro provides project context
5. Claude Chat fetches:
   - memory/clients/<slug>/projects/<slug>/PROJECT_CARD.md
   - memory/clients/<slug>/projects/<slug>/OPEN_LOOPS.md
6. Claude Chat answers questions, drafts responses
7. Claude Chat outputs a Claude Code Handoff if facts need to be saved
8. Alejandro takes handoff to Claude Code session
9. Claude Code updates PROJECT_CARD.md, commits, pushes
10. Next Claude Chat session reads updated files
```

---

## Future State — With Phase 2 Vercel API

```
Layer 1 becomes accessible to Claude Chat:
  Claude Chat fetches /api/ai/dashboard-summary → live Supabase data
  Claude Chat fetches /api/ai/project/<slug>/<slug> → current project card served by API

Claude Code still owns:
  Writing repo files
  Triggering Supabase writes (with approval)
  Deploying
```

---

## What Is Never Allowed

- Writing secrets, tokens, raw emails, or screenshots to the repo
- Sending client messages without Alejandro saying "send it"
- Writing to Supabase, Smartsheet, or Vercel without approval
- Inventing project numbers, dates, contacts, or statuses
- Scanning unrelated client folders without a cross-client search request
- Trusting old chat memory over the current project card
