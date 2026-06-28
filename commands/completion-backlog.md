# /completion-backlog

Read-only command. Shows all projects past their scheduled date that are not yet
completed or closed, grouped by evidence level.

Purpose: replace one-by-one stalled-project review with a structured triage view.
Use this output to decide what needs Alejandro's eyes, not to auto-update anything.

**Never writes. Never updates status, booleans, or any field.**

---

## Step 1 — Query past-dated active projects

```sql
SELECT
    p.project_number,
    p.name,
    p.status,
    p.scheduled_date,
    (CURRENT_DATE - p.scheduled_date)::int          AS days_past,
    p.fastfield_submitted,
    p.completion_report_sent,
    p.actual_end_at,
    p.pm_assigned,
    p.vendor_required,
    p.fastfield_submitted
        OR p.completion_report_sent
        OR p.actual_end_at IS NOT NULL              AS has_completion_signal,
    (CURRENT_DATE - p.scheduled_date)::int <= 14    AS recently_ended,
    p.name ILIKE '%phase%'
        OR p.name ILIKE '%multi%'
        OR p.name ILIKE '%punch list%'
        OR p.name ILIKE '%walkthrough%'             AS phase_or_scope_flag
FROM public.projects p
WHERE p.status NOT IN ('completed', 'closed', 'cancelled')
  AND p.scheduled_date < CURRENT_DATE
ORDER BY
    CASE
        WHEN p.fastfield_submitted OR p.completion_report_sent OR p.actual_end_at IS NOT NULL
            THEN 0
        WHEN (CURRENT_DATE - p.scheduled_date)::int <= 14
            THEN 1
        ELSE 2
    END,
    p.scheduled_date ASC;
```

---

## Step 2 — Cross-reference open_loops

```sql
SELECT
    pr.project_number,
    ol.title,
    ol.status,
    ol.source,
    ol.priority,
    ol.created_at
FROM public.open_loops ol
JOIN public.projects pr ON ol.project_id = pr.id
WHERE pr.status NOT IN ('completed', 'closed', 'cancelled')
  AND pr.scheduled_date < CURRENT_DATE
  AND ol.status = 'open'
ORDER BY pr.project_number;
```

Also check `memory/open_loops/` for any `.md` files referencing the same project numbers
(memory loops are not yet synced to the Supabase open_loops table).

---

## Step 3 — Group into evidence buckets

Apply the following logic to each project:

| Bucket | Rule |
|--------|------|
| `likely_complete` | `fastfield_submitted = true` OR `completion_report_sent = true` OR `actual_end_at IS NOT NULL` |
| `recently_ended_monitor` | None of the above AND `days_past <= 14` |
| `stalled_needs_review` | None of the above AND `days_past > 14` AND no scope/phase flag |
| `scope_risk` | `phase_or_scope_flag = true` — multi-phase or punch-list projects; can't auto-confirm complete |
| `open_loop_active` | Has an open entry in `open_loops` or `memory/open_loops/` — do not close, actively tracked |

---

## Step 4 — Flag candidates excluded from batch actions

Projects that should NOT be batch-confirmed even if `fastfield_submitted = true`:
- Any project where `actual_end_at` is earlier than `scheduled_date` — suggests date mismatch or reopened work
- Any project with an open loop (source = teams, outlook, or manual) still in status = open
- Projects with "Phase", "Multi-Phase", "Punch List" in the name — scope may be ongoing

---

## Output Format

```
## Completion Backlog — [date]
Source: v_project_health + projects table | Read-only

### Summary
past-dated-active: N | likely_complete: N | recently_ended: N | stalled: N | scope_risk: N | open_loop_active: N

### Likely Complete (has FastField / completion report / actual_end_at)
| # | Project | Scheduled | Days Past | Signal | Flag |
|---|---------|-----------|-----------|--------|------|
| 7053 | Strategic Education Washington DC | 2026-03-21 | 97 | fastfield ✅ | — |
| 7364 | MMC Allentown Move | 2026-03-19 | 99 | fastfield ✅ actual_end_at ✅ | ⚠️ actual_end_at < scheduled_date |

Proposed action (requires Alejandro approval): status → completed for clean ones.

### Recently Ended — Monitor (≤14 days past, no signal)
| # | Project | Scheduled | Days Past |
...

### Stalled — Needs Review (>14 days past, no signal)
| # | Project | Scheduled | Days Past | PM |
...
Sort: most overdue last (give benefit of the doubt to older projects — they're probably done).

### Scope Risk (multi-phase or punch list — do not auto-confirm)
| # | Project | Scheduled | Days Past | Note |
...

### Open Loop Active (tracked — do not auto-close)
| # | Project | Scheduled | Open Loop | Source |
...

### Proposed Next Actions (not applied)
> These require Alejandro's approval before any Supabase write.
- [project_number]: [reason] → proposed action
```

---

## Rules

- **Never** write, update, or delete anything
- If proposing status changes: list them clearly, wait for "approve"
- Do not flag `actual_end_at < scheduled_date` as an error — surface it as a question
- Completion signal pipeline (FastField/WC report → Supabase) is the durable fix; this command is for interim visibility
- See `memory/references/interwork-command-center.md` for full permission policy
