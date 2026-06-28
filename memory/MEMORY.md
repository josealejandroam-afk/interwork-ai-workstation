# Memory Index

## User
- [User Profile](profile/user_profile.md) — Alejandro's role, work style, projects, and preferences

## Reference
- [AI Ops Master Context](references/interwork_ai_ops_master_context.md) — ⭐ PRIMARY REFERENCE: vision, architecture, all commands, schema, blockers, priorities, approval queue, production checklist
- [InterWork Command Center](references/interwork-command-center.md) — Architecture, design principles, system roles, permission policy, success definition
- [Supabase Schema](references/interwork_command_center_schema.md) — Full table/column/enum reference for hskgrxhdtgowagkfkjsw ⚠️ RLS disabled on all tables
- [People Map](references/interwork_people_map.md) — Core team (Alejandro OPM, Hunter OPM), field PMs, client/vendor contacts; lookup before drafting confirmations
- [Project Types](references/interwork_project_types.md) — 8 project types: Decom, Move, Install, Delivery, Walkthrough, Punchlist, Storage, Internal Relocation — required info, risks, completion signals per type
- [FastField Make Integration](references/fastfield_make_integration.md) — Make.com scenario IDs, webhook config, Supabase table proposal, payload mapping, phase plan

## Project
- [Workstation Setup](project_workstation_setup.md) — AI coding/automation workstation setup progress and remaining tasks

## Feedback
- [ChatGPT Message Method](feedback_chatgpt_message_method.md) — save message to temp file before sending; never inline long strings
- [ChatGPT App vs Browser](feedback_chatgpt_app_vs_browser.md) — Alejandro uses ChatGPT desktop app; Playwright cannot reach it; must open conversation in Chrome first
- [Token Handling](feedback_token_handling.md) — never print TOKEN_SECRET or full webhook URLs in terminal, chat, diffs, memory, or RAG; write to config silently; show REDACTED in all output

## Projects
- [Project 7492](projects/project-7492.md) — MMC, John Smith (Teams), status: active, open loop teams-20260701-001
- [Project template](projects/_template.md) — standard format for new project memory files

## Clients
- [Client template](clients/_template.md) — standard format for client profiles (contacts, locations, billing, PO, lessons learned)

## Vendors
- [Sunset](vendors/sunset.md) — vendor stub; awaiting knowledge dump
- [Just4Wheels](vendors/just4wheels.md) — vendor stub; awaiting knowledge dump
- [Vendor template](vendors/_template.md) — standard format for vendor profiles (contacts, capabilities, rates, reliability, use cases)

## Operating Knowledge
- [Project Lifecycle](procedures/interwork_project_lifecycle.md) — 14-stage lifecycle (Request → Quote → Smartsheet → Supabase → Plan → Vendor → Client → FF → Teams PM → Execution → Verify → WC → Closeout → Closed) with approval gates per stage
- [Approval Rules](procedures/interwork_approval_rules.md) — what Claude can do automatically vs. what requires Alejandro approval; quick reference card
- [Communication Rules](procedures/interwork_communication_rules.md) — tone, message templates (client / vendor / field PM), what to include/exclude, what requires approval before sending

## Procedures
- [FF Sent](../../../.claude/commands/ff-sent.md) — `/ff-sent <project_number> <pm_name> <date>` manual fallback: records FF dispatched to PM; creates open loop; does NOT set fastfield_submitted
- [FastField Assignment Watch](../../../.claude/commands/fastfield-assignment-watch.md) — `/fastfield-assignment-watch` detects if FF was sent via Outlook/Teams/memory; falls back to `/ff-sent`; never sets fastfield_submitted
- [FastField Intake](../../../.claude/commands/fastfield-intake.md) — `/fastfield-intake` reads raw events from fastfield_webhook_events, proposes project matches and fastfield_submitted updates; never auto-applies
- [Teams Brief](../../../.claude/commands/teams-brief.md) — `/teams-brief` reads Teams via Graph → Playwright → PS1; never sends without explicit approval
- [RAG Status](../../../.claude/commands/rag-status.md) — `/rag-status` checks index health, coverage, and staleness
- [Dashboard Status](../../../.claude/commands/dashboard-status.md) — `/dashboard-status` lightweight read-only Supabase query: counts, active projects, attention items
- [Project Health](../../../.claude/commands/project-health.md) — `/project-health` deep scoring via v_project_health view + Claude judgment; proposes but never auto-applies confirmation updates
- [Completion Backlog](../../../.claude/commands/completion-backlog.md) — `/completion-backlog` read-only triage of past-dated active projects grouped by evidence level
- [Read AI Brief](../../../.claude/commands/readai-brief.md) — `/readai-brief` pulls last 10 meetings via Read AI, matches to projects, surfaces action items needing attention
- [Meeting Intake](../../../.claude/commands/meeting-intake.md) — `/meeting-intake <ULID>` deep intake for one meeting: saves note to memory, proposes open loops, re-indexes RAG
- [Completion Intake](../../../.claude/commands/completion-intake.md) — `/completion-intake` accepts FastField exports, WC reports, email, pasted notes → proposes Supabase updates, never auto-applies
- [Ask OpenAI Review](../../../.claude/commands/ask-openai-review.md) — `/ask-openai-review` sends feedback_loop/to_chatgpt.md to OpenAI Responses API → saves response + action plan; never auto-executes
- [Feedback Status](../../../.claude/commands/feedback-status.md) — `/feedback-status` read-only check of feedback loop file state, freshness, and pending action items

## Applied Schema (2026-06-26)
- `open_loops` table — migration `create_open_loops_table` applied via Supabase MCP
- `v_project_health` view — migration `create_v_project_health_view` applied via Supabase MCP
- Draft SQL files remain at `C:\Users\1\scripts\sql\` for reference

## Decisions
- **2026-06-26 ChatGPT:** Sequence = (1) clean backlog → (2) build completion-intake pipeline → (3) add more signal sources (Teams/Read AI/Outlook/M365). Do not add intake features before completion data is reliable. Gmail = personal account, never a work signal source.

## Open Loops
- [Open Loops Queue](open_loops/) — unified queue: one file per item, frontmatter fields: source / project / person / status / created / updated
- [Loop Template](open_loops/_template.md) — standard format for all sources (teams, outlook, smartsheet, fastfield, browser, manual)
- [Backfill Review 2026-06-26](open_loops/backfill_review_2026-06-26.md) — 47 flagged projects grouped: Group A (fastfield done, likely complete), B (walkthroughs), C (no signals), D (missing PM), E (genuine reds)

---
**Memory structure follows ChatGPT recommendations (2026-06-25):**
Each memory file uses frontmatter: `type`, `status`, `confidence`, `source`, `review_after`
Subfolders: profile/ projects/ clients/ vendors/ contacts/ procedures/ decisions/ preferences/ open_loops/ mistakes/ tool_notes/ references/
