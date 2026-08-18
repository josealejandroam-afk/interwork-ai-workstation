# Module 4 — AI and Shared Project Knowledge
This is the layer built on top of the systems from Module 3: a shared GitHub repo that acts as durable memory, plus Claude as a research/drafting assistant. Nothing in this module changes what you learned about the business in Modules 1–2 — it's how the AI tools help you do that work faster.

_Sources used: `memory/ai_index/START_HERE_FOR_AI.md`, `memory/company_knowledge/REPO_LOOKUP_RULES.md`, `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md`, `docs/AGENT_PERMISSIONS.md` — verified against current state as of 2026-07-28._

## What this repo is

A GitHub repo (`interwork-ai-workstation`) that holds structured project memory: client context, project cards, open loops, and the company knowledge you read in Modules 1–3. It exists so every AI session — and every person — is working from the same facts.

**It is not the live dashboard.** It's a durable record that supplements Supabase, not a replacement for it. When repo content and Supabase disagree, Supabase (live state) wins — but say so, don't silently pick one.

## Repo navigation — don't scan the whole thing

1. Always start with the company knowledge files (Modules 1–3 pulled from these)
2. Identify the client → open only `memory/clients/<client_slug>/CLIENT_CONTEXT.md`
3. Identify the project → open only that project's folder: `PROJECT_CARD.md`, `OPEN_LOOPS.md`, `NOTES.md`, `DRAFTS.md`
4. If a vendor is named, also check `memory/vendors/VENDOR_INDEX.md`
5. Use `memory/ai_index/CLIENT_ROSTER.md` only when the client isn't obvious

Full detail and worked examples: `memory/company_knowledge/REPO_LOOKUP_RULES.md`.

## Claude Code vs. Claude Chat

- **Claude Code** is the only session with repo write access, script execution, and Supabase write capability. It's the one that commits memory updates.
- **Claude Chat** (and any other AI session) reads the repo for context and drafts, but needs current information handed to it — it can go stale between sessions.
- Either way: **AI drafts freely. AI sends and writes nothing without your explicit approval** — same rule as covers you directly in Module 3, just stated again because it's the one rule that must never get fuzzy.

## What's actually connected right now (verified 2026-07-28)

| System | Status |
|---|---|
| Supabase | Connected, read-only for AI. Writes require explicit approval, field by field. |
| Command Center dashboard | Live, read-only |
| Outlook / Teams (M365) | **Blocked** by company tenant policy — not a simple reconnect, requires IT (Christian) or Gal to approve a sanctioned path. Don't request or follow up. |
| Smartsheet | Not connected as an AI read source; permanently no-write for AI regardless of connection status |
| FastField | No API, ever — mobile form only. The Make.com bridge to Supabase is inactive pending a confirmed test payload. |
| GitHub repo | AI reads/writes today; your own access is staged per `07_ACCESS_CHECKLIST_SCOTT.md` / `_MATT.md` |

If another doc in `docs/` describes a different status, or references `D:\ai-workstation`, that doc is stale — this file and `00_MANAGER_PREP_CHECKLIST.md`'s findings section are current.

## Approval rules for AI-assisted work

From `docs/AGENT_PERMISSIONS.md`, the short version:
- **Automatic, always safe**: reading, searching, summarizing, drafting (email/Teams/reports) — none of this needs sign-off
- **Ask first**: sending anything, deleting records, writing to a live database, changing access controls

From `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md`, the rules that apply to everyone using the AI tools, not just Claude:
- Never put API keys, tokens, `.env` contents, or Supabase credentials into a repo file or a chat
- Never send an email or Teams message through the AI without Alejandro's "send it"
- Never write to Supabase through the AI without "approve" / "apply"
- Never write to Smartsheet through the AI — permanent, no exceptions
- Never invent a project number, contact name, or phone number to fill a gap

## Source-of-truth precedence, when things disagree

1. Live Supabase/dashboard read (current operational state)
2. Repo's dashboard snapshot (`memory/ai_index/DASHBOARD_STATUS.md`) — only if the live read is unavailable
3. The project card — best source for scope, contacts, and history
4. The project's `OPEN_LOOPS.md` — durable history Supabase doesn't carry
5. Client knowledge pack / bootstrap files — routing aids, not fact sources

If live data and the project card conflict, flag it — don't silently trust the newer-looking one.

## Knowledge Check

No formal check for this module either — you'll exercise repo navigation and the approval rules directly in Module 5. Before moving on, be able to explain: if Claude drafts a client email for you, what has to happen before it actually gets sent?
