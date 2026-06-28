# Today's Operations Brief
**Date:** 2026-06-28 (Sunday)
**Source:** Live Supabase read + local RAG
**Mode:** Read-only — no writes performed
**Dashboard:** https://interwork-command-center.vercel.app/

---

## A. Top 10 Projects Needing Attention

### 1. 🔴 7304 — Montebello Install Acoustic Panels + Chairs, West Berlin NJ
| | |
|--|--|
| Status | scheduled |
| Scheduled | **Jul 2 — 4 days from now** |
| PM assigned | **NO** |
| Vendor confirmed | No (possibly untracked) |
| FastField | Not submitted |
| **Main issue** | No PM with 4 days to go |
| **Why it matters** | If no PM by tomorrow, this project goes in without an owner on a tight timeline |
| **Next action** | Assign PM today or confirm existing assignment that isn't in the DB |
| **Contact** | Alejandro assigns directly or delegates |

---

### 2. 🔴 7494 — MMA Furniture Move, San Diego to Walnut Creek CA
| | |
|--|--|
| Status | scheduled |
| Scheduled | **Jul 6 — 8 days out** |
| PM assigned | **NO** |
| Vendor confirmed | No (possibly untracked) |
| **Main issue** | No PM. Cross-city furniture move with no owner |
| **Why it matters** | Vendor and logistics coordination needed before move day |
| **Next action** | Assign PM |
| **Contact** | Alejandro assigns |

---

### 3. 🔴 7546 — MMA Conference Room Table Replacement, Dallas TX
| | |
|--|--|
| Status | scheduled |
| Scheduled | **Jul 9 — 11 days out** |
| PM assigned | **NO** |
| Vendor confirmed | No (possibly untracked) |
| **Main issue** | No PM |
| **Next action** | Assign PM |
| **Contact** | Alejandro assigns |

---

### 4. 🟡 7364 — MMC Allentown Move & Workstation Setup Support
| | |
|--|--|
| Status | **scheduled** (anomalous — likely done) |
| Scheduled start | 2026-03-19 |
| Scheduled end | 2026-06-25 |
| **actual_end_at** | **2026-04-20 14:00 UTC — already recorded in DB** |
| FastField | Submitted |
| **Main issue** | Has an actual_end_at AND fastfield submitted, but status is still "scheduled" |
| **Why it matters** | This is the most ready-to-close project in the system. The DB already has an end date. Status flip needs only a quick Alejandro confirm — no PM outreach needed |
| **Next action** | Alejandro confirms: "Yes, Allentown was done Apr 20 — approve status → completed" |
| **Contact** | Alejandro only (no PM confirmation needed — data is already there) |

---

### 5. 🟠 7060 — MMC Dallas Walnut Hill to Galleria Relocation & Decommission
| | |
|--|--|
| Status | in_progress |
| Scheduled end | **2026-04-30 — 59 days ago** |
| actual_end_at | NULL |
| FastField | **Not submitted** |
| PM | Frank Barrett |
| **Main issue** | Largest stuck project. 4-phase multiphase. No post-Apr-3 DB activity. FastField missing. |
| **Why it matters** | If genuinely complete, it's the biggest cleanup win. If not, need to know why. |
| **Next action** | Send Teams/email to Frank Barrett (draft in PROJECT_STATUS_CONFIRMATION_DRAFTS.md) |
| **Contact** | Frank Barrett (PM) |

---

### 6. 🟠 7497 — Radian TierPoint Navy Yard Decom, Philadelphia PA
| | |
|--|--|
| Status | **pending_approval** |
| Scheduled | 2026-05-18 — 41 days ago |
| FastField | **Submitted** |
| PM | assigned |
| **Main issue** | FastField submitted on a project still in pending_approval — field work happened before formal approval was recorded |
| **Why it matters** | Either the approval was granted but never logged, or work was done without it. Either way it's an anomaly that needs resolution before this can be closed or invoiced. |
| **Next action** | Alejandro confirms: was this approved? Resolve the status — either approve it retroactively or flag it |
| **Contact** | Alejandro |

---

