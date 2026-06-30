# UiPath — Claude Chat Knowledge Pack

_Generated: 2026-06-30 (dashboard snapshot update) | Source: memory/clients/uipath/_

---

## How to Use This Pack

Upload this file to a Claude Chat Project named "UiPath."
Start every session by telling Claude: "You have the UiPath knowledge pack loaded. Use it as your source of truth for all UiPath projects."

---

## Dashboard Snapshot — 2026-06-30

> **Source:** Manual screenshot — needs live Supabase refresh for full accuracy.
> **If this pack is more than 1 day old, treat counts as stale.** Ask Claude Code to run `scripts/update_dashboard_snapshot.ps1` and regenerate.

### Global Counts (as of snapshot)

| Filter | Count |
|---|---|
| All (active) | 140 |
| Alerts | 47 |
| At Risk | 46 |
| Today | 4 |
| Tomorrow | 3 |
| This Week | 9 |

### UiPath Projects in Today's Dashboard

_No UiPath projects appeared in today's dashboard rows (2026-06-30)._
_Project 7516 is past-dated (2026-05-15). The 1450 Broadway project is Postponed with no confirmed execution date._

> **For dashboard/status questions:** use the global counts above for overall operational context.
> UiPath-specific operational status must come from the project cards below — no live dashboard rows captured.
> If a future snapshot shows a UiPath row, it will appear here after the next pack regeneration.
>
> Full snapshot: `memory/dashboard/CURRENT_DASHBOARD_STATUS.md`
> Rules for reconciling sources: `memory/dashboard/DASHBOARD_CHECK_RULES.md`

---

## Client Overview

UiPath is an enterprise automation software company. InterWork has an active engagement for a NYC move-out project and a past-dated service call in Dallas.

---

## Known Projects

| # | Name | Location | Status | Notes |
|---|---|---|---|---|
| 7516 | Service Call Dallas TX | Dallas, TX (full address TBC) | Past-dated 2026-05-15 — no completion signals | External PM; vendor confirmed; access confirmed; no FastField |
| TBD | 1450 Broadway Move Out | 1450 Broadway, New York, NY | **Postponed** — awaiting new date from Morgan Alvarado | Project # not assigned; original target week of 6/29; tentative July 1 date internally cancelled |

---

## Project 7516 — Service Call Dallas TX

- **Location:** Dallas, TX (full address needs confirmation)
- **Scheduled:** 2026-05-15
- **PM:** External PM (name needs confirmation)
- **Vendor:** Confirmed
- **Access:** Confirmed
- **FastField:** false
- **Status:** Past-dated — no completion signals on file

**Open loops:**
1. Confirm project 7516 is complete — no FastField on file
2. Confirm full Dallas TX address
3. Identify external PM name

---

## Project TBD — 1450 Broadway Move Out (NYC)

- **Location:** 1450 Broadway, New York, NY
- **Scope:** Review storage rooms; relocate designated items; dispose of unwanted items/furniture
- **Initial request:** 2026-06-12
- **Original target:** Week of 2026-06-29
- **Tentative execution:** 2026-07-01 (internally scheduled — **NOT client-confirmed; now postponed**)
- **Status:** **Postponed** — UiPath postponed the July 1 date; Morgan Alvarado to send formal email with new date
- **Project #:** Unknown — not yet assigned; do not invent one
- **Confidence:** Medium — based on email/chat context; no Supabase record yet

**Open loops:**

| # | Loop | Owner | Status |
|---|---|---|---|
| 1 | New execution date | Morgan Alvarado (UiPath) | Pending — awaiting formal email |
| 2 | Final scope (quantities, inventory, destinations) | Morgan Alvarado | Not provided |
| 3 | Building access information | TBD | Not provided |
| 4 | Inventory or floor plan | TBD | Not provided |
| 5 | On-site point of contact for rescheduled work | TBD | Not provided |
| 6 | Project number assignment | InterWork internal | Not assigned |

**Drafts pending:** None — hold all client-facing drafts until Morgan's formal postponement email arrives.

---

## Known Contacts

| Name | Role | Project |
|---|---|---|
| Morgan Alvarado | Client — Workplace Experience Manager | 1450 Broadway (primary contact) |
| Simon Chey | Client contact | 1450 Broadway |
| Michele Nerio | Client contact | 1450 Broadway |
| David Steinbrecher | InterWork PM | 1450 Broadway |
| Francisco Vinueza | InterWork | 1450 Broadway |

No client-side contacts confirmed for project 7516. Ask Alejandro before drafting any client communication.

---

## Operating Rules for This Client

1. **Do not invent a project number for 1450 Broadway** — it has not been assigned yet.
2. **Do not draft any client-facing communication for 1450 Broadway** until Morgan Alvarado's formal postponement email arrives.
3. **Project 7516 is past-dated with no FastField** — do not assume it is complete; flag as open loop.
4. **If asked about operational status** — check the dashboard snapshot section above first.
5. **If dashboard snapshot conflicts with a project card** — flag the conflict; ask Alejandro to confirm.
6. **Do not send communication** — draft only, Alejandro reviews and sends.
7. **Do not write to Supabase** — propose changes, wait for approval.

---

## PM Key (InterWork)

AJ = Alejandro Acosta | DS = David Steinbrecher | FV = Francisco Vinueza | HB = Hunter Barbieri | JuM = Juan Martinez | FB = Frank Barrett | JE = Jairo Escalante | MH = Melvin Hernandez | EXT = External PM

---

_To refresh this pack: tell Claude Code to regenerate claude_project_packs/uipath_knowledge_pack.md_
