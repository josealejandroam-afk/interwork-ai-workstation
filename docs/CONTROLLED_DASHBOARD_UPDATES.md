# Controlled Dashboard Updates — Design (Planning Only)
_Created: 2026-07-01_
_Revised: 2026-07-01 — corrected target architecture: explicit instruction = apply, not propose-only_
_Revised: 2026-07-01 — ai_action_queue schema applied (v1 scope: open_loop_create/open_loop_resolve); endpoint still not built_
_Status: Schema live. Endpoint not yet built — no caller-auth decision made, no code written._

---

## Purpose

Define how Claude Chat (and other AI tools) can update the live dashboard (Supabase) when Alejandro explicitly instructs it to — **without Chat ever holding database credentials or writing to Supabase directly, and without requiring a separate Claude Code session for every routine update.**

**Target architecture:**

```
Alejandro gives Chat an explicit instruction
      ↓
Chat calls a protected server-side API endpoint (not Supabase directly)
      ↓
Endpoint validates the request
      ↓
Endpoint writes an audit/action row (ai_action_queue) — the record of what happened and why
      ↓
Endpoint applies the update to Supabase, using the service role server-side only,
IF the instruction was explicit and the change is low-risk
      ↓
Endpoint returns a confirmation; Chat reports back to Alejandro
      ↓
Repo memory update handoff created, if durable context should also change
```

**What this is not:**
- Not "Chat writes to Supabase directly" — Chat never holds a Supabase key, service role or otherwise.
- Not "Chat can only propose, and Alejandro must separately go apply it in Claude Code" — that was the wrong framing in the first draft of this document. Explicit instruction from Alejandro *is* the approval. The endpoint applies it in the same flow, then confirms.
- Not unrestricted write access — the endpoint enforces which update types can apply immediately (low-risk, explicitly instructed) versus which must stop and ask.

---

## 1. Why Chat Cannot Write to Supabase Directly Today

- Supabase credentials are never passed into Claude Chat sessions — passing them through chat is a security anti-pattern (see `DASHBOARD_AI_ACCESS_MODEL.md`).
- The live `/api/ai/*` endpoints are intentionally read-only, using the anon key with RLS enforcing read-only access on every table they touch (see `AI_ACCESS_LAYER_V1.md`).
- Claude Code, which does have Supabase MCP write access, follows a strict manual approval procedure for complex writes today (`APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`) — appropriate for status/closeout writes with financial or reporting consequences, but too heavy for routine updates like "mark FF submitted" or "add an open loop."
- There is currently no durable audit record of "AI applied X, on Alejandro's instruction, at time T" for anything outside a live Claude Code session — git history is explicitly not an audit trail (`APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`).

**The fix is not "make Chat ask permission every time and route everything back to Claude Code."** The fix is a protected server-side endpoint that Chat can call directly, which holds the Supabase credentials Chat itself never sees, and which logs every write it makes.

---

## 2. Desired Future Behavior

Two concrete examples of the target experience:

> Alejandro: "FF submitted for 7492, update dashboard."
> Chat calls the protected endpoint → dashboard's `fastfield_submitted` flips to true on 7492 → an audit row is written → Chat confirms: "Done — 7492 fastfield_submitted set to true."

> Alejandro: "Add COI as an open loop for 7492."
> Chat calls the protected endpoint → a new `open_loops` row is created → an audit row is written → Chat confirms the loop was added.

Neither example requires Alejandro to separately open Claude Code and approve a queued row. The instruction itself, given explicitly and covering a low-risk update type, is the approval. The audit trail exists so Alejandro can review what was changed and why — not so every change has to wait on a second review step.

Complex/ambiguous writes (the kind `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` was built for) are the exception, not the default — see Section 4's risk tiers.

---

## 3. Two Modes

### Default mode — infer, don't assume

If Chat infers a plausible update from conversation but Alejandro did not clearly instruct it (e.g. Alejandro mentions in passing that a delivery happened, without saying "update the dashboard"), Chat proposes or asks. It does not call the apply endpoint on its own initiative.

### Explicit instruction mode — instruction is approval

If Alejandro clearly instructs an update — phrases like "update dashboard," "mark complete," "mark FF submitted," "client informed," "add open loop," "close open loop," and equivalents — that instruction **counts as approval** for low-risk operational update types (Section 4). Chat calls the apply endpoint in the same turn and reports the result. No separate queued-approval round trip for these.