### 7. 🟡 7348 — Amtrust Cleveland (location: Princeton NJ)
| | |
|--|--|
| Status | in_progress |
| Scheduled | 2026-04-15 — 74 days ago |
| FastField | **Submitted** |
| PM | Pedro Martinez |
| **Main issue** | Likely done (FastField submitted, narrow scope), but name/location mismatch blocks closure |
| **Next action** | Send Teams message to Pedro Martinez (draft ready in PROJECT_STATUS_CONFIRMATION_DRAFTS.md) |
| **Contact** | Pedro Martinez |

---

### 8. 🟡 7381 / 7435 / 7440 — Three in-progress with FastField submitted
All three have `fastfield_submitted = true`, are 54–68 days past scheduled date, and have `actual_end_at = NULL`.

| # | Name | Scheduled | FastField | Days past |
|---|------|-----------|-----------|-----------|
| 7381 | Resintech Deliver Install Monitor Arms, Camden NJ | Apr 21 | ✅ | 68 |
| 7435 | MMA Colleague Relocation (Metairie LA) | Apr 23 | ✅ | 66 |
| 7440 | Rothman Move, King of Prussia PA | May 4–5 | ✅ | 54 |

**Main issue:** These are very likely complete. FastField is submitted on all three. Scope was narrow for 7381 and 7435; 7440 was a two-day move.
**Next action:** Alejandro confirms "yes these are done" → approve batch status write for all three.
**Contact:** Alejandro only — no PM outreach needed if he can confirm directly.

---

### 9. 🟡 7053 — Strategic Education, Washington DC
| | |
|--|--|
| Status | scheduled |
| Scheduled end | **2026-06-30 — yesterday** |
| FastField | Submitted |
| actual_end_at | NULL |
| **Main issue** | Scheduled end just passed, FastField submitted, still showing scheduled |
| **Next action** | Alejandro confirms if this is complete — likely a status backfill |
| **Contact** | Alejandro |

---

### 10. 🔴 7395 — Dallas Office Restack
| | |
|--|--|
| Status | pending_approval |
| Scheduled | 2026-04-11 — 78 days ago |
| PM assigned | **NO** |
| FastField | Not submitted |
| **Main issue** | Pending approval for 78 days with no PM and no field activity |
| **Why it matters** | Either it was cancelled/deferred and nobody updated the record, or it's genuinely stuck |
| **Next action** | Alejandro confirms: still alive or close it? |
| **Contact** | Alejandro |

---

## B. Do Today (max 7 actions)

These are practical things Alejandro can act on right now, in order of urgency:

1. **Assign PM to 7304 Montebello West Berlin NJ** — Jul 2, 4 days out. This is the most time-sensitive action. One call or message.

2. **Confirm 7364 Allentown is closed** — actual_end_at is already in the DB (Apr 20). Alejandro just needs to say "yes, approve the status flip to completed." Fastest win of the day.

3. **Confirm 7381, 7435, 7440 are done** — all have FastField submitted. If Alejandro can confirm these three from memory, approve a batch write. Three records cleaned up in one decision.

4. **Send the Frank Barrett message (7060)** — draft is in `docs/PROJECT_STATUS_CONFIRMATION_DRAFTS.md`. Copy, paste, send from Teams or Outlook.

5. **Send the Pedro Martinez message (7348)** — same file. Copy, paste, send.

6. **Resolve 7497 Radian TierPoint** — FastField submitted, still pending_approval. Alejandro either approves it retroactively or decides how to handle it. One decision.

7. **Assign PM to 7494 and 7546** — Jul 6 and Jul 9. Less urgent than 7304 but should be done today or tomorrow.

---

## C. Upcoming Next 14 Days (Jun 28 – Jul 12)

