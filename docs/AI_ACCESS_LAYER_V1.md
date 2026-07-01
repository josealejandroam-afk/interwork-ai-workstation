# AI Access Layer v1
_Created: 2026-07-01_
_Status: Live — read path complete_

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

All three endpoints are read-only, use the same direct Supabase REST fetch with the anon key (no `lib/supabase.js`, no service role), and share one safe-field mapper (`lib/aiProjectCard.mjs` in `interwork-command-center`) so the redacted-field boundary (no `internal_notes`, emails, phone numbers, secrets) is defined in exactly one place.

`/api/ai/project` is **global** — it takes any `project_number` and returns whatever `v_project_card` has for it. It contains no client names, no project numbers, and no per-client branching in its implementation.

---

## Explicitly Out of Scope for v1

- `GET /api/ai/open-loops` — blocked on `open_loops` table actually existing live in Supabase (`scripts/sql/draft_open_loops_table.sql` is drafted, not yet applied/approved). Build after the migration lands.
- Controlled action queue / `pending_actions` (AI drafts a write → human approves → system executes) — this is the "hands" phase, not part of the read layer.
- Slug-based project route (`/api/ai/project/[client_slug]/[project_slug]`) — superseded by the numeric endpoint; project number is the operational primary key already used across QuoteWerks, FastField, and Smartsheet, so a second lookup shape isn't needed.

---

## Related Docs

- [`AI_ACCESS_ENDPOINT_IMPLEMENTATION_PLAN.md`](AI_ACCESS_ENDPOINT_IMPLEMENTATION_PLAN.md) — endpoint-by-endpoint build history and response shapes
- [`HANDS_EYES_EARS_MODEL.md`](HANDS_EYES_EARS_MODEL.md) — read vs write boundaries across all InterWork AI surfaces
