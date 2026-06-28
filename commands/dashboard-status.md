# /dashboard-status

Query the InterWork Command Center Supabase database for live operational status.
Read-only. No writes. Shows project counts, attention items, and checklist gaps.

**Project ref:** `hskgrxhdtgowagkfkjsw`

---

## Instructions

Use the Supabase MCP (`mcp__claude_ai_Supabase__execute_sql`) with project_id `hskgrxhdtgowagkfkjsw`.

### 1. Project counts by status
```sql
SELECT status, COUNT(*) AS count
FROM public.projects
GROUP BY status
ORDER BY count DESC;
```

### 2. Active projects needing attention
```sql
SELECT
  project_number,
  name,
  status,
  scheduled_date,
  vendor_confirmed,
  client_confirmed,
  access_confirmed,
  fastfield_submitted,
  completion_report_sent,
  pm_assigned
FROM public.projects
WHERE status IN ('approved','scheduled','in_progress','planning')
ORDER BY scheduled_date ASC NULLS LAST;
```

### 3. Upcoming projects (next 14 days)
```sql
SELECT project_number, name, scheduled_date, status, vendor_confirmed, client_confirmed
FROM public.projects
WHERE scheduled_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '14 days'
ORDER BY scheduled_date ASC;
```

### 4. Checklist gaps on active projects
```sql
SELECT p.project_number, p.name, ci.item, ci.category, ci.required_by
FROM public.checklist_items ci
JOIN public.projects p ON ci.project_id = p.id
WHERE ci.status = 'pending'
  AND p.status IN ('approved','scheduled','in_progress')
ORDER BY ci.required_by ASC NULLS LAST;
```

### 5. Recent communications (last 7 days)
```sql
SELECT p.project_number, c.source, c.direction, c.subject, c.from_address, c.occurred_at, c.important
FROM public.communications c
JOIN public.projects p ON c.project_id = p.id
WHERE c.occurred_at > NOW() - INTERVAL '7 days'
ORDER BY c.occurred_at DESC
LIMIT 20;
```

---

## Output Format

```
## Dashboard Status — [date]
Source: Supabase interwork-command-center | Read-only

### Projects by Status
inquiry: N | pending_approval: N | approved: N | scheduled: N | in_progress: N | completed: N

### Needs Attention (active/scheduled)
| # | Project | Date | Vendor ✅/❌ | Client ✅/❌ | Access ✅/❌ | FastField ✅/❌ |
|---|---------|------|-------------|-------------|-------------|----------------|
...

### Upcoming (next 14 days)
- [date] [project_number] [name] — vendor: ✅/❌ client: ✅/❌

### Open Checklist Items
- [project_number] | [category] | [item] | due: [date]

### Recent Communications
- [project_number] | [source] | [subject] | [date]

### Flags
- [any anomaly: scheduled project with no vendor, overdue items, etc.]
```

---

## Rules
- Read-only — no INSERT, UPDATE, or DELETE
- If a project has no `project_number`, flag it but do not assign one
- Surface conflicts (e.g. status=scheduled but vendor_confirmed=false) as flags, not auto-fixes
- See `memory/tool_notes/interwork_command_center_schema.md` for full schema reference
- See `memory/reference/interwork-command-center.md` for architecture and permission policy
