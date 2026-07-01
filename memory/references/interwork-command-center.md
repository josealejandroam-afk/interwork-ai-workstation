---
name: interwork-command-center
description: "Strategic reference for the InterWork AI Operations Engine — architecture, design principles, system roles, and success definition"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: manual
  review_after: 2026-09-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Command Center — Strategic Reference

## Core Framing

**Claude is the operations engine. The dashboard is one interface, not the brain.**

Alejandro spends time making decisions, not collecting information or moving data between systems.
Claude handles collection, preparation, verification, and routine updates.

---

## System Architecture

```
Alejandro
  └─→ Claude Code / AI Operations Engine
        ├─→ Supabase Dashboard     (write target, canonical operational DB)
        ├─→ Memory / RAG           (historical context, decisions, procedures, lessons)
        ├─→ Outlook/M365           (live signal source — work emails, BOLs, WC reports, vendor updates)
        ├─→ Microsoft Teams        (live signal source — conversations, project mentions)
        ├─→ Google Drive           (live signal source — documents, submittals, specs)
        └─→ Smartsheet             (read-only — scheduling source of truth)
```

**Smartsheet is never written to.** It is the scheduling source of truth, consumed by Claude.
**Supabase is the write target.** All confirmed project state lives there.

---

## Design Principles

1. **Claude is the operations engine. The dashboard is one interface.**
   The system works whether Alejandro is looking at a dashboard, a Teams chat, or a brief. Claude is the consistent layer.

2. **Supabase stores the canonical project state.**
   Any field displayed on the dashboard comes from Supabase. No other system is the source of truth for operational data.

3. **Smartsheet is read-only and should never be written to.**
   Claude reads schedule data from Smartsheet. Claude never writes, edits, or modifies Smartsheet rows.

4. **Memory/RAG stores historical context, decisions, procedures, and lessons learned.**
   When a project concludes or a decision is made, it goes to memory. Future Claude sessions can retrieve it without re-deriving it from emails or files.

5. **Outlook/M365, Teams, and Drive are live signal sources.**
   Claude reads these to surface what needs attention. Nothing is written to these systems without explicit approval.
   Gmail is Alejandro's personal account and is not a work signal source. Do not use Gmail for project data.

6. **Every meaningful project event should update memory or open loops.**
   A vendor delay, a scope change, a client approval — each goes to `open_loops/` or `projects/` in memory before it goes stale in an inbox.

7. **Never overwrite confirmed dashboard fields without human confirmation.**
   If a Supabase field already has a confirmed value (status, completion date, client name), Claude flags differences rather than silently overwriting.

8. **Never create or update dashboard projects without a confirmed project number.**
   Project numbers are the canonical identifier. Claude never creates a Supabase record without one.

9. **Automations should reduce Alejandro's manual work, reduce errors, or surface decisions earlier.**
   If an automation does not achieve at least one of these, it should not be built.

10. **Alejandro should spend time making decisions, not collecting information or moving data between systems.**
    Every workflow Claude runs should close the loop on something or prepare Alejandro to close it.

---

## System Roles Summary

| System | Role | Write? |
|--------|------|--------|
| Supabase | Canonical operational DB, dashboard backend | ✅ Yes (with confirmation) |
| Smartsheet | Schedule source of truth | ❌ Never |
| Memory / RAG | Historical context, decisions, lessons | ✅ Yes (automatic) |
| Outlook/M365 | Live signal — work emails, BOLs, WC reports (alejandroa@interworkoffice.com) | ❌ Read only (drafts shown for approval) — requires Graph API auth |
| Microsoft Teams | Live signal — conversations, project mentions | ❌ Read only (drafts shown for approval) |
| Google Drive | Live signal — docs, submittals, specs | ❌ Read only |

---

## Success Definition

Alejandro opens one screen and knows exactly what needs attention.

- **Projects on track** → stay quiet
- **Projects needing decisions** → surface automatically with context
- **Vendor emails, BOLs, FastFields, client updates** → prepared or drafted by Claude
- **Alejandro's role** → make judgment calls
- **Claude's role** → collect, prepare, verify, and route routine updates

---

## Architecture Decisions (adopted 2026-06-26)

### 1. Data authority split (confirmed)
- Supabase = current operational truth
- Memory/RAG = history, reasoning, decisions, lessons learned
- Smartsheet = read-only scheduling source
- Outlook/M365/Teams = live signal sources (Gmail = personal account, not a work source)

### 2. /dashboard-status stays lightweight and read-only
Queries only: project counts, active/upcoming projects, top missing fields, attention items.
No writes. No scoring logic. Fast and safe to run any time.

