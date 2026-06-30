# UiPath — Claude Chat Knowledge Pack

_Generated: 2026-06-30 (rescheduled status fix) | Source: memory/clients/uipath/_

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

### UiPath Projects in Dashboard (Live Read — 2026-06-30)

**1450 Broadway Move Out — NOT in Supabase/dashboard.**
Live read confirmed: this project has no Supabase record yet. The repo project card is the authoritative source.
Known UiPath rows in dashboard: 7516, 7479, 7403, 7489, 7227, 7317, 6787.
A new Supabase record will be needed once a project number is assigned or Alejandro approves.

_No UiPath rows appeared in today's scheduled/active dashboard view for 2026-06-30._

> **For dashboard/status questions:** use the global counts above for overall operational context.
> **For 1450 Broadway specifically:** use the project card in this pack — it is not in Supabase yet.
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
| TBD | 1450 Broadway Move Out | 1450 Broadway, 21st Floor, NY 10018 | **Rescheduled — July 8, 2026, 11:00 AM** | Project # not assigned; date confirmed by Morgan Alvarado email 2026-06-30; not in Supabase |

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

- **Location:** 1450 Broadway, 21st Floor, New York, NY 10018
- **Execution date:** **Wednesday, July 8, 2026, 11:00 AM start** (confirmed by client)
- **Status:** **Rescheduled — date confirmed**
- **Scope:** ~55 smaller boxes; a few to 1 Vanderbilt; majority to donation locations (labeled/grouped); additional disposal items
- **Freight entry:** 41st Street between 6th Ave and Broadway, door next to FedEx; building management has InterWork COI on file
- **Onsite contacts:** Michele Nerio (512-426-1492), Morgan Alvarado (929-996-5850)
- **Donation locations:**
  - Materials for the Arts, 33-00 Northern Blvd, LIC 11101 — M/W/F 9am–2:30pm; dock available; arrive before 2:15 PM
  - Goodwill NYNJ Donation Center, 1114 1st Ave, NY 10065 — M–Sun 11am–7pm
  - Housing Works, 157 E 23rd St, NY 10010 — M–Sat 12pm–7pm
- **Source of confirmation:** Morgan Alvarado email, 2026-06-30 2:01 PM
- **Project #:** Unknown — not yet assigned; do not invent one
- **Supabase/dashboard:** Not present as of 2026-06-30 live read; project card is authoritative

**Open loops:**

| # | Loop | Owner | Status |
|---|---|---|---|
| 1 | ~~New execution date~~ | ~~Morgan Alvarado~~ | **Resolved — July 8, 2026, 11:00 AM** |
| 2 | ~~Final scope confirmation~~ | ~~Morgan Alvarado~~ | **Resolved — ~55 boxes, donation breakdown confirmed** |
| 3 | ~~Building access information~~ | ~~TBD~~ | **Resolved — 41st St freight entry; COI on file** |
| 4 | ~~On-site POC~~ | ~~TBD~~ | **Resolved — Michele Nerio / Morgan Alvarado** |
| 5 | Project number assignment | InterWork internal | Still open |
| 6 | Item-level inventory / floor plan | TBD | Still open — box count known, no item list yet |
| 7 | InterWork team freight/access logistics | David Steinbrecher / InterWork Ops | Still open |
| 8 | Supabase record creation | Alejandro / internal | Still open — needs project number first |

**Drafts pending:** None — draft only when Alejandro requests it.

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
2. **1450 Broadway is Rescheduled for July 8, 2026, 11:00 AM** — date and scope confirmed by Morgan Alvarado email 2026-06-30. Do not describe it as postponed or awaiting a date.
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
