# System Capability Matrix

**InterWork AI Operations Engine**  
Last updated: 2026-06-29

---

## Architecture

```
[Smartsheet]  ──read-only──►  [Claude]
[Outlook/M365]──read-only──►  [Claude]  ──write-proposed──►  [Supabase DB]
[Read AI]     ──read-only──►  [Claude]                            │
[Teams]       ──read-only──►  [Claude]        ▼              [activity_log]
[FastField]   ──manual/file►  [Claude]   [Memory / RAG]
```

---

## Command Inventory

### Tier 1 — Live (Supabase connected)

| Command | File | Type | What it does |
|---------|------|------|-------------|
| `/dashboard-status` | commands/dashboard-status.md | Read-only | Project counts, attention items, health overview |
| `/project-health` | commands/project-health.md | Read-only | Deep scoring via `v_project_health` view; red/yellow/green |
| `/completion-backlog` | commands/completion-backlog.md | Read-only | Triage past-dated projects still marked scheduled/in_progress |
| `/completion-intake` | commands/completion-intake.md | Write-proposed | Accepts FastField / WC report / email → proposes status updates |
| `/ff-sent` | commands/ff-sent.md | Write-proposed | Records FF dispatched to PM; creates open loop; never sets `fastfield_submitted` |

**Requires:** `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` env vars set.

---

### Tier 2 — Live (local / memory-based)

| Command | File | Type | What it does |
|---------|------|------|-------------|
| `/rag-search` | commands/rag-search.md | Read-only | Hybrid BM25 + vector search over memory and procedures |
| `/rag-status` | commands/rag-status.md | Read-only | RAG index health, chunk count, staleness check |
| `/find-open-loops` | commands/find-open-loops.md | Read-only | Surfaces unresolved open loops from memory files |
| `/brief-me` | commands/brief-me.md | Read-only | Local-only morning brief from memory and RAG |
| `/feedback-status` | commands/feedback-status.md | Read-only | Feedback loop file state and freshness |

**Requires:** RAG index built locally. No external connections needed.

---

### Tier 3 — Partial (M365 / Teams OAuth pending)

| Command | File | Type | Blocker |
|---------|------|------|---------|
| `/teams-brief` | commands/teams-brief.md | Read-only | Teams OAuth re-auth (alejandroa@interworkoffice.com) |
| `/readai-brief` | commands/readai-brief.md | Read-only | Read AI MCP CLI auth |
| `/meeting-intake` | commands/meeting-intake.md | Write-proposed | Mode A needs M365; Mode B (paste) works now |
| `/fastfield-assignment-watch` | commands/fastfield-assignment-watch.md | Read-only | M365 Graph API (memory fallback works) |
| `/project-brief` | commands/project-brief.md | Read-only | Supabase connected + M365 for live signals |

**Partial workaround:** paste Teams/email content manually; use `/brief-me` or `/meeting-intake --paste`.

---

### Tier 4 — Blocked (requires additional setup)

| Command | File | Blocker |
|---------|------|---------|
| `/ask-openai-review` | commands/ask-openai-review.md | `OPENAI_API_KEY` + feedback_loop/ files present |

---

## Signal Sources

| Source | Role | Status | Notes |
|--------|------|--------|-------|
| Supabase | Canonical write target | Connected (read-only review mode) | Writes require Alejandro approval |
| Smartsheet | Schedule source | MCP re-auth pending | Read-only forever; never write |
| M365 / Outlook | Work email signals | OAuth pending | Work email: alejandroa@interworkoffice.com |
| Teams | Unread messages, mentions | OAuth pending | |
| Read AI | Meeting summaries | MCP auth pending | Works in Claude app; not yet in Claude Code CLI |
| FastField | Completion forms | No API | Manual / file intake only |
| Gmail | Personal only | Connected but wrong inbox | Do not use for work signals |
| Memory / RAG | Procedures and context | Healthy | 24+ files, BM25 + vector |

---

## Supabase Tables

| Table | Rows (approx.) | Notes |
|-------|---------------|-------|
| `projects` | ~580 | Canonical project records |
| `clients` | — | Client companies |
| `contacts` | — | All people |
| `vendors` | — | Vendor companies |
| `team_members` | — | InterWork staff |
| `project_vendors` | — | Project-vendor assignments |
| `open_loops` | — | Action item queue (added 2026-06-26) |
| `activity_log` | ~4 | Write audit trail |
| `fastfield_forms` | minimal | Completion signals not flowing yet |
| `communications` | 0 | Email/Teams not synced yet |
| `v_project_health` | view | Red/yellow/green health scoring (added 2026-06-26) |

---

## Known Data Quality Issues

| Issue | Impact | Fix |
|-------|--------|-----|
| 61 past-dated projects still marked `scheduled` | `v_project_health` false alerts | Status backfill — 6-project batch HELD for approval |
| `completion_report_sent` = 0% populated | Can't distinguish done vs. not done | WC report email parser built; needs M365 to run live |
| `v_project_health` proximity check triggers on past-dated projects | Noisy red alerts | SQL calibration fix pending |
| `fastfield_submitted` sparse | Only 11 true out of 580 | FastField webhook not yet active |
| `communications` table empty | No email/Teams data | Needs M365 Graph API OAuth |

---

## Integration Unlock Order

```
1. Env vars set (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY) ✅ Done
2. Supabase read-only confirmed ✅ Done 2026-06-28
3. 6-project batch status update → awaiting Alejandro approval
4. M365 OAuth → unlocks Teams + Outlook + WC report parser + FF assignment detection
5. Smartsheet MCP re-auth → schedule rows readable
6. Read AI MCP auth → meeting summary auto-ingest
7. FastField webhook test → before activating Make.com scenario 5506328
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/workstation_status.ps1` | Full workstation health check |
| `scripts/check_env_readiness.ps1` | Verify env vars are set |
| `scripts/rag_status.ps1` | RAG index status |
| `scripts/rag_reindex.ps1` | Rebuild RAG index |
| `scripts/rag_search.ps1 "query"` | Command-line RAG search |
| `scripts/ask_openai_review.py` | OpenAI Responses API bridge |
| `scripts/parse_completion_email.py` | WC report email parser |
