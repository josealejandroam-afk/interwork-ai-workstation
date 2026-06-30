---
name: interwork-ai-ops-master-context
description: "Comprehensive reference for the InterWork AI Operations System — vision, architecture, commands, schema, blockers, and production checklist"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-09-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork AI Operations System — Master Context
_Last updated: 2026-06-26 | Maintained by Claude Code_

---

## Review Context Summary

**Roles:** Claude Code = builder/operator. OpenAI/ChatGPT = reviewer/advisor. Alejandro Acosta (Operations Project Manager) = final approval authority. Hunter Barbieri (Operations Project Manager) = peer OPM, scheduling/coordination support. OpenAI only knows what Claude sends — always include this section.

**Architecture:**
- Supabase = canonical write target (projects, open_loops, activity_log, v_project_health)
- Smartsheet = read-only schedule source (never write)
- Memory/RAG = procedures, decisions, historical context (44 chunks indexed)
- Outlook/M365/Teams/Read AI = live signal sources (read-only); Gmail = personal account only, not a work source
- Claude Code = operations engine

**Commands:** /dashboard-status, /project-health, /completion-backlog, /completion-intake, /readai-brief, /meeting-intake, /teams-brief, /rag-status, /rag-search, /ask-openai-review, /feedback-status, /ff-sent

**Applied schema:** open_loops table ✅, v_project_health view ✅, activity_log pre-existing ✅. RLS not applied. Communications schema not applied.

**Blockers:** M365/Teams OAuth incomplete. Read AI not available in Claude Code CLI. FastField has no API (manual/file intake only). Work email is M365 (personal Gmail has no project data). Health alerts noisy until status backfill completes.

**Held for approval:** 6-project batch status→completed (7374, 7499, 7498, 7347, 7472, 7482). 7447 actual_end_at correction. RLS policies. Communications changes. Confirmation boolean updates. Any Smartsheet writes.

**Permission model:**
- Auto-allowed: reads, memory/RAG writes, local scripts, parser work, SQL drafts, status reports
- Requires approval: Supabase writes, status changes, RLS, vendor_confirmed/client_confirmed/access_confirmed, Outlook/Teams sends, Smartsheet writes, production data deletion

**Priority:** Data reliability first → clean backlog → completion signal intake → reduce false alerts → then expand signal automation.

**Key decisions:** 7053 held (punchlist due June 30). 7447 bad actual_end_at awaits fix approval. Use source='manual' in activity_log for Claude writes. Never auto-set vendor_confirmed/client_confirmed/access_confirmed.

---

## 1. System Vision

Build an AI operations engine for InterWork Office that:
- Gives Alejandro a reliable, real-time view of all active projects
- Surfaces completion signals automatically (FastField, WC reports, email, Teams)
- Flags genuine risks (overdue in_progress, missing PM, unconfirmed near-term jobs)
- Eliminates false alerts caused by stale "scheduled" status on completed work
- Acts as a proposal engine — never auto-updates data, always surfaces for approval

**Core principle (ChatGPT-confirmed):** Claude executes, ChatGPT reviews, Alejandro approves.

**Build sequence (ChatGPT-confirmed):**
1. Clean the old noise (backlog triage + status cleanup)
2. Fix why the noise happened (completion signal pipeline)
3. Then add more signal sources (Teams, Read AI, Outlook/M365)

---

## 2. Architecture

```
[Smartsheet]  ──read-only──►  [Claude Code]
[Outlook/M365]──read-only──►  [Claude Code]  ──write-proposed──►  [Supabase DB]
[Read AI]     ──read-only──►  [Claude Code]                             │
[Teams]       ──read-only──►  [Claude Code]         ▼              [activity_log]
[FastField]   ──manual/file►  [Claude Code]   [Memory / RAG]
                                                    │
                                              [MEMORY.md index]
```

**Data flow:**
- Smartsheet → schedule source (row_id in projects.smartsheet_row_id)
- Outlook/M365 → completion signals, open loop detection (work email only; Gmail = personal)
- Read AI → meeting summaries, action items
- Teams → unread messages, project mentions, pending replies
- FastField → work completion confirmation (boolean `fastfield_submitted`)
- WC Reports → completion confirmation (boolean `completion_report_sent`)
- Supabase → canonical write target; source of truth for project state
- Memory/RAG → historical context, decisions, procedures (35 chunks indexed)

