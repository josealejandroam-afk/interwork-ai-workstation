# Marsh McLennan — Claude Chat Knowledge Pack

_Generated: 2026-06-30 (dashboard snapshot update) | Source: memory/clients/marsh_mclennan/_

---

## How to Use This Pack

Upload this file to a Claude Chat Project named "Marsh McLennan" or "MMC."
Start every session by telling Claude: "You have the Marsh McLennan knowledge pack loaded. Use it as your source of truth for all MMC/Marsh/MMA projects."

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

### MMC / MMA Projects in Today's Dashboard

| Project # | Client | Location | Type | Date Range | Time | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|---|
| 7556 | MMA | 1717 Main St, Dallas, TX | Install | 6/24/26–6/30/26 | 9:00 AM | External PM | Scheduled | Ready |

> **For dashboard/status questions:** use the counts and rows above for today's operational status.
> Then check the project table below for context, contacts, and open loops.
> If this snapshot conflicts with a project entry, flag the conflict — do not silently pick one.
> For live operational status, dashboard/Supabase wins. For scope, contacts, notes, and history, the project entry wins.
>
> Full snapshot: `memory/dashboard/CURRENT_DASHBOARD_STATUS.md`
> Rules for reconciling sources: `memory/dashboard/DASHBOARD_CHECK_RULES.md`

---

## Client Overview

Marsh McLennan (MMC) is a global professional services firm. InterWork has an ongoing multi-location engagement covering office moves, decommissions, and service calls across US offices.

**All of the following names refer to the same client family and are filed together:**
- MMC — Marsh McLennan Company (corporate parent)
- Marsh — the Marsh insurance brokerage business
- Marsh McLennan — full corporate name
- MMA / Marsh McLennan Agency — agency subsidiary
- MarshMMA, MM Tech, Global Security — internal groups or project labels

### Naming Rule
Use the exact entity name that appears on the project request or SOW. Do not rename.

| Paperwork says | Use in records |
|---|---|
| MMC | MMC |
| MMA or Marsh McLennan Agency | MMA or Marsh McLennan Agency |
| Marsh | Marsh |
| MM Tech / Global Security | Use that name — do not convert to MMC |

### Related Entities — Handle Carefully
These are MMC subsidiaries but may have separate billing and contacts:

| Entity | Relationship | Rule |
|---|---|---|
| Guy Carpenter | MMC subsidiary (reinsurance) | Use "Guy Carpenter" unless paperwork says MMC billing |
| Mercer | MMC subsidiary (HR consulting) | Use "Mercer" unless paperwork says MMC billing |
| Oliver Wyman | MMC subsidiary (management consulting) | Use "Oliver Wyman" unless paperwork says MMC billing |
| McGriff | MMC-affiliated (insurance brokerage) | Use "McGriff" — has its own client folder |

---

## Active and Upcoming Projects

| # | Name | Location | Dates | Status | Notes |
|---|---|---|---|---|---|
| 7556 | MMA Art Work Hanging Dallas | 1717 Main St, Dallas, TX | 6/24/26–6/30/26, 9 AM | Active — on today's dashboard, Ready | External PM; Install scope |
| 7189 | MMC Bermuda Inventory Hoboken NJ | 121 River St, Hoboken NJ | Jul 1 | Scheduled | Field PM: Jairo Escalante. Multi-phase since Oct 2025. |
| 7378 | MMA Van Nuys Decom — Phase 3 | Sepulveda Blvd, 5th Fl, Van Nuys CA | 7/13–7/16, 9 AM | Scheduled | Phase 2 dates (6/1–6/4) superseded. Evette Acosta contact. |
| 7494 | MMA Furniture Move — SD to Walnut Creek | San Diego CA → Walnut Creek CA | 7/8–7/9, load-in 6 PM Wed | Scheduled | Client (Marie Peralta) confirmed 6/29; Smartsheet had wrong dates (7/6–7/9). |
| 7495 | MMA Charlotte Restack Phase 1 | Charlotte, NC | 7/2 supplies + 7/13–7/17 main, 9 AM | Scheduled | PM: Melvin Hernandez. Supersedes 5/27–5/28 dates. |
| 7521 | MMC Austin Restack | Austin TX | TBD | Planning | 105 desks, 154 monitors, crate work. Vendor transition to Monica. |
| 7576 | Marsh Broomfield Motor Swap | Broomfield CO | TBD | Pending | Single desk motor swap. Vendor: Mike (TBC). |
| 7472 | MMA Punchlist Addison | Addison TX | end 7/7 (TBD) | Active | Punchlist leg added; dates TBD on Smartsheet. |
| 7465 | MMA Ancillary Furniture Move | TBD | start 7/16 | Scheduled | Start date corrected from 7/15. |

