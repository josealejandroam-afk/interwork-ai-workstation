# Manager Prep Checklist — Before Monday, August 3

For: Alejandro Acosta. Complete before Scott and Matt's first session.

## 1. Fix stale documentation first

Do not hand Scott or Matt anything until this is done — several onboarding-adjacent docs currently point at the wrong drive and an outdated integration status. See "Outdated / conflicting documentation found" below for the specific files and fixes.

## 2. Accounts and credentials

- [ ] Confirm IT/company process for provisioning Scott's and Matt's individual accounts: email, Teams, QuickQuo, Smartsheet, FastField, GitHub, Supabase dashboard (read-only), Vercel viewer (if applicable)
- [ ] Do **not** share your own passwords, API keys, `.env` file, or Supabase service-role key with either of them — each gets their own credentials
- [ ] Decide whether Scott and Matt get individual GitHub accounts with read access to `josealejandroam-afk/interwork-ai-workstation`, or view access via raw URL only (no git operations) for week 1 — recommended: raw-URL/read-only for week 1, real GitHub read access once they've done the repo-navigation exercise in Module 4 (Day 3)
- [ ] Confirm who at InterWork (you, Francisco, or IT) actually creates these accounts — this package assumes you coordinate but doesn't automate account creation

## 3. Pick real material for training

- [ ] Before Day 3's guided system tour (Module 4), run `/dashboard-status` or `/project-health` and pick one **completed** project with a clean, resolved history — avoid anything with open disputes (e.g. the crate-quantity conflict on 7549, or 7347's AV recovery) since those add noise to a first-pass tour
- [ ] Before Days 4–5, pick live projects matching Scenarios 1 and 2 in `06_PRACTICE_SCENARIOS.md` — re-verify against current `/project-health` output the morning of, since project status changes daily and any list made now will be stale by August 3
- [ ] Before Days 6–7 (reverse shadowing), set aside 4–6 small, low-risk real projects — no active client escalations, no held Supabase batch approvals — for Scott and Matt to work independently under your review

## 4. Set expectations up front (say this to both, together, Day 1 morning)

- **Introduce Francisco Vinueza explicitly as direct manager for all three of you — Alejandro, Scott, and Matt — and as the primary escalation point for field issues, unresolved operational problems, and project guidance.** State this clearly on Day 1; don't leave it implicit or let it surface later as a surprise. This is a reporting-line fact, separate from and on top of the approval-authority point below.
- Alejandro is the sole approval authority for sends and live-system writes during onboarding — this is not a trust judgment, it's the current company-wide rule for everyone, and it applies during onboarding regardless of how it evolves after
- Whether that changes after the Day 10 competency review is not decided yet — don't let them treat Week 1 behavior as a guarantee either way
- Evaluate them individually — training together does not mean grading together (see `08_COMPETENCY_SIGNOFF_SCOTT.md` / `_MATT.md`)
- Draft freely, always; send/write nothing without your explicit go-ahead
- **Days 1–2 are company and process only — no AI tools, dashboard, or repo.** They need to understand InterWork before any system is introduced to help with it. If either of them wants to jump ahead to "the AI stuff," that's a sign Modules 1–2 need reinforcing, not a sign they're ready to skip forward.

## 5. Logistics

- [ ] Block your own calendar for Days 1–5 (heaviest hands-on time) and lighter check-in blocks Days 6–10
- [ ] Confirm Scott and Matt each have a workstation/laptop provisioned before Monday
- [ ] Decide where they'll sit relative to you for Week 1 shadowing

---

## Outdated / conflicting documentation found

Found while assembling this package — fix before onboarding, since Scott and Matt will read these paths literally.

| File | Issue | Fix |
|---|---|---|
| `README.md` (repo root) | Says repo lives at `D:\ai-workstation`; references a `C:\Users\Owner\.claude` archive "do not delete yet"; dated 2026-06-28 | Repo is actually at `C:\Users\AlejandroAcosta\Documents\ai-workstation` now (confirmed via `git remote`/cwd). Needs a full rewrite of the location and status section — this is the single most misleading file for a new hire since it's the first thing anyone opens. |
| `docs\FIRST_DAY_RUNBOOK.md` | Every script path uses `D:\ai-workstation\scripts\...`; step 2 checks `C:\Users\Owner\.claude` | Same stale-drive issue as README. This doc is written for you personally post-migration, not for new hires — do not use it as onboarding material as-is. |
| `docs\EXTERNAL_INTEGRATION_GATES.md` | Says M365/Teams/Smartsheet are "NOT connected — OAuth not yet reauthorized," implying reconnection is just a pending step | This is now superseded: `memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md` and `memory/company_knowledge/GLOBAL_OPEN_LOOPS.md` (both later, confirmed 2026-06-30) state M365/Teams/Graph are **blocked by company tenant policy**, not just unreauthorized — it requires IT (Christian) or Gal to approve a sanctioned path, and Claude is told not to retry or pressure. Anyone reading only `EXTERNAL_INTEGRATION_GATES.md` would think this is a quick reconnect. `04_MODULE4_AI_AND_SHARED_KNOWLEDGE.md` in this package uses the corrected (blocked) status — reconcile the source doc when you have time. |
| ~50 other files (scripts, docs) | Still reference `D:\ai-workstation` | Not fixed here — out of scope for this package. Worth a cleanup pass later; `grep -r "D:\\\\ai-workstation"` from the repo root finds them all. |

None of this blocks Monday — Modules 3 and 4 in this package already use the corrected path and status so Scott and Matt aren't misled. But README.md and FIRST_DAY_RUNBOOK.md should get fixed soon since they'll come up in any general repo browsing.
