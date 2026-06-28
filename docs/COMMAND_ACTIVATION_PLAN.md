# Command Activation Plan

Generated: 2026-06-28 12:38

All 17 slash commands in D:\ai-workstation\commands\ audited.
Path fixes applied. Commands NOT yet installed to %USERPROFILE%.claude\commands.

## Activation Tiers

### Tier 1 -- Safe Now (local only, paths fixed)

| Command | File | Needs | Safe to Install |
|---------|------|-------|----------------|
| /rag-search | rag-search.md | D:\ai-workstation\rag (exists) | YES |
| /rag-status | rag-status.md | D:\ai-workstation\rag (exists) | YES |
| /find-open-loops | find-open-loops.md | D:\ai-workstation\memory (exists) | YES |
| /feedback-status | feedback-status.md | feedback_loop\ dir (needs creation) | After dir created |

### Tier 2 -- Safe with Local Fallback (some features offline)

| Command | File | Online Features | Offline Fallback |
|---------|------|----------------|-----------------|
| /meeting-intake | meeting-intake.md | Read AI MCP (Mode A) | Manual paste (Mode B) -- works now |
| /readai-brief | readai-brief.md | Read AI MCP (Mode A) | Manual input (Mode B) -- works now |
| /brief-me | brief-me.md | M365, Smartsheet, Gmail | Local open_loops only -- partial |
| /fastfield-assignment-watch | fastfield-assignment-watch.md | M365, Teams | Memory fallback -- works now |
| /project-brief | project-brief.md | Supabase, M365, Teams | Memory/RAG tier only -- partial |

### Tier 3 -- Blocked Until Supabase Connected

| Command | File | Requires |
|---------|------|---------|
| /dashboard-status | dashboard-status.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| /project-health | project-health.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| /completion-backlog | completion-backlog.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| /completion-intake | completion-intake.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| /ff-sent | ff-sent.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |
| /fastfield-intake | fastfield-intake.md | SUPABASE_URL + Make webhook active |

### Tier 4 -- Blocked Until External MCP/API Connected

| Command | File | Requires |
|---------|------|---------|
| /teams-brief | teams-brief.md | M365 OAuth re-authorization |
| /ask-openai-review | ask-openai-review.md | OPENAI_API_KEY + feedback_loop/ files |

## Installation Decision

Commands safe to install into %USERPROFILE%.claude\commands\ NOW:

- /rag-search (fully local, paths fixed)
- /rag-status (fully local, paths fixed)
- /find-open-loops (local memory read-only, paths fixed)

All others: hold until secrets set or integration connected.
Installing external-dependent commands now would silently fail and confuse the session.

## feedback_loop/ Directory

Several commands reference D:\ai-workstation\feedback_loop\
This directory does not exist on D: yet.
Alejandro should migrate feedback_loop/ content from C: archive when ready.
Do not create empty placeholder -- stale files would corrupt /ask-openai-review.