---

## 3. Data Authority Rules

| Source | Authority | Write? |
|--------|-----------|--------|
| Supabase | Canonical operational DB | Yes — with approval |
| Smartsheet | Schedule/planning source | No — read-only |
| Outlook / M365 | Signal source (work email: alejandroa@interworkoffice.com) | No — read-only; requires Graph API auth |
| Teams | Signal source | No — read-only (sends require approval) |
| Read AI | Meeting record source | No — read-only |
| FastField | Completion signal source | No API yet; manual/file intake only |
| Memory/RAG | Procedure and context store | Yes — automatic for .md files |

---

## 4. Supabase / Dashboard Role

Supabase is the **write target**. All project state lives here.

Key tables:
- `projects` — 140 rows confirmed (Content-Range verified 2026-06-29; prior ~580 estimate was incorrect, likely confused with Smartsheet row count)
- `open_loops` — action item queue (applied 2026-06-26)
- `activity_log` — write audit trail (4 rows; was pre-existing)
- `fastfield_forms` — mostly empty; completion signals not flowing yet
- `communications` — 0 rows; email/Teams not synced
- `v_project_health` — view applied 2026-06-26; red/yellow/green + 0-100 score

**Known data quality issues:**
- 61 past-dated active projects (status=scheduled but work is done)
- 11 have `fastfield_submitted=true` → 6 clean ones proposed for status=completed
- `completion_report_sent`: 0% populated
- `v_project_health` false alert rate high until status backfill done
- `communications` table empty — no email/Teams data synced

---

## 5. FastField Workflow — Sent vs. Submitted (Critical Distinction)

**FF Sent to PM** and **FF Submitted by PM** are two separate events with different sources, meanings, and Supabase effects.

| Event | Source | Meaning | Supabase effect |
|-------|--------|---------|-----------------|
| FF Sent to PM | Outlook sent email / Teams message / `/ff-sent` manual command | Alejandro dispatched the FastField to the field PM | Create open loop: "waiting for PM to submit FF" — do NOT set `fastfield_submitted = true` |
| FF Submitted by PM | FastField HTTP webhook → `fastfield_webhook_events` table | PM completed and submitted the FF form in the field | Propose `fastfield_submitted = true` + capture timestamp + resolve open loop — requires Alejandro approval |

**`fastfield_submitted = true` means the PM submitted the form. It never means FF was sent.**

### FastField Assignment Detection — Priority Order
1. **Outlook/M365 Graph API** — read Alejandro's sent email for FF instructions to PM; extract: project number, PM name, date, scope
2. **Teams** — if FF instructions were sent via Teams message
3. **Outlook Web via Playwright** — only if Graph API unavailable AND Alejandro explicitly approves browser-based reading
4. **Manual: `/ff-sent <project_number> <pm_name> <date>`** — always available as fallback

### FastField Submission Detection
- Source: `fastfield_webhook_events` table (Make.com scenario receives webhook, stores raw payload)
- Scenario ID: 5506328 | Hook ID: 2508004 | Status: inactive until one controlled test completes
- Config: `D:\ai-workstation\scripts\fastfield_webhook_config.txt` (token not in memory/RAG)

---

## 5a. Smartsheet Read-Only Rule

Smartsheet is a **read-only schedule source**. Never write to Smartsheet.
Projects link to Smartsheet via `projects.smartsheet_row_id`.
Smartsheet completion signals (% complete, "Done" status) are treated as
**low/medium confidence** — never sufficient alone to set `fastfield_submitted`
or `completion_report_sent`.

---

## 6. Memory / RAG Role