| Date | # | Project | PM | Vendor | Client | Verify |
|------|---|---------|-----|--------|--------|--------|
| **Jul 1** | 7189 | MMC Bermuda Inventory — Hoboken NJ | ✅ | ❌ (possibly untracked) | ❌ (possibly untracked) | Who is the field crew? Any access requirements? |
| **Jul 1** | 7510 | Pear Relocation — San Francisco CA | ✅ | ❌ (possibly untracked) | ❌ (possibly untracked) | Vendor confirmed? Client has access ready? |
| **Jul 2** | 7304 | Montebello Install Acoustic Panels + Chairs — West Berlin NJ | **❌ NO PM** | ❌ | ❌ | **Assign PM immediately** |
| **Jul 6** | 7494 | MMA Furniture Move — San Diego to Walnut Creek CA | **❌ NO PM** | ❌ | ❌ | **Assign PM** |
| **Jul 9** | 7546 | MMA Conference Room Table Replacement — Dallas TX | **❌ NO PM** | ❌ | ❌ | **Assign PM** |

Note: vendor/client confirmation fields are unreliable across the board (known backfill gap). "❌" means the field is false in the DB — it does not necessarily mean unconfirmed in reality.

---

## D. Stale / Stuck Projects

### Old in-progress (all past scheduled date, likely complete)
| # | Name | Scheduled | FastField | Days stale | Signal |
|---|------|-----------|-----------|------------|--------|
| 7060 | MMC Dallas Relocation | Apr 3–30 | ❌ | 59 past end | Needs PM confirm |
| 7348 | Amtrust Cleveland (Princeton NJ) | Apr 15 | ✅ | 74 | Likely done |
| 7381 | Resintech Camden NJ | Apr 21 | ✅ | 68 | Likely done |
| 7435 | MMA Colleague Relocation Metairie LA | Apr 23 | ✅ | 66 | Likely done |
| 7440 | Rothman Move King of Prussia PA | May 4–5 | ✅ | 54 | Likely done |

### Pending approval with field signals (anomalous)
| # | Name | Scheduled | FastField | Issue |
|---|------|-----------|-----------|-------|
| 7497 | Radian TierPoint Navy Yard Decom Philadelphia PA | May 18 | ✅ | Work done before approval logged |
| 7395 | Dallas Office Restack | Apr 11 | ❌ | 78 days, no PM, no activity — may be dead |

### Scheduled but likely complete (fastfield + actual_end or scheduled_end passed)
| # | Name | Scheduled end | FastField | actual_end_at | Action |
|---|------|--------------|-----------|---------------|--------|
| 7364 | MMC Allentown | Jun 25 | ✅ | **Apr 20 — in DB** | Easiest close — just needs approval |
| 7053 | Strategic Education DC | Jun 30 | ✅ | NULL | Alejandro confirm |
| 7391 | Premier Orthopedics Multi-Phase Newtown Square PA | Jun 30 | ✅ | NULL | Alejandro confirm |
| 7352 | Goldberg Segalla Phase 1 Decom White Plains NY | May 4–6 | ✅ | NULL | Alejandro confirm |

---

## E. Completion / FastField Gaps

### The pattern: FastField submitted, completion_report_sent = false, invoiced = false
This applies to **57 projects** total. The `completion_report_sent` field has never been set to `true` in the entire database — the field appears untracked from the start.

Most recent completed projects with this gap (highest billing priority):

| # | Name | Scheduled | Invoiced |
|---|------|-----------|---------|
| 7472 | MMA Walkthrough + Colleague Relocation Dallas TX | May 15 | ❌ |
| 7482 | Amtrust Furniture Delivery & Install Jersey City NJ | May 15 | ❌ |
| 7347 | MMA Colleague Relocation McLean VA | May 13 | ❌ |
| 7499 | MMC Hoboken to Huddle Room King of Prussia PA | May 8 | ❌ |
| 7498 | MMC Furniture from 1166 Hoboken NJ | May 8 | ❌ |
| 7374 | Ingersoll Rand Internal Move Buffalo NY | May 4 | ❌ |
| 7479 | UiPath Service Call New York NY | May 1 | ❌ |
| 7403 | UiPath Paint Scope New York NY | May 1 | ❌ |
| 7297 | UGI Deliver Install Furniture King of Prussia PA | May 1 | ❌ |

**Root cause:** FastField forms are not yet syncing to Supabase (`fastfield_forms` table has only 1 row). Completion pipeline (Make.com scenario 5506328) not yet activated. The `completion_report_sent` field has never been populated.

