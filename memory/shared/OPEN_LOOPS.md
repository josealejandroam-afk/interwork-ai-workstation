# Open Loops
_Unresolved items requiring action. Update status as items close._
_Last updated: 2026-06-29_

---

## URGENT — Due Today / Tomorrow

| # | Loop | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1 | **7510 Pear SF — Frank Barrett must confirm crew and building access** | Frank Barrett / Alejandro | OPEN — UPDATED | Location confirmed: 600 Townsend SF. Client (Mel Apostol) confirmed Jul 1 + 8 AM start in email. Jill Buchman is account mgr. COI sent. Quote under review. Remaining gap: crew not named, building access not confirmed. |
| 2 | **7189 MMC Bermuda Hoboken — Jairo Escalante confirmation + MMC access** | Hunter Barbieri / Alejandro | OPEN | Jul 1 job, no client/access confirmation. Draft Teams msg ready. |

---

## HELD — Awaiting Alejandro Approval

| # | Loop | Trigger Phrase | Notes |
|---|------|---------------|-------|
| 3 | Batch status → completed: 7374, 7499, 7498, 7347, 7472, 7482 | "approve batch complete 6" | 6 projects with fastfield_submitted=true; SQL drafted at scripts/sql/draft_batch_complete_fastfield.sql |
| 4 | Project 7447 — null out invalid actual_end_at | "apply 7447 fix" | April 15 date is before June 16 start; SQL drafted at scripts/sql/draft_fix_7447_actual_end.sql |
| 5 | Send confirmation to Frank Barrett (project 7060 MMC Dallas) | "send it" after reviewing draft | Draft in docs/PROJECT_STATUS_CONFIRMATION_DRAFTS.md |
| 6 | Send confirmation to Pedro Martinez (project 7348 Amtrust Cleveland) | "send it" after reviewing draft | Same file |

---

## BLOCKED — Waiting on Integration Auth

| # | Loop | Blocker | Impact | Next Step |
|---|------|---------|--------|-----------|
| 7 | Outlook/M365 access (alejandroa@interworkoffice.com) | VMX/IT admin approval needed — Outlook add-in store is wrong path | No work email, no WC report parser, no FF assignment detection | Send draft to Christian (VMX/IT) — `docs/drafts/m365_access_request.md` |
| 8 | Teams read access | Same approval as Outlook — Claude M365 connector or Graph MCP | No Teams message reading | Same as #7 |
| 9 | FastField direct HTTP/HTTPS webhook | Make.com scenario 5506328 inactive — needs test payload first | fastfield_submitted not auto-populating | Send one test form submission, confirm lands in fastfield_webhook_events, then activate |
| 10 | Smartsheet read re-auth | MCP re-auth pending | Schedule rows not readable | Re-auth in Claude Code MCP panel |
| 11 | Read AI access in Claude Code CLI | MCP CLI auth incomplete | /readai-brief Mode A broken | OAuth via /mcp or API key header |

---

## PROJECT-LEVEL GAPS — Known, Awaiting Resolution

| # | Project | Gap | Risk |
|---|---------|-----|------|
| 12 | 7579 JPMC Miami / Vecos SMART Lockers | Pending scheduling -- no date, no technician, no building access. Vecos said "sometime next week." Memory card created 2026-06-30. NOT IN SUPABASE. | MEDIUM -- no date yet |
| 13 | 7304 Montebello West Berlin NJ (Jul 2) | No PM assigned, vendor required but not set | HIGH — 3 days out |
| 14 | 7494 MMA Furniture Move SD to Walnut Creek (Jul 6) | No PM assigned, vendor required | HIGH — 7 days out |
| 15 | 7546 MMA Conference Room Dallas (Jul 9) | No PM assigned, vendor required | MEDIUM — 10 days out |
| 16 | 7060 MMC Dallas in_progress since Apr 3 | client_confirmed=false, fastfield_submitted=false | HIGH — 3 months overdue |
| 17 | 7448 — check 7435 MMA Colleague Relocation | in_progress since Apr 23, fastfield_submitted=true but status stuck | MEDIUM — likely done |
| 18 | 48 past-dated projects with status=scheduled | Status backfill needed | MEDIUM — creates noise in health view |

---

## INFRASTRUCTURE / SYSTEM

| # | Loop | Status | Notes |
|---|------|--------|-------|
| 19 | v_project_health date calibration fix | Pending — SQL not yet drafted | False proximity alerts for past-dated projects |
| 20 | RLS policies for Supabase | HELD — do not enable until policies written | Enabling without policies blocks all access |
| 21 | C:\Users\Owner\.claude archive | HELD — do not delete | Keep until fully operational on D: |
| 22 | communications table empty | Blocked on M365 OAuth | No email/Teams data syncing |
