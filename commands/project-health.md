# /project-health

Deep health check for one or all active projects.
Combines deterministic Supabase scoring (v_project_health view) with Claude's judgment for context risks.

Usage:
- `/project-health` — score all active/scheduled projects
- `/project-health 7492` — score a single project
- `/project-health red` — show only red projects

**Read-only. Never updates confirmation booleans (vendor_confirmed, client_confirmed, access_confirmed) without Alejandro's explicit approval.**

---

## Step 1 — Query v_project_health

```sql
-- All active projects
SELECT * FROM public.v_project_health;

-- Single project
SELECT * FROM public.v_project_health WHERE project_number = '{NUMBER}';

-- Filter by color
SELECT * FROM public.v_project_health WHERE health_color = 'red';
```

If `v_project_health` does not exist yet (view not applied), fall back to the raw query from `/dashboard-status` and compute health inline.

---

## Step 2 — Phase-aware interpretation

Apply judgment on top of the deterministic score:

| Phase | Extra checks Claude applies |
|-------|-----------------------------|
| `scheduled` ≤7 days | Check open_loops for unresolved vendor/access items |
| `in_progress` | Check if fastfield_submitted; flag if not |
| `in_progress` past date | Flag for completion report + status update |
| Any | Check communications table for recent activity that may resolve a flag |

**Detecting likely confirmations (propose only, never auto-apply):**
If a recent `communications` row has `source='outlook'` or `source='teams'` and the subject/body suggests confirmation (e.g. "confirmed", "we're set", "see you on"), note it as a *proposed* update:
> "Vendor email received 2026-05-12 may confirm vendor. Propose setting vendor_confirmed = true on project 7492. Approve?"

---

## Step 3 — Open loops cross-reference

Query any open loops linked to this project:
```sql
-- Once open_loops table exists:
SELECT title, priority, source, created_at
FROM public.open_loops
WHERE project_id = (SELECT id FROM public.projects WHERE project_number = '{NUMBER}')
  AND status = 'open';
```

Until then, check `memory/open_loops/` for files with matching project number.

---

## Output Format

```
## Project Health — [scope] — [date]

### 🔴 Red  (N projects)
| # | Project | Date | Score | Top Risk | Recommended Action |
|---|---------|------|-------|----------|--------------------|
| 7060 | MMC Dallas Galleria | Apr 3 | 32 | overdue_in_progress | Send completion report, update status |

### 🟡 Yellow  (N projects)
| # | Project | Date | Score | Top Risk | Recommended Action |
...

### 🟢 Green  (N projects)
| # | Project | Date | Score | — |
...

---

### Proposed Confirmation Updates (not applied)
> These require Alejandro's approval before any Supabase write.
- Project 7492: email from vendor on Jun 4 suggests confirmation → propose vendor_confirmed = true
- ...

### Open Loops by Project
- 7492 (Radian Decom Denver): teams-20260701-001 — waiting on John Smith

### Flags for Claude Judgment (not in SQL)
- [any context risk not capturable in a boolean]
```

---

## Write Rules
- **Never** set `vendor_confirmed`, `client_confirmed`, or `access_confirmed` without explicit approval
- If proposing a boolean update: show the evidence (email/message snippet), show the proposed SQL, wait for "approve" before writing
- All Supabase writes must log to `activity_log` with `actor='claude'` and `source='manual'`
- See `memory/references/interwork-command-center.md` for full permission policy
