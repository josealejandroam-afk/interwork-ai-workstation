---
name: ""
metadata: 
  node_type: memory
  id: manual-20260626-backfill
  source: manual
  person: Alejandro
  status: action-needed
  priority: high
  created: 2026-06-26T00:00
  updated: 2026-06-26T00:00
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# Confirmation Backfill Review — 2026-06-26

Generated after first `/project-health` run. 38 red / 9 yellow / 0 green.
Distribution reflects unbackfilled confirmation fields, not actual project risk.
**Do not update any fields without Alejandro approval.**

---

## Context

- `v_project_health` queries `status NOT IN (completed, closed, cancelled)`
- 39 of 47 flagged projects are `scheduled` but past their `scheduled_date` — likely completed, status never updated
- `communications` table is empty — no email evidence available
- Only in-database completion signal: `fastfield_submitted = true`

---

## Group A — High Confidence: Likely Completed (fastfield_submitted = true)

These projects are past their scheduled date, still `status = scheduled`, but
FastField was submitted — strong signal the work was physically done.

**Proposed action: `status → completed` (requires Alejandro approval per project)**

| # | Project | Scheduled | Days Past | Other Signals |
|---|---------|-----------|-----------|---------------|
| 7053 | Strategic Education Washington DC | 2026-03-21 | 97 | fastfield ✅ client_confirmed ✅ |
| 7364 | MMC Allentown Move & Workstation Setup | 2026-03-19 | 99 | fastfield ✅ access_confirmed ✅ |
| 7391 | Premier Orthopedics Multi-Phase Newtown Square PA | 2026-04-24 | 63 | fastfield ✅ — multi-phase, confirm scope done |
| 7374 | Ingersoll Rand Internal Move Buffalo NY | 2026-05-04 | 53 | fastfield ✅ |
| 7352 | Goldberg Segalla Phase 1 Decom White Plains NY | 2026-05-04 | 53 | fastfield ✅ |
| 7499 | MMC Hoboken to Huddle Room King of Prussia PA | 2026-05-08 | 49 | fastfield ✅ access_confirmed ✅ |
| 7498 | MMC Furniture from 1166 Hoboken NJ | 2026-05-08 | 49 | fastfield ✅ |
| 7347 | MMA Colleague Relocation McLean VA | 2026-05-13 | 44 | fastfield ✅ access_confirmed ✅ |
| 7482 | Amtrust Furniture Delivery & Installation Jersey City NJ | 2026-05-15 | 42 | fastfield ✅ access_confirmed ✅ |
| 7472 | MMA Walkthrough Addison TX + Colleague Relocation Dallas TX | 2026-05-15 | 42 | fastfield ✅ access_confirmed ✅ |
| 7447 | MMA Tech Install Move Clearwater Tampa FL | 2026-06-16 | 10 | fastfield ✅ |

---

## Group B — Walkthroughs / Scoping (No Fastfield Expected)

These project types typically don't produce a FastField submission.
Past their dates with no completion signals — may be complete or may be genuinely open.

**Action: Human review required — was work completed?**

| # | Project | Scheduled | Days Past |
|---|---------|-----------|-----------|
| 7431 | MMC Walkthrough for Internal Move | 2026-04-13 | 74 |
| 7490 | Fox Decom Walkthrough | 2026-05-04 | 53 |
| 7500 | Warfel Construction Walkthrough White Marsh MD | 2026-05-06 | 51 |
| 7504 | Premier Workspaces Walkthrough NYC | 2026-05-11 | 46 |

---

## Group C — Past-Dated Scheduled, No Completion Signals

Past their dates with `fastfield_submitted = false`, `completion_report_sent = false`,
`invoiced = false`. May be complete (just never tracked) or may still be in process.

**Action: Human review required — sorted by recency (most recent = most likely still open)**

