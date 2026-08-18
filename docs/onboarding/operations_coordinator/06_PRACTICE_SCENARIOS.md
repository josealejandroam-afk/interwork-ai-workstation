# Practice Scenarios
Used across Days 4–7 of `05_MODULE5_TRAINING_AGENDA.md`. Each type needs a **real, currently-live project** selected fresh — do not reuse the same project number across cohorts or weeks without checking it's still in the right state; project status changes daily. These are a different set of projects from the four fixed examples in Module 2 (`02_MODULE2_PROJECT_LIFECYCLE_AND_EXAMPLES.md`), which are static, sanitized case studies — these are live, current, and re-selected each time.

For each scenario, have Scott and Matt practice:
- Confirming the project number
- Finding the authoritative record (Supabase/dashboard first, then the project card)
- Checking client context and project history
- Identifying open loops
- Preparing an internal brief
- Drafting a client email
- Drafting a Teams dispatch
- Identifying what can safely be changed vs. what needs Alejandro's approval
- Escalating conflicts between sources instead of guessing

## Scenario 1 — Newly awarded project needing setup

**What it teaches:** starting a project from a quote, before anything else exists.

**How to pick a live example:** run `/dashboard-status` and look for a project recently added with `status = scheduled` and minimal confirmation flags set (`client_confirmed`, `vendor_confirmed`, `access_confirmed` all false or null). As of 2026-07-28, several TBD-dated projects flagged in `memory/company_knowledge/GLOBAL_OPEN_LOOPS.md` under "Scheduling — TBD-Dated Projects" fit this shape — re-verify their state before using, since these will likely have moved on by August 3.

**Exercise:** given only the project number, have them build the initial project card content: client, scope, dates (or "needs confirmation"), PM/vendor assignment status, and the pre-execution confirmation checklist from Module 2 with each item marked confirmed/open.

## Scenario 2 — Upcoming project with missing confirmations

**What it teaches:** the pre-execution confirmation loop and how to escalate a genuine conflict rather than resolve it themselves.

**How to pick a live example:** look for a project with an upcoming date but `client_confirmed`, `vendor_confirmed`, or `access_confirmed` still false, or with a noted open conflict in its `OPEN_LOOPS.md`. As of 2026-07-28, project 7549 (KV Indianapolis relocation) has a live example of exactly this — a crate-quantity conflict across sources that is explicitly flagged "do not resolve without Alejandro." Good example of what escalation looks like even if the specific numbers have since resolved — check current state first.

**Exercise:** have them identify every unconfirmed item, draft the client email and Teams dispatch that would go out once confirmed, and write out — in their own words — exactly what they'd say to Alejandro to escalate the open conflict, rather than picking a number themselves.

## Scenario 3 — Completed project needing closeout

**What it teaches:** the FastField → completion report → client communication → Supabase status sequence, and why status changes are held for approval even when the work is obviously done.

**How to pick a live example:** the held batch-completion approvals are a direct example of this — as of 2026-07-28, `memory/company_knowledge/GLOBAL_OPEN_LOOPS.md` lists a batch of projects with a proposed `status = completed` that is held pending Alejandro's explicit approval. Re-check `/completion-backlog` for the current held list, since the exact project numbers will change.

**Exercise:** have them draft the completion-acknowledgment client email, confirm what a work completion report needs to contain, and write the exact Supabase field changes they'd propose (`status`, `fastfield_submitted`, `completion_report_sent`, `actual_end_at`) without executing any of them — then explain why each one is held rather than auto-applied.

## A note on staleness

Every "as of 2026-07-28" reference above needs re-verification the day it's used — this doc describes *where to look and what shape to look for*, not a fixed list of project numbers to reuse indefinitely.