This mirrors the existing rule everywhere else in this repo: drafts are free, sends/writes need Alejandro's explicit word (`"send it"`, `"approve"`, `"apply"` — see `ACCESS_AND_SAFETY_RULES.md`). What changes here is *where* that explicit instruction gets executed — through a protected API in the same conversation, not exclusively through a separate Claude Code session.

---

## 4. Update Types and Risk Tiers

### Low-risk — apply immediately on explicit instruction

| Type | Target | Example |
|---|---|---|
| `project_readiness_update` | `supabase_dashboard` | Mark `fastfield_submitted`, `client_informed`, `client_confirmed`, `vendor_confirmed`, or `access_confirmed` true/false |
| `project_pm_update` | `supabase_dashboard` | Assign/change PM, when Alejandro names the PM or it's a known InterWork PM (see `KEY_PEOPLE.md`) |
| `project_date_update` | `supabase_dashboard` | Update `scheduled_date`/`scheduled_start_time` when Alejandro provides the date/time |
| `project_status_update` | `supabase_dashboard` | Update `status` when Alejandro states it clearly (e.g. "mark it in progress") |
| `open_loop_create` | `supabase_dashboard` | New row in `open_loops` |
| `open_loop_update` | `supabase_dashboard` | Edit an existing open loop |
| `open_loop_resolve` | `supabase_dashboard` | Mark an open loop resolved |
| `contact_update` | `repo_memory` or `both` | New/changed contact info for a project or client |
| `warehouse_route_context` | `repo_memory` | Route/logistics note tied to warehouse usage |
| `repo_memory_update_handoff` | `repo_memory` | Durable context change that doesn't touch Supabase at all |
| `project_scope_summary_update` | `supabase_dashboard` | Add an operational note / update `scope_summary` text |

### Needs confirmation, or reject outright — never apply immediately

- Delete a project
- Change a project number
- Overwrite a confirmed client identity (name mismatch resolution — same caution as `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` already applies to)
- Clear/null out an important field without a stated reason
- Bulk updates (more than one project per call)
- Anything ambiguous — instruction doesn't clearly name the project, field, or new value
- Anything touching `invoiced`, `completion_report_sent`, or `actual_end_at` — these have financial/reporting consequences and stay on the existing manual field-by-field checklist procedure indefinitely, per `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`
- Secrets, credentials, tokens in any field

These are written to `ai_action_queue` with `status = 'needs_confirmation'` and stop there — Chat tells Alejandro what it would do and waits for explicit confirmation before a second call actually applies it.

---

## 5. Controlled Action Queue — Audit Trail, Not a Bottleneck

`ai_action_queue` is not a manual approval gate that every update must wait in. It is:

- **The audit trail.** Every apply — whether immediate (low-risk + explicit instruction) or confirmed-later (needs_confirmation → approved) — gets a row. Alejandro can always see what changed, when, on whose instruction, and why.
- **The safety layer for the exceptions.** High-risk/ambiguous updates stop at `needs_confirmation` instead of applying, and require a second explicit step before they apply.
- **Still never silently applied without some form of Alejandro instruction** — for low-risk types, that instruction is the chat message itself; for needs_confirmation types, it's a follow-up confirmation.

### Flow for low-risk + explicit instruction (the common case)

```
1. Alejandro gives an explicit instruction in chat
2. Chat calls POST /api/ai/actions/apply
3. Endpoint validates: is this a known low-risk type? is the instruction unambiguous?
4. Endpoint writes the ai_action_queue row: status starts 'proposed', immediately set
   reviewed_by = 'alejandro (explicit instruction)', reviewed_at = now(), status = 'approved'
5. Endpoint applies the write to Supabase (and/or repo memory) in the same request
6. Row updated: status = 'applied', applied_at = now() (or 'failed' + error if the write itself fails)
7. Endpoint returns confirmation; Chat reports the result to Alejandro
```

### Flow for needs_confirmation (the exception case)

```
1. Chat detects an ambiguous or high-risk request
2. Chat calls the endpoint (or just responds directly) with status = 'needs_confirmation'
3. Chat asks Alejandro to confirm the exact change
4. Alejandro confirms explicitly
5. Chat calls apply again, now treated as an explicit low-risk-equivalent instruction, OR
   escalates to the manual Claude Code / APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md procedure
   if it's one of the categories that never gets a simple apply path (financial/reporting fields)
```

---

## 6. Safety Rules

