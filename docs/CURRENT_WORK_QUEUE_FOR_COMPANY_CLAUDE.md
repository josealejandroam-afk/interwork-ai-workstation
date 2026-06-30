# Current Work Queue for Company Claude

**As of:** 2026-06-29  
**Operator:** Alejandro Acosta  
**Status:** Post-migration, Supabase read-only active, M365 OAuth pending

Actions requiring approval are clearly marked. Do not apply held items without Alejandro's explicit "approve" or "apply" instruction.

---

## HELD — Awaiting Alejandro Approval

These are ready to execute. Do not apply without Alejandro reviewing and confirming.

| # | Item | What's needed | Details |
|---|------|--------------|---------|
| 1 | Batch status update: 7374, 7499, 7498, 7347, 7472, 7482 → `status = 'completed'` | Say: "approve batch complete 6" | Proposed 2026-06-26; 6 projects with `fastfield_submitted = true`, no red flags. Draft SQL: `scripts/sql/draft_batch_complete_fastfield.sql` |
| 2 | Project 7447 — fix invalid `actual_end_at` (April 15 before June 16 start) | Say: "apply 7447 fix" | Bad date caused health score issues. Fix: NULL out the field. Draft: `scripts/sql/draft_fix_7447_actual_end.sql` |
| 3 | Project 7053 — review for completion | Review after 2026-06-30 | Final punchlist was due June 30. Hold until Juan Martinez (field PM) confirms work done. |
| 4 | Send confirmation to Frank Barrett (project 7060) | Say: "send it" after reviewing draft | Draft in `docs/PROJECT_STATUS_CONFIRMATION_DRAFTS.md` |
| 5 | Send confirmation to Pedro Martinez (project 7348) | Say: "send it" after reviewing draft | Same file |

---

## READY NOW — No Secrets, No MCP Required

These can be run in any Claude session as long as the repo is open.

| # | Action | How |
|---|--------|-----|
| 1 | Check open loops | `/find-open-loops` |
| 2 | Search memory and procedures | `/rag-search "topic"` |
| 3 | Morning brief from memory | `/brief-me` |
| 4 | Review feedback loop status | `/feedback-status` |
| 5 | RAG index health | `/rag-status` |

---

## READY — Supabase Connected

These require `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` env vars (already set on desktop).

| # | Action | How |
|---|--------|-----|
| 1 | Project count and health overview | `/dashboard-status` |
| 2 | Full health scoring by project | `/project-health` |
| 3 | Triage past-dated projects | `/completion-backlog` |
| 4 | Record FastField dispatched to PM | `/ff-sent <project_number> <pm_name> <date>` |
| 5 | Process completion evidence | `/completion-intake` |

---

## BLOCKED — Waiting on M365 / Teams OAuth

These cannot run until Alejandro re-authenticates M365 in the Claude Code MCP panel.

| # | Action | Blocker |
|---|--------|---------|
| 1 | Read Teams messages | Teams OAuth (alejandroa@interworkoffice.com) |
| 2 | Read Outlook/work email | Same — Outlook/M365 Graph API |
| 3 | WC report email parser live run | Same |
| 4 | FastField assignment detection via email | Same |
| 5 | `/teams-brief` | Teams OAuth |
| 6 | `/readai-brief` Mode A | Read AI MCP CLI auth |

**Workaround:** Paste content manually and use `/meeting-intake --paste` or `/brief-me`.

---

## BLOCKED — Waiting on Test Payload Confirmation

Do not activate until tested.

| # | Action | Blocker |
|---|--------|---------|
| 1 | Activate Make.com FastField scenario 5506328 | Test submission must land in `fastfield_webhook_events` table first |
| 2 | Set `fastfield_submitted = true` via webhook | FastField/Make confirmed working + Alejandro approval per project |

---

## PRODUCTION-READINESS GAPS

Must-have before fully trusting dashboard data:

- [ ] Status backfill: 61 past-dated projects with wrong status (6-project batch is step 1)
- [ ] `actual_end_at` fix on 7447
- [ ] `v_project_health` proximity calibration (SQL fix not yet drafted)
- [ ] `activity_log` entry verified on every Supabase write going forward
- [ ] M365 OAuth connected

Should-have for full signal coverage:

- [ ] `completion_report_sent` populated (WC report parser running live)
- [ ] `fastfield_submitted` auto-populated (FastField webhook active)
- [ ] `communications` table receiving email/Teams data
- [ ] Smartsheet MCP re-authorized

---

## DO NOT TOUCH — Permanently Blocked

| Item | Reason |
|------|--------|
| Write to Smartsheet | Permanently read-only — no exceptions |
| Auto-send any email or Teams message | Requires "send it" from Alejandro |
| Set `vendor_confirmed`, `client_confirmed`, `access_confirmed` | Never auto-set |
| Delete C: archive (`C:\Users\Owner\.claude`) | Keep until fully operational on D: |
| Enable RLS on Supabase | Not until policies are written and reviewed |

---

## Open Loops in Memory

Key unresolved items tracked in `memory/open_loops/`:

- `teams_2026-07-01_001.md` — Teams loop from July 1 (check file for details)
- `backfill_review_2026-06-26.md` — Status backfill open items from June 26

Run `/find-open-loops` to surface all open loop files with current status.