| # | Project | Scheduled | Days Past | Notes |
|---|---------|-----------|-----------|-------|
| 7569 | MMC Service Call Birmingham AL | 2026-06-25 | 1 | Very recent — likely just happened |
| 7556 | MMA Art Work Hanging Dallas TX | 2026-06-24 | 2 | Recent |
| 7572 | Amtrust Move 40-50 Boxes New York NY | 2026-06-24 | 2 | Recent |
| 7565 | Vecos Lockers Philadelphia PA | 2026-06-23 | 3 | Recent |
| 7538 | MMA Office Cleanout Decom Clayton MO | 2026-06-22 | 4 | Recent |
| 7552 | Dropbox Phase 3 San Francisco CA | 2026-06-22 | 4 | Recent |
| 7561 | Reckitt Walkthrough Minneapolis MN | 2026-06-22 | 4 | Recent |
| 7486 | MMA Austin TX | 2026-06-04 | 22 | Open loop 7492 is nearby — check both |
| 7492 | Radian Decom Denver CO | 2026-06-04 | 22 | Open loop teams-20260701-001 (John Smith) |
| 7378 | MMA Phase 2 Decom Van Nuys CA | 2026-06-01 | 25 | |
| 7471 | MMA Decom + Move Loveland OH | 2026-06-10 | 16 | |
| 7529 | Monster Energy Furniture RDI Mount Pocono PA | 2026-06-15 | 11 | |
| 6853 | Claritev Internal Move De Pere WI | 2026-06-16 | 10 | |
| 7437 | CRC Decom Internal Move Virginia Beach VA | 2026-05-15 | 42 | |
| 7450 | Bentley Systems Framingham to Exton Relocation & Decom | 2026-05-25 | 32 | |
| 7495 | MMA Move/Light Decom Charlotte NC | 2026-05-27 | 30 | |
| 7515 | Amtrust Storage Disposal New York NY | 2026-05-27 | 30 | |
| 7513 | Amtrust Move Office Furniture Southington CT | 2026-05-21 | 36 | |
| 7399 | Dropbox Asset Relocation San Francisco CA | 2026-05-22 | 35 | |
| 7341 | Guardian Decom Newport Beach CA | 2026-05-18 | 39 | |
| 7502 | Amtrust Small Office Move Garden Grove CA | 2026-05-11 | 46 | |
| 7474 | The Team Decal Install New York NY | 2026-05-08 | 49 | |
| 7425 | UPenn Delivery Install Round Table Philadelphia PA | 2026-05-07 | 50 | |
| 7191 | MMA Punch List Cape May NJ | 2026-05-07 | 50 | |
| 7516 | UiPath Service Call Dallas TX | 2026-05-15 | 42 | vendor_confirmed ✅ access_confirmed ✅ |
| 7407 | MMC Install Service Call Phoenix AZ | 2026-05-15 | 42 | vendor_confirmed ✅ access_confirmed ✅ |
| 7354 | MMA Retrieve Tech for Shipment Alpharetta GA | 2026-05-15 | 42 | vendor_confirmed ✅ access_confirmed ✅ |
| 7322 | Goldberg Segalla May 5 | 2026-05-05 | 52 | vendor_confirmed ✅ access_confirmed ✅ |
| 7454 | Vecos Commissioning Tallahassee FL | 2026-04-16 | 71 | |
| 7467 | Dropbox Seattle Studio Move | 2026-04-27 | 60 | |
| 7434 | MMA Paint Scope / Furniture Decom | 2026-04-07 | 80 | |
| 7350 | Bentley Systems Furniture Move/Disposal Exton PA | 2026-05-04 | 53 | |

---

## Group D — Missing PM Assigned (pm_assigned = false)

### Future-scheduled (genuine gap — needs PM before project date):
| # | Project | Scheduled | Days Until |
|---|---------|-----------|-----------|
| 7304 | Montebello Install Acoustic Panels West Berlin NJ | 2026-07-02 | +6 |
| 7494 | MMA Furniture Move San Diego to Walnut Creek CA | 2026-07-06 | +10 |
| 7546 | MMA Conference Room Table Replacement Dallas TX | 2026-07-09 | +13 |

### Past-dated (may already be handled or part of status cleanup):
| # | Project | Scheduled | Status |
|---|---------|-----------|--------|
| 7395 | Dallas Office Restack | 2026-04-11 | pending_approval |
| 7370 | MMA Decom + Whiteboard Install Bend OR | 2026-04-30 | scheduled |
| 7418 | MMA Colleague Relocation + Decom Columbia MD | 2026-05-20 | scheduled |
| 7512 | Togetherwork Kesef Accounting Office Decom Montvale NJ | 2026-05-28 | scheduled |
| 7537 | CRC Walkthrough Client Checkin Tampa FL | 2026-06-18 | scheduled |

---

## Group E — Genuine Reds (in_progress + overdue)

These are not false alerts. Work started, past scheduled date, no completion report.

| # | Project | Scheduled | Days Overdue | Score | Top Risk |
|---|---------|-----------|-------------|-------|----------|
| 7060 | MMC Dallas - Walnut Hill to Galleria Relocation & Decom | 2026-04-03 | 84 | 30 | overdue_in_progress |
| 7348 | Amtrust Cleveland | 2026-04-15 | 72 | 50 | overdue_in_progress |
| 7381 | Resintech Deliver Install Monitor Arms Camden NJ | 2026-04-21 | 66 | 25 | overdue_in_progress |
| 7435 | MMA Colleague Relocation | 2026-04-23 | 64 | 25 | overdue_in_progress |
| 7440 | Rothman Move King of Prussia PA | 2026-05-04 | 53 | 50 | overdue_in_progress |

**These need completion reports and/or status updates. No data-quality defense here.**

---

## No Evidence Found

All flagged projects lack communications data (table is empty for all active projects).
No email or Teams messages available to auto-detect confirmations.
Backfill must come from Alejandro's direct knowledge or manual review.