- **Instruction, not inference, triggers an apply.** Chat only calls the apply endpoint when Alejandro's message clearly authorizes the specific change — not when Chat merely infers one might be warranted.
- **Chat never holds Supabase credentials of any kind.** The endpoint holds the service role key server-side; Chat only ever calls the endpoint over HTTPS with whatever caller-auth the endpoint requires (Section 8).
- **Every applied row must state its evidence/source** (`reason`, `source` fields) — no apply without a stated basis, same as the existing "no invented facts" rule.
- **One project/one field per call where possible** — mirrors the field-independence policy in `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`. No bundling unrelated changes into one call.
- **Financial/reporting fields (`invoiced`, `completion_report_sent`, `actual_end_at`) never go through the immediate-apply path**, regardless of how explicit the instruction sounds — they stay on the manual checklist procedure.
- **RLS on `ai_action_queue`** restricts `anon`/`authenticated` from reading or writing rows — this table is exactly as locked down as `open_loops` (service_role only).
- **No secrets, tokens, or credentials ever go in `proposed_change`/`reason`/`source`** — same rule as everywhere else in this repo.
- **Every apply is logged before the write executes**, not after — if the write fails partway, there's still a row showing what was attempted.

---

## 7. Schema — APPLIED 2026-07-01

Migration `create_ai_action_queue`, applied via Supabase MCP and verified (table exists, all 19 columns match, RLS enabled, single `service_role`-only policy, both indexes present, `anon` confirmed denied).

```sql
-- APPLIED 2026-07-01. Reflects the live schema.

CREATE TABLE public.ai_action_queue (
    id                UUID PRIMARY KEY DEFAULT extensions.uuid_generate_v4(),

    action_type       TEXT NOT NULL,               -- see Section 4 update types
    target_system     TEXT NOT NULL DEFAULT 'supabase_dashboard'
                           CHECK (target_system IN ('supabase_dashboard', 'repo_memory', 'both')),

    project_number    TEXT,                        -- nullable — some actions aren't project-scoped
    client            TEXT,

    title             TEXT NOT NULL,                -- short human-readable summary
    proposed_change   TEXT NOT NULL,                -- what is being applied/proposed, in plain language
    payload           JSONB NOT NULL DEFAULT '{}'::jsonb,  -- exact structured request body from Chat
    result            JSONB,                        -- exact structured result after apply (null until applied)
    target_record_id  TEXT,                         -- affected row id, e.g. an open_loops.id
    reason            TEXT NOT NULL,                -- evidence/source basis for the change
    source            TEXT NOT NULL DEFAULT 'chat',  -- e.g. "Claude Chat — explicit instruction"

    status            TEXT NOT NULL DEFAULT 'proposed'
                           CHECK (status IN ('proposed', 'needs_confirmation', 'approved', 'rejected', 'applied', 'failed')),

    created_by        TEXT NOT NULL,                -- which AI/session created the row
    reviewed_by       TEXT,                         -- 'alejandro (explicit instruction)' for immediate-apply, or Alejandro's name once confirmed
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    reviewed_at        TIMESTAMPTZ,
    applied_at         TIMESTAMPTZ,
    error             TEXT,

    repo_handoff_path  TEXT           -- if a repo memory handoff was generated for this action
);

ALTER TABLE public.ai_action_queue ENABLE ROW LEVEL SECURITY;
CREATE POLICY ai_action_queue_service_role_all
    ON public.ai_action_queue
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE INDEX ai_action_queue_status_idx ON public.ai_action_queue (status);
CREATE INDEX ai_action_queue_project_number_idx ON public.ai_action_queue (project_number);
```

Schema is deliberately close to `open_loops` in shape (same `extensions.uuid_generate_v4()` PK default — confirmed as the dominant convention across 14 of 15 existing tables — same RLS pattern) to reuse an already-reviewed, already-working pattern rather than invent a new one. `payload`/`result` (JSONB) preserve the exact request/response for each action; `target_record_id` points at the affected row (e.g. an `open_loops.id`) without a formal FK, so it can reference rows across different target tables over time. The `needs_confirmation` status is the structural addition that lets high-risk/ambiguous requests stop instead of applying.

**Table is live and empty (0 rows).** No endpoint exists yet — nothing can write to it outside of Claude Code/Supabase MCP until the `apply` endpoint (Section 8) is built and approved.

---

## 8. Minimum Viable API Endpoints (design only — do not build yet)

