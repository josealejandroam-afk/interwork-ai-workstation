# Company Claude Handoff Document

**For:** Company Claude account (claude.ai or Claude for Work)  
**Repo:** interwork-ai-workstation (private)  
**Operator:** Alejandro Acosta, Operations Project Manager, InterWork Office  
**Prepared:** 2026-06-29

---

## What This Repo Is

This is the AI operations engine for InterWork Office — a commercial furniture and office services company that runs workstation relocations, decommissions, installations, and assessments across client sites.

Alejandro manages roughly 580 projects in Supabase. This workstation gives Claude persistent memory, custom commands, RAG search over procedures and context, and an approval-gated pipeline for proposing project data changes.

---

## Who Is Alejandro

- **Title:** Operations Project Manager, InterWork Office
- **Work email:** alejandroa@interworkoffice.com (M365 / Outlook / Teams)
- **Personal email:** jose.alejandro.a.m@gmail.com — personal only, no project data
- **Role in this system:** Final approval authority for every write, status change, and outbound message
- **Reports to / escalates to:** Francisco Vinueza (Operations Manager), David Steinbrecher (leadership)
- **Peer:** Hunter Barbieri (Operations PM, scheduling/coordination support)

---

## What Claude Does Here

**Reads:**  
- Supabase projects table (~580 rows) and related tables
- Smartsheet schedule rows (read-only forever)
- M365 / Outlook / Teams / Read AI when connected
- FastField form data when available

**Proposes (never auto-applies):**  
- Project status changes
- Completion signal flags (`fastfield_submitted`, `completion_report_sent`)
- Open loop entries in Supabase
- Draft client/vendor messages for Alejandro to approve and send

**Never does autonomously:**  
- Write to Supabase without explicit "approve" or "apply" from Alejandro
- Send Teams messages or emails without "send it"
- Set `vendor_confirmed`, `client_confirmed`, or `access_confirmed` on any project
- Write to Smartsheet
- Expose or print secret values

---

## What Is in This Repo

| Folder | Purpose |
|--------|---------|
| `commands/` | 17 custom slash commands (see SYSTEM_CAPABILITY_MATRIX.md) |
| `memory/` | Persistent context — procedures, project notes, people, open loops |
| `rag/` | RAG pipeline: BM25 + vector hybrid search over memory files |
| `scripts/` | PowerShell and Python utility scripts |
| `docs/` | Reference docs, runbooks, approval checklists |
| `feedback_loop/` | OpenAI review exchange files |

---

## What Is NOT in This Repo (Must Be Set Locally)

- `.env` files — not committed; secrets live in Windows Registry
- API keys, tokens, service keys, webhook URLs
- `rag/stores/` — RAG vector database (rebuilt locally via `uv run python rag/ingest.py`)
- `.venv/` — Python virtual environment
- `D:\ai-cache\` — HuggingFace model weights

---

## Key Relationships

| System | Role | Write? |
|--------|------|--------|
| Supabase (`interwork-command-center`) | Canonical operational DB | Yes — with Alejandro approval |
| Smartsheet | Schedule source | Never |
| M365 / Outlook / Teams | Signal source (work signals only) | Draft only, send requires approval |
| Read AI | Meeting summaries | Read only |
| FastField | Work completion forms | Read only (no API) |
| Memory / RAG | Procedure and context store | Auto (local `.md` files) |

---

## Current System State (as of 2026-06-29)

- Supabase: **connected, read-only review mode**
- M365 / Teams / Smartsheet: **OAuth re-auth pending**
- RAG index: **healthy — 24+ files indexed**
- Env vars: **set in Windows Registry on desktop machine**
- Make.com FastField webhook: **inactive — awaiting test payload**
- Repo: **pushed to GitHub private — josealejandroam-afk/interwork-ai-workstation**

---

## Documents to Read First

1. `docs/OPERATING_RULES_FOR_COMPANY_CLAUDE.md` — what you can and cannot do
2. `docs/SYSTEM_CAPABILITY_MATRIX.md` — all commands and their status
3. `docs/CURRENT_WORK_QUEUE_FOR_COMPANY_CLAUDE.md` — what needs doing right now
4. `memory/references/interwork_ai_ops_master_context.md` — full architecture and decisions
5. `memory/procedures/interwork_approval_rules.md` — permission model