## Recent / Past-Dated Projects

| # | Name | Location | Notes |
|---|---|---|---|
| 7060 | MMC Dallas Walnut Hill to Galleria | Dallas TX | In-progress (overdue ~3 months); client unconfirmed; draft ready |
| 7484 | MMC Crates Pickup Austin TX | Austin TX | End date 6/26; additional legs found |
| 7486 | MMC Austin TX | Austin TX | End date 6/26; additional legs found |
| 7364 | MMC Allentown Move | Allentown PA | FastField submitted; likely done |
| 7431 | MMC Walkthrough Austin TX | Austin TX | Vendor confirmed; no FastField |
| 7299 | MMC Alpharetta Monitor Arms | Alpharetta GA | Monitor arm install; details sparse |
| 7241 | MMC Allentown Move | Allentown PA | Relocation scope; details sparse |
| 7407 | MMC Install Service Call Phoenix | Phoenix AZ | External PM; vendor confirmed |
| 7471 | MMA Decom + Move Loveland OH | Loveland OH | Frank Barrett PM; no FastField |
| 7418 | MMA Colleague Relocation Columbia MD | Columbia MD | No PM in pm_assigned field |
| 7354 | MMA Retrieve Tech Alpharetta GA | Alpharetta GA | External PM; vendor confirmed |
| 7434 | MMA Paint Scope Edina MN | Edina MN | No FastField; status unclear |
| 7447 | MMA Tech Install Clearwater FL | Clearwater FL | Bad actual_end_at field; fix held |
| 7191 | MMA Punch List Cape May NJ | Cape May NJ | No signals |

---

## Known Contacts

| Name | Role | Contact |
|---|---|---|
| Hunter Barbieri | InterWork office PM — multiple MMC projects | hunterb@interworkoffice.com |
| Jairo Escalante | Field PM — project 7189 | jairoe@interworkoffice.com |
| Melvin Hernandez | PM — project 7495 (Charlotte Restack) | — |
| Marie Peralta | Client contact — MMA (7494 SD to Walnut Creek) | confirmed via email 6/29 |
| Evette Acosta | Client POC — MMA Van Nuys (7378) | — |
| Francisco Vinueza | Referenced for 7553 scope assessment | — |

Client-side contacts vary by location. Ask Alejandro for project-specific contacts.

---

## Operating Rules for This Client

1. **7556 is on today's dashboard (6/30/26)** — Scheduled, Ready, External PM, 9:00 AM, 1717 Main St Dallas.
2. **If asked about operational status** — check the dashboard snapshot section above first.
3. **If dashboard status conflicts with a project entry** — flag it, ask Alejandro to confirm.
4. **Never invent contacts.** If a contact is not in this pack or pasted by Alejandro, say "contact not on file."
5. **Never reference a project's details from memory alone.** Ask for the project card if needed.
6. **Use the exact entity name on the paperwork** — do not automatically write "MMC" for MMA projects.
7. **Past-dated projects are not confirmed closed** unless there is a FastField completion + WC report.
8. **Do not send any communication** — draft only, then Alejandro reviews and sends.
9. **Do not write to Supabase** — propose changes in a table, wait for approval.
10. **Date overrides:** When client-confirmed dates differ from Smartsheet, the client-confirmed date is authoritative (e.g., 7494 load-in 7/8 not 7/6).

---

## Drafting Standards

### Client confirmation (project complete)
- Subject: `[Project #] [Client Name] [Location] — Work Complete`
- Body: Date, scope completed, field PM, any open items
- Tone: Professional, brief, factual — no filler phrases

### Internal status update
- State: project number, location, status, next action
- Flag any discrepancy between what was planned and what happened

---

_To refresh this pack: tell Claude Code to regenerate claude_project_packs/marsh_mclennan_knowledge_pack.md_
