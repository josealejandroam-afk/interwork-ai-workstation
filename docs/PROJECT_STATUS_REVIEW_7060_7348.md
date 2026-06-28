# Project Status Review — Human Review Packet
**Projects:** 7060 (MMC Dallas Relocation) | 7348 (Amtrust Cleveland)  
**Date:** 2026-06-28  
**Mode:** Read-only — no writes performed  
**Purpose:** Provide Alejandro with enough context to decide whether either project should be moved from `in_progress` to `completed` (or another status) in a future approved write session.  
**Source:** Supabase read-only queries + local memory/RAG index

---

## Project 7060 — MMC Dallas Walnut Hill to Galleria Relocation & Decommission

### 1. Identification
| Field | Value |
|-------|-------|
| Project number | 7060 |
| Project name | MMC Dallas - Walnut Hill to Galleria Relocation & Decommission |
| Type | Installation (multiphase) |
| Current Supabase status | `in_progress` |

### 2. Dates
| Field | Value |
|-------|-------|
| Scheduled start | 2026-04-03 (Phase 0 / partial IT move) |
| Scheduled end | **2026-04-30** (Phase 4 final punch/closeout) |
| Actual start | 2026-04-03 09:00 UTC (recorded) |
| Actual end | **NULL — never recorded** |
| Days past scheduled end (today 2026-06-28) | **59 days** |
| DB record last updated | **2026-04-03** — no updates since Phase 0 launch day |

### 3. Assignment & Contacts
| Field | Value |
|-------|-------|
| PM | Frank Barrett (pm_id linked, pm_assigned = true) |
| Client POC | Jane Bae — Sr PM, Lincoln Property Company (LPC) — contact via Outlook/Teams |
| On-site POC | Brent Lee — Marsh MMA — contact via Outlook/Teams (phone discrepancy noted; separate records task) |
| Vendor | Exserv Facility Services |
| Vendor lead | Sergio Rios — Exserv — contact details in Supabase `internal_notes` |
| IT sourcing contact | Dwyane Bailey — Marsh — contact details in Supabase `internal_notes` |

### 4. Confirmation Fields
| Field | Value | Reliability |
|-------|-------|-------------|
| vendor_confirmed | true | Likely legitimate — Sergio Rios/Exserv confirmed in scope detail |
| client_confirmed | false | **Possibly unbackfilled** — Jane Bae was actively engaged; false may reflect missing backfill |
| access_confirmed | false | **Possibly unbackfilled** — access details are extensively documented in notes |
| client_informed | true | Recorded in DB |

### 5. Completion Signals
| Field | Value |
|-------|-------|
| fastfield_submitted | **false** |
| completion_report_sent | false |
| invoiced | false |

### 6. Scope & Phase Detail (from DB internal_notes and scope_detail)
Four-phase multiphase project:

| Phase | Date | Description | DB Status |
|-------|------|-------------|-----------|
| Phase 0 | Apr 3 | Partial IT move — 10 employees to Galleria | Completed (noted) |
| Phase 1 | Apr 6 | IT disconnect/transport Walnut Hill → Galleria | **COMPLETED** (explicitly noted) |
| Phase 2 | Apr 7–9 | IT install at Galleria Floors 11–14 | **IN PROGRESS** (last known state as of Apr 3) |
| Pre-decom walkthrough | Apr 10 | Frank Barrett + Jane Bae at Walnut Hill | Scheduled as of Apr 3 |
| Phase 3 | Apr 11–29 | Walnut Hill Floors 15–18 decommission | Upcoming as of Apr 3 |
| Phase 4 | Apr 30 | Final punch/closeout | Upcoming as of Apr 3 |

**Critical detail:** The DB record was last updated on **Apr 3** — the day Phase 0 occurred. All subsequent phases (Phase 2 install, Phase 3 decom, Phase 4 closeout) have **no DB updates**. The Apr 30 scheduled_end_date passed 59 days ago with no `actual_end_at` recorded and no FastField submission.

**Outstanding items as of Apr 3 (last known state):**
- Remaining monitors, docking stations, power strips at Galleria (755 monitors, 293 docking stations, 151 power strips across Floors 11–14)
- Docking station delivery — critical path (Dwyane Bailey sourcing)
- UPS at Walnut Hill requiring separation (after Apr 11)
- Finance Group move date — TBD as of Apr 3
- Monitor arm missing component (Kyle Bass at Business Interiors)
- Brent Lee phone number discrepancy — 469-383-6012 vs. 972-342-2190

