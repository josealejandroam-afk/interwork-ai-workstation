# InterWork Command Center — Review Packet
_Session: 2026-06-26 (evening)_

## Context
InterWork Office is a commercial office relocation and furniture company.
Alejandro Acosta (Operations Project Manager) manages field operations.
Claude Code is the AI operations engine. Hunter Barbieri is a peer OPM.
Work email: alejandroa@interworkoffice.com (Outlook/M365).
Personal Gmail: personal only — no project data there.

---

## What was built and applied this session

### 1. FastField HTTP webhook intake pipeline (Make.com + Supabase)
- Created Make.com scenario 5506328 "FastField Submission Intake"
- Created webhook 2508004 with token-based auth (query string `?token=...`)
- Applied `fastfield_webhook_events` table to Supabase — raw intake buffer, nullable project_id
- Scenario flow: webhook → token filter → HTTP POST to Supabase
- Status: **INACTIVE pending one controlled test submission**
- Restrictions in place: scenario does NOT update project records, fastfield_submitted, status, or any confirmation boolean

### 2. Operating Knowledge Layer (memory files)
Created structured memory files:
- `interwork_people_map.md` — core team, field PMs, client/vendor contacts, lookup rules
- `interwork_project_lifecycle.md` — 14-stage lifecycle with approval gates
- `interwork_communication_rules.md` — tone, templates, what requires approval before sending
- `interwork_approval_rules.md` — auto-allowed vs requires-Alejandro permission model
- `interwork_project_types.md` — 8 project types with required info, completion signals, risks

### 3. Vendor/Client/Project templates
- `clients/_template.md`, `vendors/_template.md`, `projects/_template.md`
- Vendor stubs: Sunset, Just4Wheels (awaiting knowledge dump)

### 4. Gmail → Outlook/M365 correction (full sweep)
Critical correction: Alejandro uses Outlook/M365 for work, not Gmail. Gmail is personal.
Updated ~13 files (commands + memory) to replace Gmail with Outlook as work signal source.
- All architecture diagrams now show Outlook/M365 as work email
- Gmail explicitly labeled "personal account only — do not use for work signals" everywhere
- Teams remains a live signal source

### 5. FastField Sent vs Submitted semantic fix
Introduced clear distinction:
- **FF Sent** = Alejandro dispatched FastField to PM (source: Outlook/Teams/manual)
  → creates open loop "waiting for PM to submit"
  → does NOT set `fastfield_submitted = true`
- **FF Submitted** = PM completed and submitted the form (source: FastField webhook)
  → proposes `fastfield_submitted = true` via `/completion-intake`
  → resolves the open loop

### 6. New commands
- `/ff-sent <project_number> <pm_name> <date>` — manual fallback when M365 is unavailable; records FF dispatched, creates open loop
- `/fastfield-assignment-watch` — detects if FF was sent via Outlook/Teams/memory/manual; priority chain: M365 Graph → Teams → Playwright (requires approval) → memory → `/ff-sent`

### 7. Batch status update — APPLIED
6 projects updated: status scheduled → completed (all had fastfield_submitted=true, past-dated 37–49 days)
- 7347 MMA Colleague Relocation McLean VA ✅
- 7374 Ingersoll Rand Internal Move Buffalo NY ✅
- 7472 MMA Walkthrough Addison TX + Colleague Relocation Dallas TX ✅
- 7482 Amtrust Furniture Delivery & Installation Jersey City NJ ✅
- 7498 MMC Furniture from 1166 Hoboken NJ ✅
- 7499 MMC Hoboken to Huddle Room King of Prussia PA ✅
Activity log entries written for all 6 with source='manual', actor='alejandro'.

### 8. RAG
73 chunks indexed. BM25+vector hybrid. Verified search finds: FF sent vs submitted distinction, Outlook work email, fastfield assignment detection priority chain.

---

## Current state

### Applied to Supabase
- `open_loops` table ✅
- `v_project_health` view ✅
- `fastfield_webhook_events` table ✅
- 6-project batch: status=completed ✅
- activity_log: 4 baseline + 6 new entries

### Still held for approval
- 7447: `actual_end_at` correction (date is April 15, before scheduled start June 16 — data error; fix drafted at `C:\Users\1\scripts\sql\draft_fix_7447_actual_end.sql`)
- RLS policies
- Communications table schema changes
- vendor_confirmed / client_confirmed / access_confirmed — never auto-set
- Any Smartsheet writes

### Integration gaps (not authorized yet)
- M365/Teams OAuth — needed for Outlook email reading and Teams message scanning
- Read AI MCP — visible in Claude app, not available in Claude Code CLI
- FastField webhook — needs one controlled test submission to map payload fields
- Make.com scenario 5506328 stays inactive until payload structure confirmed

### Remaining backlog
- 7053: hold — punchlist in scope through June 30
- ~41 remaining past-dated active projects — most have no completion signals; need Outlook/manual review once M365 connects
- completion_report_sent: 0% populated across all projects

---

## Permission model (unchanged)
- Auto-allowed: reads, memory/RAG writes, local scripts, SQL drafts
- Requires approval: all Supabase writes, status changes, sends, confirmation booleans
- Gmail: personal account — never a work signal source

---

## Questions for this review

1. **FastField webhook intake design**: We built a raw intake buffer (`fastfield_webhook_events`) that stores the payload without touching project records. The next step after a test submission is to build a matching/review layer: detect project number from payload, propose `fastfield_submitted = true` for matched projects, route unmatched ones for manual review. Is this the right architecture, or should we consider a different approach?

2. **7447 data error**: `actual_end_at` = April 15 before `scheduled_date` = June 16. Proposed fix: NULL the bad `actual_end_at` and leave the rest for manual update. Is this the right call, or is there a risk in nulling it (e.g., does it affect any downstream rollups)?

3. **Stalled projects (no signal, no Outlook yet)**: ~41 past-dated projects have no fastfield/WC/actual_end_at signal. Without M365 access, the only remaining option is manual review or Playwright-based Outlook scrape (which requires Alejandro approval each time). Should we: (a) build a batch manual review workflow where Alejandro pastes email threads, (b) prioritize getting M365 OAuth done first, or (c) treat them as provisional completions after N days with no counter-evidence?

4. **Build sequence**: Current sequence is (1) clean backlog → (2) completion signal intake → (3) signal source expansion (M365/Teams/Read AI). Given the FastField webhook is now set up and waiting for a test, and the backlog is partly cleaned, is the next highest-leverage move to (a) complete the backlog cleanup, (b) do the M365 OAuth, or (c) test the FastField webhook?

5. **activity_log `source` enum**: Current values: outlook/teams/manual/smartsheet/fastfield/phone_log. Claude-initiated writes use 'manual'. Should we propose adding 'ai' as an enum value to distinguish Claude-initiated actions from truly manual ones by Alejandro, or does 'manual' remain the right label?