### 3. /project-health for deep scoring
Separate command. Combines `v_project_health` view (deterministic SQL) with Claude's judgment for context risks.
- green / yellow / red + numeric score (0–100)
- Phase-aware checks (imminent vs. far-out vs. overdue)
- Proximity-weighted risk (vendor penalty scales as date approaches)
- Recommended next action per project

### 4. Confirmation booleans are human-gated
`vendor_confirmed`, `client_confirmed`, `access_confirmed` are never auto-updated.
Claude may detect likely confirmations from communications and propose an update with evidence, but Alejandro must approve before any Supabase write.
Pattern: "Email received Jun 4 suggests vendor confirmed → propose `vendor_confirmed = true` on 7492. Approve?"

### 5. open_loops table in Supabase (APPLIED 2026-06-26)
Canonical open loops live in Supabase. Memory/open_loops/*.md files mirror them for RAG context.
Migration: `create_open_loops_table` (applied via MCP `apply_migration`)
Fields: id · project_id (nullable FK) · title · detail · status (open/resolved/snoozed) · priority · source · ai_generated · external_ref · created_at · updated_at · resolved_at

### 6. Communications table: enrich, don't replace
Use the existing `communications` table. Fields to add when ready:
- `body_ref` (reference path, not full body stored in DB)
- `matched_project_confidence` (float — how confident the AI is in the project match)
- `requires_action` (bool)
- `ai_classification` (text — vendor_confirmation, client_update, bol, access_info, etc.)
- `handled` (bool — loop resolved)
- `received_at` (alias or rename of occurred_at)
- `snippet` (short preview, not full body)
`external_id` + `thread_id` already exist for deduplication.

### 7. v_project_health view — deterministic SQL layer (APPLIED 2026-06-26)
Migration: `create_v_project_health_view` (applied via MCP `apply_migration`).
Note: SQL draft had `b.*` without alias — fixed to `FROM base AS b` on apply.
SQL handles hard rules (boolean checks, proximity windows, overdue detection).
Claude handles judgment/context risks (email content, open loops, pattern recognition).
Proximity weighting: vendor_confirmed penalty scales from 5 pts (far out) to 30 pts (≤3 days).
Known calibration issue: proximity checks (≤3/7/14 days) also trigger on past-dated scheduled
projects, producing false red alerts. Past-dated scheduled projects need status cleanup before
health scores are fully reliable. The 5 in_progress overdue projects are genuine reds.

### 8. RLS is a security project — not a quick fix
Do not apply RLS automatically.
First step: generate a report covering:
  - Current RLS status per table
  - Required frontend permissions (anon key usage)
  - Recommended policies per table
  - Migration SQL for review only
Then Alejandro decides what to apply and when.
Remediation SQL template is in `memory/references/interwork_command_center_schema.md`.

### 9. ai_action_queue table — controlled write audit trail (APPLIED 2026-07-01)
Migration: `create_ai_action_queue` (applied via MCP `apply_migration`).
Purpose: durable audit trail for AI-initiated dashboard writes, starting with `open_loop_create`/`open_loop_resolve` only (v1 scope). Full design in `docs/CONTROLLED_DASHBOARD_UPDATES.md`.
Schema mirrors `open_loops` conventions: `extensions.uuid_generate_v4()` PK default, RLS enabled, single `service_role`-only policy (`ai_action_queue_service_role_all`) — no anon/authenticated access, verified.
Key fields: `action_type`, `target_system`, `project_number`, `payload` (JSONB — exact request), `result` (JSONB — exact applied result), `target_record_id` (affected row id, e.g. an `open_loops.id`), `status` (`proposed`/`needs_confirmation`/`approved`/`rejected`/`applied`/`failed`), `reason`, `source`.
Schema-only so far — no endpoint built yet. Explicit-instruction-mode write flow (Alejandro's instruction = approval, endpoint applies immediately for low-risk types) is designed but not implemented; still requires a caller-auth decision (admin header vs. Vercel protection) before any code is written.

---

## Key Workflows (reference)

- `/brief-me` — daily operational dashboard from all live sources + open loops
- `/project-brief <number>` — full project state: Supabase (current) + memory/RAG (history) + Outlook/M365/Teams (signals)
- `/teams-brief` — recent Teams activity, open questions, waiting items
- `/find-open-loops` — unified queue across all sources
- `/rag-search <query>` — retrieve historical context, decisions, procedures
- `/rag-status` — index health and coverage check

---

## Permission Policy (reminder)

| Action | Level | Rule |
|--------|-------|------|
| Read any source | 1 — auto | Always allowed |
| Write to memory / RAG | 1 — auto | Always allowed |
| Draft an email or Teams reply | 2 — show user | Show draft, wait for approval |
| Write to Supabase | 2 — show user | Show change, wait for confirmation |
| Send email or Teams message | 3 — explicit | Must have explicit "send it" |
| Write to Smartsheet | ❌ Never | Hard rule — do not write |