### 7. Local Memory / RAG References
No dedicated memory file found for project 7060 in the RAG index. Context is drawn entirely from the Supabase `internal_notes` and `scope_detail` fields, which contain a detailed ChatGPT-extracted project log dated Apr 3, 2026.

### 8. Communications Rows
**0 rows** — `communications` table is empty (no M365 pipeline active yet).

### 9. Checklist Rows
**0 rows** — no checklist items linked to this project.

### 10. FastField Forms
**0 rows** — no FastField submission on record for this project.

### 11. Why It Appears Stuck
- DB last updated Apr 3 (Phase 0 day). No subsequent updates across a 4-phase, 27-day project.
- `actual_end_at` is NULL despite scheduled end of Apr 30 having passed 59 days ago.
- `fastfield_submitted = false` — unusual for a project of this scale if truly complete.
- No completion report, no invoice recorded.
- All four phases after Phase 0 have no confirmation of execution in the DB.

### 12. Evidence FOR Closing (candidate for completed)
- Scheduled end date was Apr 30 — 59 days ago. A project of this scope would not normally still be "in progress" 2 months later.
- Phase 0 and Phase 1 are explicitly marked COMPLETED in the scope notes.
- The `ai_summary` describes Phase 4 (final punch Apr 30) as a scheduled endpoint, implying the project was designed to close by then.
- If Exserv/Frank Barrett executed Phases 2–4 as planned, the project is almost certainly complete.
- MMA / Marsh MMA (client) would have moved into Galleria long ago — the building effective date was Apr 13.

### 13. Evidence AGAINST Closing (reasons to be cautious)
- `fastfield_submitted = false` — this is the strongest counter-signal. If field work was completed, a FastField form would normally have been submitted.
- Outstanding items were documented as of Apr 3: docking stations on critical path, Finance Group move date TBD. If these were never resolved, the project may have partial open threads.
- No actual_end_at, no invoice, no completion report — triple absence suggests either genuine incompletion or a significant DB backfill gap.
- The DB has not been touched since Apr 3 — it's possible the project stalled or scope changed after that date and was never updated.

### 14. Recommended Action
**Needs email/PM verification** — Do not close without Frank Barrett or Alejandro confirming that Phases 2–4 were executed. If confirmed complete, this becomes a strong candidate for `completed` with `actual_end_at` backfill.

**Minimum confirmation needed:** Frank Barrett or Alejandro confirms all 4 phases executed. FastField submission status explained (never submitted, or submitted under a different project link).

---

## Project 7348 — Amtrust Cleveland

### 1. Identification
| Field | Value |
|-------|-------|
| Project number | 7348 |
| Project name | Amtrust Cleveland |
| Type | Workstation relocation |
| Current Supabase status | `in_progress` |

### 2. Dates
| Field | Value |
|-------|-------|
| Scheduled start | 2026-04-15 |
| Scheduled end | NULL — no end date recorded |
| Actual start | **NULL — never recorded** |
| Actual end | **NULL — never recorded** |
| Days past scheduled start (today 2026-06-28) | **74 days** |
| DB record last updated | **2026-04-17** (2 days after scheduled date) |

### 3. Assignment & Contacts
| Field | Value |
|-------|-------|
| PM | Pedro Martinez (pm_id linked, pm_assigned = true) |
| Client | Amtrust (client_id linked) |
| Client POC | NULL — not recorded |
| On-site POC | NULL — not recorded |

### 4. Confirmation Fields
| Field | Value | Reliability |
|-------|-------|-------------|
| vendor_confirmed | true | Possibly legitimate — vendor_required = true |
| client_confirmed | false | **Possibly unbackfilled** |
| access_confirmed | true | Possibly legitimate |
| client_informed | true | Recorded in DB |

### 5. Completion Signals
| Field | Value |
|-------|-------|
| fastfield_submitted | **true** |
| completion_report_sent | false |
| invoiced | false |

