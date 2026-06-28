# InterWork Command Center — Dashboard URL
**Recorded:** 2026-06-28

---

## Frontend Dashboard (user-facing)

**URL:** https://interwork-command-center.vercel.app/

**Host:** Vercel
**Purpose:** User-facing operational dashboard — project status, schedule, health views
**Access:** Alejandro only (or approved team members)

---

## Architecture Clarification

| Layer | URL / Location | Purpose |
|-------|---------------|---------|
| **Frontend dashboard** | `https://interwork-command-center.vercel.app/` | What users see and interact with |
| **Backend / API** | Supabase project `hskgrxhdtgowagkfkjsw` — URL stored in `SUPABASE_URL` env var | Database, API, auth — not a user-facing URL |
| **Supabase Studio** | Accessed via Supabase dashboard (supabase.com) with project credentials | Admin/schema/SQL — not the operational dashboard |

The Vercel dashboard URL and the `SUPABASE_URL` env var are **different things**. Do not confuse them:
- `SUPABASE_URL` is the Supabase API endpoint used by the backend and by Claude's MCP tools.
- `https://interwork-command-center.vercel.app/` is the deployed frontend that end users open in a browser.

---

## Usage Rules

- **Dashboard testing is read-only** unless Alejandro explicitly approves a write action.
- Do not use the dashboard UI to trigger data changes without the same approval process required for direct Supabase writes.
- Dashboard data reflects the Supabase backend — changes made via the dashboard write to the same database that Claude's read-only queries target.
- If the dashboard exposes any write actions (status updates, form submissions, etc.), treat them under the same approval rules as `APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md`.

---

## Connection Status

| Check | Status |
|-------|--------|
| Supabase backend | Connected — read-only confirmed 2026-06-28 |
| Vercel frontend | URL confirmed 2026-06-28 — not yet browser-tested in this session |
| Dashboard writes | Blocked until Alejandro explicit approval |

---

*URL recorded for reference. No browser automation used. No writes performed.*
