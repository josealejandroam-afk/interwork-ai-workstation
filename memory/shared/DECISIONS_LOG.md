# Decisions Log
_Strategic and architectural decisions. Add an entry any time a non-obvious choice is made._
_Last updated: 2026-06-29_

---

| Date | Decision | Why | Approved By | Follow-up |
|------|----------|-----|-------------|-----------|
| 2026-06-26 | Build sequence: (1) clean backlog → (2) completion pipeline → (3) add signal sources | Don't add intake features before completion data is reliable | Alejandro (via ChatGPT review) | Status backfill in progress |
| 2026-06-26 | FastField parser priority order: WC report email → email text → pasted notes → folder → CSV | Most reliable signals first | Alejandro | WC parser built; needs M365 to run live |
| 2026-06-26 | Smartsheet = low/medium confidence; never alone justifies setting fastfield_submitted or completion_report_sent | Smartsheet lags and is often inaccurate | Alejandro | Enforced in all commands |
| 2026-06-26 | 7053 Strategic Education DC — hold until June 30 punchlist | Final punchlist still in scope | Alejandro | Revisit 2026-07-01 — punchlist due Jun 30 |
| 2026-06-26 | 7364 and 7447 — excluded from 6-project batch | Suspicious actual_end_at values | Alejandro | 7447 fix drafted; awaiting approval |
| 2026-06-26 | Use source='manual' in activity_log for Claude-initiated writes | No 'ai' enum value in the current schema | Alejandro | Update if enum is extended |
| 2026-06-26 | RLS not enabled on Supabase — hold until policies written | Enabling RLS with no policies blocks all access immediately | Alejandro | Policies not yet drafted |
| 2026-06-26 | GitHub repo = shared AI memory hub for Claude and ChatGPT | Built-in memory doesn't sync between AIs; repo is private, versioned, readable by both | Alejandro | memory/shared/ created 2026-06-29 |
| 2026-06-29 | Project count corrected to 140 | REST API Content-Range confirmed 0-139/140; prior ~580 was incorrect (likely Smartsheet estimate) | Claude (read-only verification) | Updated master context and handoff doc |
| 2026-06-29 | Aggressive execution mode set | Alejandro prefers action-first; stop only before sends/writes/production changes | Alejandro | Saved to session memory |