### 6. Scope Detail
| Field | Value |
|-------|-------|
| Scope summary | "On-site support & adjustments: punch list, furniture, artwork, electrical. Pedro Martinez PM." |
| Location | **116 Village Blvd, Suite 303, Princeton, NJ** |
| AI summary | "Apr 15. Princeton NJ. Amtrust on-site support. In progress. Pedro Martinez." |

### 7. Data Anomaly — Name vs. Location Mismatch
**Project is named "Amtrust Cleveland" but the recorded location is Princeton, NJ.**  
This is a significant data-quality flag. Possible explanations:
- The project name refers to the Amtrust client account (which may have offices in multiple cities), and the Apr 15 work was actually in Princeton NJ, not Cleveland.
- The location was entered incorrectly.
- "Cleveland" in the name may refer to an internal naming convention, not the city.

**This must be clarified before any status write.** If the work was actually in Princeton NJ and a different project number covers Cleveland, the status decision may differ.

### 8. Local Memory / RAG References
No dedicated memory file found for project 7348. The backfill review (open_loops/backfill_review_2026-06-26.md, indexed in RAG) references Amtrust as a client with multiple active projects but does not specifically call out 7348.

### 9. Communications Rows
**0 rows** — `communications` table empty.

### 10. Checklist Rows
**0 rows** — no checklist items linked.

### 11. FastField Forms
**0 rows** in `fastfield_forms` table — however, `fastfield_submitted = true` is set on the project record. The FastField form may have been submitted through FastField directly but not yet synced to Supabase (Make.com pipeline not yet active at scale).

### 12. Why It Appears Stuck
- Scheduled date was Apr 15. DB last updated Apr 17. Status never advanced from `in_progress` to `completed`.
- `fastfield_submitted = true` — field work appears to have occurred (this is the strongest signal of completion).
- `actual_start_at` and `actual_end_at` are both NULL — no timestamps recorded despite FastField being submitted.
- Scope is narrow ("punch list, furniture, artwork, electrical") — the kind of single-day job that should have closed quickly.

### 13. Evidence FOR Closing (candidate for completed)
- `fastfield_submitted = true` — this is the strongest completion signal available. FastField is submitted on-site at job completion.
- Scope was limited (punch list / adjustments), consistent with a single-day job.
- DB was last touched Apr 17 — 2 days after the job — suggesting activity at job close but status was not advanced.
- 74 days have passed with no further updates — no evidence of ongoing work.
- `vendor_confirmed = true`, `access_confirmed = true`, `client_informed = true` — operationally prepared and executed.

### 14. Evidence AGAINST Closing
- `client_confirmed = false` — weak signal (likely unbackfilled), but worth noting.
- No `actual_end_at` recorded — completion timestamp missing.
- Name/location mismatch (Cleveland vs. Princeton NJ) — ambiguity about what was actually completed.
- No completion report sent, no invoice.
- No FastField form data in `fastfield_forms` table (pipeline not connected), so the submission cannot be verified from DB alone.

### 15. Recommended Action
**Candidate for completed** — `fastfield_submitted = true` on a narrow-scope, single-day punch list job that is 74 days past its scheduled date is a strong indicator this is done. However, the name/location mismatch must be resolved first, and Pedro Martinez should confirm.

**Minimum confirmation needed:** Pedro Martinez or Alejandro confirms Apr 15 Princeton NJ work was completed. Location discrepancy explained ("Amtrust Cleveland" = client account name, not city).

---

## Side-by-Side Comparison

| Field | 7060 MMC Dallas | 7348 Amtrust Cleveland |
|-------|-----------------|----------------------|
| Scheduled end | 2026-04-30 (explicit) | None set |
| Days overdue | 59 days past end | 74 days past start |
| Last DB update | 2026-04-03 (Day 1) | 2026-04-17 (Day 2) |
| fastfield_submitted | **false** | **true** |
| Actual start/end | Start recorded, end NULL | Both NULL |
| Scope complexity | High — 4 phases, 1,199 items | Low — punch list, 1 day |
| PM contact | Frank Barrett | Pedro Martinez |
| Confidence to close | Low-medium — needs PM confirm + FF explanation | Medium-high — FF submitted, narrow scope |
| Recommended action | Needs email/PM verification | Candidate for completed (pending name/location clarification) |

---

*All data sourced read-only from Supabase and local RAG index. No writes performed.*