**What this means for today:** The invoiced=false flags across completed projects are likely real billing exposure, not just data gaps. These should be reviewed for outstanding invoices.

---

## F. Ready-to-Send Messages

Copy and paste directly into Teams. Do not send from here.

---

**Message 1 — PM assignment for 7304 (send to whoever assigns PMs)**
```
7304 Montebello — West Berlin NJ — July 2

This project has no PM assigned and is 4 days out. Acoustic panels + chairs install.
Can someone confirm who's handling this or get it assigned today?
```

---

**Message 2 — Frank Barrett re: 7060 MMC Dallas**
```
Hey Frank — quick check on project 7060 (MMC Dallas, Walnut Hill → Galleria).

Our system still shows it as in-progress from Apr 3 with nothing logged after that.
Can you confirm:
1. Did Phases 2–4 run as planned through Apr 30?
2. Was a FastField submitted? If so, under what entry?
3. Any admin items still open — report, invoice, outstanding threads?

No rush on reply, just need it before I can update the record.
```

---

**Message 3 — Pedro Martinez re: 7348 Amtrust**
```
Hey Pedro — records check on project 7348, Amtrust, Apr 15.

DB has it as "Amtrust Cleveland" but the address is Princeton NJ — can you confirm?
Also FastField shows submitted. Is the Apr 15 job fully closed?

Need:
1. Princeton NJ confirmed (or correct location)
2. FastField submission reference if you have it
3. Actual close date — Apr 15 or 16?
4. Anything still open?
```

---

**Message 4 — Self-check (Alejandro's internal note) re: 7364 Allentown**
```
7364 MMC Allentown — the DB already has actual_end_at = Apr 20 and FastField submitted.
Status is still "scheduled." This just needs my confirmation to close.

If I confirm this is done → tell Claude "7364 Allentown is complete, approve status flip."
This is the fastest cleanup win available.
```

---

**Message 5 — Alejandro to self re: 7381, 7435, 7440 batch**
```
Three in-progress projects all have FastField submitted and are 54–68 days past date:
- 7381 Resintech Camden NJ (Apr 21)
- 7435 MMA Colleague Relocation Metairie LA (Apr 23)
- 7440 Rothman Move King of Prussia PA (May 4–5)

If I know these are done, I can approve a batch write to close all three.
Tell Claude: "7381, 7435, 7440 are complete — approve batch status write."
```

---

## G. Dashboard Data Corrections Needed

### Safe to discuss now (no write needed)
- `completion_report_sent` is never populated — this is a pipeline gap, not a data error
- `client_confirmed` is false across nearly all projects — known backfill gap, not real operational signal
- `fastfield_forms` table has only 1 row — Make.com pipeline not yet feeding it

### Needs confirmation before any action
- **7364 Allentown**: status=scheduled but actual_end_at recorded. Needs Alejandro to confirm it's done.
- **7053 Strategic Education DC**: scheduled_end passed yesterday. FastField submitted. Status still scheduled.
- **7391 Premier Orthopedics**: scheduled_end passed yesterday. FastField submitted. Status still scheduled.
- **7497 Radian TierPoint**: pending_approval + FastField submitted — needs Alejandro to resolve approval status.
- **7395 Dallas Office Restack**: pending_approval for 78 days, no PM, no activity — alive or dead?

### Requires full approval process before any database write
See `docs/APPROVAL_CHECKLIST_PROJECT_STATUS_WRITES.md` for the complete procedure.

| Project | What would change | Who must confirm |
|---------|-------------------|-----------------|
| 7364 | status → completed | Alejandro only (actual_end already in DB) |
| 7060 | status → completed, actual_end_at | Frank Barrett + Alejandro |
| 7348 | status → completed, actual_end_at | Pedro Martinez + Alejandro |
| 7381 | status → completed | Alejandro confirm (FastField submitted) |
| 7435 | status → completed | Alejandro confirm (FastField submitted) |
| 7440 | status → completed | Alejandro confirm (FastField submitted) |
| 7497 | status → resolve pending_approval | Alejandro |
| 7053, 7391 | status → completed | Alejandro confirm |

---

*Brief generated 2026-06-28. All data read-only from Supabase. No writes performed.*
