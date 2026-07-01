# AI Access Layer v1
_Created: 2026-07-01_
_Updated: 2026-07-01_
_Status: Live — read path complete, including open loops_

---

## Purpose

Define the stable, global read path any AI (Claude Chat, Claude Code, Cowork, ChatGPT) uses to answer questions about InterWork projects — without guessing, without client-specific logic, and without silently treating two different data sources as one.

v1 scope is **read-only**. Write capability (controlled action queue) is a future phase, not part of this build.

---

## Global Read Path

```
Search endpoint
      ↓
Dashboard endpoint
      ↓
Project endpoint
      ↓
Repo memory
      ↓
Claude Code handoff (if durable changes are needed)
```

1. **Search** (`/api/ai/search?q=`) — find candidate projects/clients by loose term.
2. **Dashboard** (`/api/ai/dashboard-summary`) — today/tomorrow/this-week/at-risk operational snapshot across all projects.
3. **Project** (`/api/ai/project?number=`) — exact live record for one project, by project number.
4. **Repo memory** (`memory/clients/<slug>/projects/<slug>/`) — durable context Supabase doesn't carry: deeper scope, contacts, notes, history, open loops.
5. **Claude Code handoff** — if a durable change is needed (updating repo memory, committing, pushing), that's a separate step from reading — it is not automatic.

---

## Source-of-Truth Rule

Supabase and the GitHub repo are **two different systems**, not mirrors. They are allowed to disagree.

| System | Owns |
|---|---|
| Supabase / API (`v_project_card`) | Live operational dashboard status — schedule, status, readiness, execution owner — for **all** projects |
| GitHub repo memory | Durable operational memory for all clients/projects — deeper scope, contacts, notes, history, open loops |

**If they conflict, flag the conflict instead of guessing.** The expected AI behavior is:

> "Dashboard says X. Repo memory says Y. These differ because repo memory contains newer operational knowledge not yet synchronized back to Supabase."

This is not a bug state. Repo memory is often updated ahead of Supabase (e.g. a client call confirms new scope) — Supabase catches up only when someone re-syncs Smartsheet or edits the record directly. Never silently prefer one source; say which is which.

---

## Endpoint Inventory

| Endpoint | Data source | Status |
|---|---|---|
| `GET /api/ai/dashboard-summary` | Supabase `v_project_card` | Live |
| `GET /api/ai/search?q=<term>` | Supabase `v_project_card` | Live |
| `GET /api/ai/project?number=<project_number>` | Supabase `v_project_card` | Live — global, exact `project_number` match, any InterWork project |
| `GET /api/ai/open-loops` | Supabase `v_open_loops_ai` | Live — production-verified 2026-07-01. Currently returns an empty list (`count: 0`, `open_loops: []`) until open-loop rows are created. |

The first three endpoints are read-only, use the same direct Supabase REST fetch with the anon key (no `lib/supabase.js`, no service role), and share one safe-field mapper (`lib/aiProjectCard.mjs` in `interwork-command-center`) so the redacted-field boundary (no `internal_notes`, emails, phone numbers, secrets) is defined in exactly one place.

`/api/ai/project` is **global** — it takes any `project_number` and returns whatever `v_project_card` has for it. It contains no client names, no project numbers, and no per-client branching in its implementation.

`/api/ai/open-loops` follows the same anon-key, read-only pattern but reads a dedicated safe view rather than a project-card view — see below.

### Open loops — table, view, and endpoint

- `public.open_loops` is the canonical table (applied 2026-06-26). **RLS is enabled** with a single policy, `open_loops_service_role_all`, scoped to `service_role` only — `anon`/`authenticated` get zero rows on direct table access.
- `public.v_open_loops_ai` is the curated, AI-facing read view (applied 2026-07-01) that the endpoint actually queries. It exposes only `id, project_number, title, status, priority, source, ai_generated, created_at, updated_at, resolved_at` — it deliberately excludes `detail` (free-text, could contain PII), `external_ref`, and raw `project_id`. `title` is also redacted for obvious email/phone patterns in the endpoint's mapper (`lib/aiOpenLoops.mjs`) before it's returned.
- `GET /api/ai/open-loops` supports `status`, `priority`, and `project_number` filters only (v1 scope — no `client` or `at_risk` filter yet).
- Because the raw table has zero rows right now, an empty response is expected, not an error — don't treat `count: 0` as a health problem.

---

## Explicitly Out of Scope for v1

- Controlled action queue / `pending_actions` (AI drafts a write → human approves → system executes) — this is the "hands" phase, not part of the read layer.
- Slug-based project route (`/api/ai/project/[client_slug]/[project_slug]`) — superseded by the numeric endpoint; project number is the operational primary key already used across QuoteWerks, FastField, and Smartsheet, so a second lookup shape isn't needed.
- `client` and `at_risk` filters on `/api/ai/open-loops` — deferred to a later revision.

---

## Deployment Note (2026-07-01)

Vercel preview-deployment protection (**Require Log In**) was temporarily disabled on `interwork-command-center` to allow direct HTTP testing of the `/api/ai/open-loops` build/verification cycle. It should be re-enabled manually in Vercel → `interwork-command-center` → Settings → Deployment Protection. This does not affect production — production has never required a change to deployment protection.

---

## Related Docs

- [`AI_ACCESS_ENDPOINT_IMPLEMENTATION_PLAN.md`](AI_ACCESS_ENDPOINT_IMPLEMENTATION_PLAN.md) — endpoint-by-endpoint build history and response shapes
- [`HANDS_EYES_EARS_MODEL.md`](HANDS_EYES_EARS_MODEL.md) — read vs write boundaries across all InterWork AI surfaces
