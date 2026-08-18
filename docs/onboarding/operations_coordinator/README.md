# Operations Coordinator Onboarding — Scott & Matt

Start date: Monday, August 3, 2026.

This package trains two new Operations Coordinators (same role as Alejandro Acosta) on InterWork's business and operations first, then the systems and AI tools that support the work. Access is staged — nobody gets everything on day one — and it ends with an individual competency signoff that determines what comes next.

**Company and process come before any system.** Modules 1–2 are deliberately AI-free, dashboard-free, and repo-free — Scott and Matt learn what InterWork does and how work actually moves before any tool is introduced to help with it.

**Francisco Vinueza is the direct manager for Alejandro, Scott, and Matt**, and the primary escalation point for field issues, unresolved operational problems, and project guidance. This is introduced explicitly on Day 1 (Module 1) — see `00_MANAGER_PREP_CHECKLIST.md`.

**Approval authority during this onboarding is not yet decided.** Every send (email, Teams) and every live-system write (Supabase, dashboard) routes through Alejandro Acosta for both Scott and Matt, with no exception, through at least Day 10. The Day 10 competency review (files 08) is the explicit point where Alejandro decides, per person, whether to extend any independent authority. Nothing in this package assumes an answer ahead of that review — see `ACCESS_AND_SAFETY_RULES.md` and `AGENT_PERMISSIONS.md` in `memory/company_knowledge/` and `docs/` for the current company-wide rules, which this package does not modify.

## Modules

| Module | File | Covers | AI/systems introduced? |
|---|---|---|---|
| 1 | [`01_MODULE1_INTERWORK_FUNDAMENTALS.md`](01_MODULE1_INTERWORK_FUNDAMENTALS.md) | What InterWork does, project types/terminology, internal roles, what good coordination looks like | No |
| 2 | [`02_MODULE2_PROJECT_LIFECYCLE_AND_EXAMPLES.md`](02_MODULE2_PROJECT_LIFECYCLE_AND_EXAMPLES.md) | Full quote-to-closeout lifecycle, where info originates, client vs. internal comms, four sanitized real project examples | No |
| 3 | [`03_MODULE3_SYSTEMS_AND_SOURCES_OF_TRUTH.md`](03_MODULE3_SYSTEMS_AND_SOURCES_OF_TRUTH.md) | QuickQuo, Smartsheet, Supabase, Command Center dashboard, FastField — as human-operated tools | First login, no AI |
| 4 | [`04_MODULE4_AI_AND_SHARED_KNOWLEDGE.md`](04_MODULE4_AI_AND_SHARED_KNOWLEDGE.md) | The GitHub repo as shared memory, Claude Code vs. Claude Chat, repo navigation, AI approval rules, current connector status | Yes |
| 5 | [`05_MODULE5_TRAINING_AGENDA.md`](05_MODULE5_TRAINING_AGENDA.md) | Day-by-day schedule tying modules to the ten-day onboarding, guided practice, reverse shadowing, controlled ownership | Practice, all tools |

## Delivery in practice

The repo is public on GitHub, so Scott and Matt can open any file above directly via its `github.com` link with no account and no waiting on access provisioning — that's the live-walkthrough path for Day 1 onward. For Days 1–2 specifically (screen-light, company-and-process-only), there's also a print-ready leave-behind covering Modules 1–2 end to end: [`handouts/Modules_1-2_InterWork_Fundamentals_Handout.pdf`](handouts/Modules_1-2_InterWork_Fundamentals_Handout.pdf). Walk through it together rather than assigning it as solo reading, and use it as their take-home reference afterward.

## Supporting files

| # | File | Purpose |
|---|---|---|
| 00 | [`00_MANAGER_PREP_CHECKLIST.md`](00_MANAGER_PREP_CHECKLIST.md) | What Alejandro does before Monday |
| 06 | [`06_PRACTICE_SCENARIOS.md`](06_PRACTICE_SCENARIOS.md) | Three live-project scenario types used in Module 5's hands-on days |
| 07 | [`07_ACCESS_CHECKLIST_SCOTT.md`](07_ACCESS_CHECKLIST_SCOTT.md) / [`_MATT.md`](07_ACCESS_CHECKLIST_MATT.md) | Individual staged-access trackers |
| 08 | [`08_COMPETENCY_SIGNOFF_SCOTT.md`](08_COMPETENCY_SIGNOFF_SCOTT.md) / [`_MATT.md`](08_COMPETENCY_SIGNOFF_MATT.md) | Individual Day 10 signoff sheets, including the approval-authority decision |

## Knowledge checks

Module 1 and Module 2 each end with a short knowledge check (in-file) — talk through answers with Alejandro before moving on. Modules 3 and 4 end with a single reflection question instead of a formal check; the real test there is Module 5's guided practice.

## Known documentation issues found while building this package

See "Outdated / conflicting documentation found" at the bottom of `00_MANAGER_PREP_CHECKLIST.md` — several existing docs (README.md, FIRST_DAY_RUNBOOK.md, EXTERNAL_INTEGRATION_GATES.md) still reference the old `D:\ai-workstation` location and a since-superseded "M365 reauth pending" status. Fix before handing anything to Scott or Matt, or they will follow stale instructions on day one.