- `D:\ai-workstation\memory\` — file-based memory store
- `MEMORY.md` — master index (loaded every conversation)
- Subfolders: profile/, projects/, procedures/, open_loops/, references/, feedback/
- RAG: BM25 + vector hybrid, `uv run python D:\ai-workstation\rag\ingest.py`
- 35 chunks indexed as of last run
- Re-index after any new memory files are created

Memory writes (`.md` files) are **automatic** — no approval needed.
Supabase writes always require approval.

---

## 7. Signal Sources — Role and Status

| Source | Role | Status |
|--------|------|--------|
| Gmail MCP | Personal account (jose.alejandro.a.m@gmail.com) — no project emails | Connected but wrong inbox; do not use for work signals |
| Outlook / M365 | Work email (alejandroa@interworkoffice.com) — WC reports, FF notifications, vendor/client comms | Integration gap: Graph API OAuth not complete |
| Teams | Project mentions, unread messages, pending replies | OAuth pending |
| Read AI | Meeting summaries, action items | Connected in Claude app; not in Claude Code CLI |
| FastField | Work completion forms | No API; manual/file only |
| Smartsheet | Schedule, project rows | Connected (read-only) |

**Key finding:** Work email is Outlook/M365 (`alejandroa@interworkoffice.com`). Gmail MCP (personal account: `jose.alejandro.a.m@gmail.com`) has no project-related emails and must never be used as a work signal source. Outlook/M365 Graph API OAuth is the unlock for email-based completion evidence and FastField assignment detection.

---

## 8. Permission Model

| Action | Level | Requirement |
|--------|-------|-------------|
| Read from any source | 1 — Auto | None |
| Write to memory (`.md` files) | 1 — Auto | None |
| Supabase DDL (schema changes) | 3 — Explicit | Alejandro: "apply migration" |
| Supabase DML (INSERT/UPDATE) | 3 — Explicit | Alejandro: "apply" / "approve" |
| Send Teams message | 3 — Explicit | Alejandro: "send it" |
| Send email | 3 — Explicit | Alejandro explicit approval |
| Supabase inserts for open_loops | 3 — Explicit | Alejandro approval |

**Fields that are NEVER auto-set (ever):**
- `vendor_confirmed`
- `client_confirmed`
- `access_confirmed`

**Fields that require per-project approval:**
- `status` changes
- `fastfield_submitted`
- `completion_report_sent`
- `actual_end_at`

Every approved Supabase write must log to `activity_log`:
```sql
INSERT INTO public.activity_log (project_id, actor, action, detail, source, before_state, after_state)
VALUES (..., 'alejandro', 'status_update', '...', 'manual', '{}', '{}');
```
(Use `source='manual'` for Claude-initiated writes until enum is extended.)

---

## 9. Commands Created

| Command | File | Type | Description |
|---------|------|------|-------------|
| `/dashboard-status` | commands/dashboard-status.md | Read-only | Project counts, attention items |
| `/project-health` | commands/project-health.md | Read-only | Deep scoring via v_project_health |
| `/completion-backlog` | commands/completion-backlog.md | Read-only | Triage of past-dated projects |
| `/completion-intake` | commands/completion-intake.md | Write-proposed | Accepts FastField/WC/email → proposes updates |
| `/readai-brief` | commands/readai-brief.md | Read-only | Read AI meeting brief (dual-mode) |
| `/meeting-intake` | commands/meeting-intake.md | Write-proposed | Deep meeting intake, saves to memory |
| `/teams-brief` | commands/teams-brief.md | Read-only | Teams unread/mentions (Graph → Playwright → PS1) |
| `/rag-status` | commands/rag-status.md | Read-only | RAG index health and staleness |
| `/ask-openai-review` | commands/ask-openai-review.md | External | Sends review packet to OpenAI, saves action plan |
| `/feedback-status` | commands/feedback-status.md | Read-only | Feedback loop file state and freshness |
| `/ff-sent` | commands/ff-sent.md | Write-proposed | Manual fallback: records FF dispatched to PM; creates open loop; never sets fastfield_submitted |

**Supporting scripts:**
- `D:\ai-workstation\scripts\ask_openai_review.py` — OpenAI Responses API bridge
- `D:\ai-workstation\scripts\parse_completion_email.py` — email completion signal parser
- `D:\ai-workstation\scripts\send_to_chatgpt.py` — Playwright ChatGPT bridge

---

## 10. Supabase Objects Created

| Object | Type | Migration Name | Applied |
|--------|------|----------------|---------|
| `open_loops` | Table | `create_open_loops_table` | 2026-06-26 |
| `v_project_health` | View | `create_v_project_health_view` | 2026-06-26 |

**`v_project_health` calibration note:**
- Proximity checks trigger on negative `days_until` (past-dated projects)
- Fix pending: use `GREATEST(scheduled_date, COALESCE(scheduled_end_date, scheduled_date))` as reference
- 5 genuine reds: in_progress + overdue (7060 MMC Dallas is the most critical)

**`activity_log` schema (pre-existing):**
```
id, project_id, actor, action, detail, source (enum), before_state (jsonb), after_state (jsonb), occurred_at
```
Use `source='manual'` for Claude-initiated writes (no 'ai' enum value yet).

---

## 11. Current Blockers

| Blocker | Impact | Resolution |
|---------|--------|------------|
| M365 / Teams OAuth not complete | No Teams or Outlook access | Run `/mcp` → "claude.ai Microsoft 365" |
| Read AI MCP needs CLI auth | `/readai-brief` Mode A not working | OAuth via `/mcp` or API key header |
| FastField no API | Completion signals manual only | Build export/email intake (in progress) |
| Gmail MCP = personal account | No work email evidence — wrong inbox | M365 Graph API OAuth is the fix; do not build Gmail workflows |
| v_project_health date calibration | Proximity false alerts | SQL fix pending (not yet drafted) |

---

## 12. Current Priorities (ChatGPT-confirmed, 2026-06-26)

1. **Approve 6-project batch status update** — awaiting Alejandro "approve batch complete 6"
   Projects: 7374, 7499, 7498, 7347, 7472, 7482 → status = completed
2. **Fix 7447 bad actual_end_at** — draft at `scripts/sql/draft_fix_7447_actual_end.sql`; awaiting approval
3. **Hold 7053** — scheduled end 2026-06-30, final punchlist still due; revisit July 1
4. **M365 OAuth** — unlocks Teams + Outlook; highest-value integration after data cleanup
5. **Build completion-intake email parsers** — WC report email parser ✅ built; M365 connection needed to run live
6. **v_project_health date calibration** — fix proximity trigger for past-dated projects
7. **30 stalled projects review** — Gmail MCP (personal) has no evidence; needs Outlook/M365 Graph API or manual review

---

## 13. Things That Require Alejandro Approval

**Pending (not yet applied):**
- Batch status update: 7374, 7499, 7498, 7347, 7472, 7482 → `status = 'completed'`
  Say: "approve batch complete 6"
- 7447 `actual_end_at` correction: NULL out the invalid April 15 value
  Say: "apply 7447 fix"
- Any future `status` changes on any project
- Any `open_loops` INSERT to Supabase
- Any `activity_log` INSERT (included with each write proposal)
- Any email or Teams message sends
- Schema changes (DDL migrations)
- `v_project_health` date calibration fix (when drafted)

**Never without explicit approval:**
- `vendor_confirmed`, `client_confirmed`, `access_confirmed` — any project
- Any Smartsheet write
- Any RLS change (enabling RLS will block all access until policies are added)

---

## 14. Production-Readiness Checklist

### Must-have before daily trust
- [ ] Status backfill complete (61 past-dated → accurate status)
- [ ] `actual_end_at` corrections applied (7447 fix approved)
- [ ] `v_project_health` date calibration fix applied
- [ ] `activity_log` entry on every Supabase write
- [ ] All write commands clearly declare `write-proposed` in output
- [ ] `/completion-backlog` and `/completion-intake` tested with real data

### Should-have for full signal coverage
- [ ] M365 / Teams OAuth connected
- [ ] Read AI MCP authenticated in Claude Code CLI
- [ ] `completion_report_sent` populated (WC report email intake running)
- [ ] `fastfield_submitted` auto-populated (FastField email/export intake)
- [ ] `communications` table receiving email/Teams sync

### Nice-to-have
- [ ] RLS policies designed and reviewed (do NOT enable without policies)
- [ ] `fastfield_forms` table receiving actual form data
- [ ] Smartsheet bidirectional sync (status updates flowing back)
- [ ] `v_project_health` score calibrated post-backfill (target: <5 false reds)
- [ ] `/rag-status` showing >100 chunks with recent project files indexed

---

## 15. Key Decisions (from ChatGPT and Claude sessions)

- **2026-06-26:** Do not add more intake features before completion data is reliable.
  Sequence: clean backlog → completion pipeline → add signal sources.
- **2026-06-26:** FastField parser priority: WC report email → email text → pasted notes → folder → CSV
- **2026-06-26:** Smartsheet signals = low/medium confidence; never sets `fastfield_submitted` or `completion_report_sent`
- **2026-06-26:** 7053 Strategic Education DC — hold until June 30 (final punchlist in scope)
- **2026-06-26:** 7364 and 7447 — exclude from batch; suspicious actual_end_at values
- **2026-06-26:** Use `source='manual'` in activity_log for Claude-initiated writes (no 'ai' enum yet)