```
POST /api/ai/actions/apply        — validates and applies a low-risk, explicitly-instructed update
                                     in one call; writes the audit row and the actual Supabase/repo
                                     write together. THIS IS THE PRIMARY ENDPOINT for the target
                                     experience in Section 2.
GET  /api/ai/actions/pending      — list needs_confirmation rows awaiting a human decision
POST /api/ai/actions/:id/confirm  — Alejandro (via Chat, after being asked) confirms a
                                     needs_confirmation row, which then applies
POST /api/ai/actions/:id/reject   — Alejandro rejects a needs_confirmation row
```

`propose`/`approve` as separate endpoints (the original draft of this document) are folded into `apply` for the low-risk path — there's no reason to force two round trips when the instruction was already explicit. They still exist conceptually for the `needs_confirmation` path (`pending` + `confirm`/`reject`).

### Access rule

**These are write endpoints — they must never be public/unauthenticated**, unlike the existing read endpoints (`dashboard-summary`, `search`, `project`, `open-loops`), which are intentionally open because they only ever return already-public-ish operational data through a curated safe view.

Before any of these are built, pick one protection strategy:

1. **Shared admin header** — a long random secret stored only in Vercel environment variables (never in this repo, never sent to a client-side context), required on every call to `/api/ai/actions/*`. Whatever session calls this endpoint on Chat's behalf holds the header; Chat itself still never sees a Supabase key. Simplest option that still supports "Chat calls the endpoint directly in the same turn."
2. **Vercel-protected function / deployment protection** — reuse Vercel's own auth gate scoped to just the `/api/ai/actions/*` routes. More setup, no custom secret to manage, but less obviously compatible with a Chat-initiated HTTP call without a browser session.
3. **Supabase service role, server-side only** — regardless of which caller-auth option is picked, the endpoint itself is the only thing that ever holds the service role key, and only in server-side environment variables. Never expose it to any client-reachable code path, and never expose it to Chat.

**Recommendation:** option 1 (shared admin header) is the most compatible with the target experience — Chat calling the endpoint directly, in-conversation, without a human opening a separate authenticated session. The header secret's blast radius is limited to this one set of write endpoints, and it never appears in this repo or in any chat transcript.

All writes — immediate-apply or confirmed-later — are logged to `ai_action_queue` regardless of which protection strategy is chosen.

---

## 9. What Should Be Deferred

- **Any actual endpoint implementation** — this document is planning only. Nothing in Section 8 gets built until the schema (Section 7) is reviewed, approved, and applied, and Alejandro explicitly asks for the endpoint work.
- **Bulk updates** — the apply endpoint should reject anything touching more than one project per call, at least initially.
- **Any UI/admin view for reviewing the queue** — reviewing via Claude Code/Supabase MCP query is sufficient for v1; a dashboard view for the queue itself is a separate, later feature.
- **Financial/reporting-consequence fields going through any apply path at all** (`invoiced`, `completion_report_sent`, `actual_end_at`) — these stay on `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` indefinitely, not just until the queue "has a track record." This is a durable exception, not a phase-in.
- **Auto-resolving `needs_confirmation` rows** — those always require a distinct confirmation step; only the low-risk explicit-instruction path applies immediately.

---

## Recommended Next Build Step

```
1. DONE — ai_action_queue schema drafted, reviewed, approved, applied, and verified (2026-07-01)
2. NEXT — prove the workflow manually first: Claude Code inserts one real/test row end-to-end
   (created → approved-by-instruction → applied, for a real open_loop_create or open_loop_resolve)
   via MCP, no endpoint yet, to validate the schema and status transitions before any HTTP surface exists
3. Design and build the protected POST /api/ai/actions/apply endpoint (Section 8), with a
   caller-auth decision (admin header vs. Vercel protection) made explicitly before any code is written
4. Test with one real low-risk explicit-instruction update end-to-end through the endpoint
   before treating this as available for regular use
```

---

## Related Docs

- [`AI_ACCESS_LAYER_V1.md`](AI_ACCESS_LAYER_V1.md) — the existing read-only layer this design extends
- [`DASHBOARD_AI_ACCESS_MODEL.md`](DASHBOARD_AI_ACCESS_MODEL.md) — earlier read-path model; its "Future Optional Improvement" section first floated a write endpoint idea, now superseded by this document's design
- [`HANDS_EYES_EARS_MODEL.md`](HANDS_EYES_EARS_MODEL.md) — current capability matrix (Hands/Eyes/Ears) across AI systems
- [`APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`](APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md) — the existing manual, field-by-field write procedure that financial/reporting-consequence writes continue to use indefinitely
