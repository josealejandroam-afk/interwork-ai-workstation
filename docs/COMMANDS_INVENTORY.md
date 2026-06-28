# Commands Inventory

Generated: 2026-06-28
Source: `D:\ai-workstation\commands\`

---

## Summary

| Category | Count |
|----------|-------|
| Safe local only (no external deps) | 2 |
| Requires external integration | 12 |
| Mixed (local fallback + external preferred) | 3 |
| **Total** | **17** |

---

## Command Details

### Safe Local Only — Can Run Now

| Command | File | Purpose | Status |
|---------|------|---------|--------|
| `/rag-search` | `commands/rag-search.md` | Hybrid BM25+vector search of local memory index | **PATH NEEDS UPDATE** — references `C:\Users\1\.claude\rag\` — use helper script `scripts\rag_search.ps1` instead |
| `/rag-status` | `commands/rag-status.md` | Health check of local RAG index: chunk count, coverage, staleness | **PATH NEEDS UPDATE** — references `C:\Users\1\.claude\` and `C:\Users\1\` paths |

**Action:** Update both files to use `D:\ai-workstation\rag\` and `D:\ai-workstation\memory\`. Safe local edit.

---

### Read-Only Dashboard / Reporting — Requires Supabase

| Command | File | Purpose | When to Enable |
|---------|------|---------|---------------|
| `/dashboard-status` | `commands/dashboard-status.md` | Read-only Supabase query: project counts, attention items, upcoming jobs, checklist gaps | After `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` are set |
| `/project-health` | `commands/project-health.md` | Deep health scoring via `v_project_health` view; cross-refs open loops | After Supabase connected |
| `/completion-backlog` | `commands/completion-backlog.md` | Read-only: past-dated active projects grouped by evidence level | After Supabase connected |
| `/project-brief` | `commands/project-brief.md` | Full project brief from Supabase + memory/RAG + M365/Teams (layered) | Partial now (memory tier works); full after Supabase + M365 |

---

### Write-Proposed — Requires Supabase + Alejandro Approval

| Command | File | Purpose | When to Enable |
|---------|------|---------|---------------|
| `/completion-intake` | `commands/completion-intake.md` | Accept completion signals (FastField CSV, WC report, email), propose Supabase updates | After Supabase connected; writes require approval |
| `/ff-sent` | `commands/ff-sent.md` | Manual fallback: records FastField dispatched to PM, creates open loop | After Supabase connected (project lookup required) |
| `/fastfield-intake` | `commands/fastfield-intake.md` | Query `fastfield_webhook_events`, propose `fastfield_submitted = true` matches | After Supabase + Make webhook active |

---

### External Integration Required

| Command | File | Purpose | Integration Needed | When to Enable |
|---------|------|---------|-------------------|---------------|
| `/teams-brief` | `commands/teams-brief.md` | Summarize recent Teams messages, open questions, waiting items | M365 Graph OAuth | After M365 re-authorized |
| `/meeting-intake` | `commands/meeting-intake.md` | Deep intake for a single Read AI meeting; saves to memory, proposes open loops | Read AI MCP (Mode A) or manual paste (Mode B) | Mode B works now; Mode A after Read AI MCP connected |
| `/readai-brief` | `commands/readai-brief.md` | Pull recent meetings from Read AI, surface attention items | Read AI MCP (Mode A) or manual (Mode B) | Mode B works now; Mode A after Read AI MCP connected |
| `/brief-me` | `commands/brief-me.md` | Morning briefing from all sources: open loops, Teams, Outlook, Smartsheet | M365, Smartsheet, Gmail MCPs | Partial now (local open loops only); full after integrations |
| `/find-open-loops` | `commands/find-open-loops.md` | Scan `memory/open_loops/` and surface items by urgency | Local only (paths need D: update) | **PATH NEEDS UPDATE** — references `C:\Users\1\.claude\` |
| `/feedback-status` | `commands/feedback-status.md` | Read-only: check `feedback_loop/` file timestamps and action plan items | Local file read only | **PATH NEEDS UPDATE** — references `C:\Users\1\.claude\feedback_loop\` |
| `/ask-openai-review` | `commands/ask-openai-review.md` | Assemble review packet, send to OpenAI, save action plan | `OPENAI_API_KEY` env var + `feedback_loop/` files | After `OPENAI_API_KEY` set |
| `/fastfield-assignment-watch` | `commands/fastfield-assignment-watch.md` | Detect if FastField was dispatched to PM via Outlook/Teams/memory | M365 OAuth (preferred); memory fallback | Memory fallback works now; M365 after re-auth |

---

## Path Update Required

These command files still reference old laptop paths (`C:\Users\1\.claude\`, `C:\Users\1\scripts\`). They must be updated before use in Claude Code on this machine.

| File | Old Path Referenced | Correct D: Path |
|------|--------------------|--------------------|
| `commands/rag-search.md` | `C:\Users\1\.claude\rag\search.py` | `D:\ai-workstation\rag\search.py` |
| `commands/rag-search.md` | `C:\Users\1\.claude\rag\ingest.py` | `D:\ai-workstation\rag\ingest.py` |
| `commands/rag-status.md` | `C:\Users\1\.claude\rag\search.py` | `D:\ai-workstation\rag\search.py` |
| `commands/rag-status.md` | `C:\Users\1\.claude\projects\C--Users-1\memory\` | `D:\ai-workstation\memory\` |
| `commands/teams-brief.md` | `C:\Users\1\.claude\projects\C--Users-1\memory\open_loops\` | `D:\ai-workstation\memory\open_loops\` |
| `commands/teams-brief.md` | `C:\Users\1\AppData\Local\Temp\claude\teams-screenshots\` | `C:\Users\Owner\AppData\Local\Temp\claude\teams-screenshots\` |
| `commands/teams-brief.md` | `C:\Users\1\scripts\` | `D:\ai-workstation\scripts\` |
| `commands/brief-me.md` | `C:\Users\1\today.md` | `D:\ai-workstation\docs\today.md` or `C:\Users\Owner\today.md` |
| `commands/brief-me.md` | `C:\Users\1\.claude\projects\C--Users-1\memory\open_loops\` | `D:\ai-workstation\memory\open_loops\` |
| `commands/find-open-loops.md` | `C:\Users\1\.claude\projects\C--Users-1\memory\open_loops\` | `D:\ai-workstation\memory\open_loops\` |
| `commands/meeting-intake.md` | `C:\Users\1\.claude\rag\ingest.py` | `D:\ai-workstation\rag\ingest.py` |
| `commands/feedback-status.md` | `feedback_loop/to_chatgpt.md` (relative) | Needs `D:\ai-workstation\feedback_loop\` to exist |
| `commands/ask-openai-review.md` | `C:\Users\1\scripts\ask_openai_review.py` | `D:\ai-workstation\scripts\ask_openai_review.py` |
| `commands/ask-openai-review.md` | `C:\Users\1\.claude\rag\search.py` | `D:\ai-workstation\rag\search.py` |
| `commands/ask-openai-review.md` | `C:\Users\1\.claude\rag\ingest.py` | `D:\ai-workstation\rag\ingest.py` |
| `commands/completion-intake.md` | `C:\Users\1\scripts\parse_completion_email.py` | `D:\ai-workstation\scripts\parse_completion_email.py` |

---

## Do NOT Install into %USERPROFILE%\.claude Yet

The command files in `D:\ai-workstation\commands\` are the authoritative source. Do not copy them to `%USERPROFILE%\.claude\commands\` until:

1. All path references are updated to D: equivalents
2. The feedback_loop directory structure is confirmed on D:
3. Alejandro reviews and approves the update pass

Use the helper scripts in `D:\ai-workstation\scripts\` for RAG operations in the meantime.

---

## Recommended Update Order (when Alejandro returns)

1. `/rag-search` and `/rag-status` — path fix only, no external deps, safe to do now
2. `/find-open-loops` and `/brief-me` — local path fix, enables local morning workflow
3. `/feedback-status` and `/ask-openai-review` — after `OPENAI_API_KEY` is set
4. `/dashboard-status`, `/project-health`, `/completion-backlog` — after Supabase secrets set
5. `/teams-brief`, `/meeting-intake`, `/readai-brief` — after M365 + Read AI OAuth
6. `/completion-intake`, `/ff-sent`, `/fastfield-intake` — after all Supabase + Make active
