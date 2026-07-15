# Marsh McLennan — Client Context
_Last updated: 2026-07-10_

## Overview

Marsh McLennan is a global professional services firm.
InterWork has an ongoing multi-location engagement covering office moves, decommissions, and service calls across US offices.

All of the following names are treated as part of the same Marsh McLennan client family and filed here:
- **MMC** — Marsh McLennan Company (corporate parent)
- **Marsh** — the Marsh insurance brokerage business
- **Marsh McLennan** — full corporate name
- **MMA / Marsh McLennan Agency** — agency subsidiary
- **MarshMMA**, **MM Tech**, **Global Security** — internal groups or project labels

## Naming Convention — Use the Name on the Paperwork

When writing project names, quotes, FastField forms, WC reports, or client emails, use the exact entity name that appears on the project request or SOW. Do not rename.

| If paperwork says... | Use in project records... |
|---|---|
| MMC | MMC |
| MMA or Marsh McLennan Agency | MMA or Marsh McLennan Agency |
| Marsh | Marsh |
| MM Tech / Global Security | Use that name — do not convert to MMC |

Differentiate the name whenever it affects: **billing entity, project title, COI requirements, site access, client contacts, business unit ownership, or scope.**

For general coordination, scheduling, field updates, and internal tracking, it is fine to reference the specific project name while understanding these are all part of the Marsh McLennan account.

## Related Entities — Handle Carefully

The following entities are related to Marsh McLennan but may operate as separate business units with different billing, contacts, or scope ownership. **Do not automatically rename these as MMC.**

| Entity | Relationship | Rule |
|---|---|---|
| **Guy Carpenter** | Marsh McLennan subsidiary (reinsurance) | Use "Guy Carpenter" unless paperwork confirms MMC billing |
| **Mercer** | Marsh McLennan subsidiary (HR consulting) | Use "Mercer" unless paperwork confirms MMC billing |
| **Oliver Wyman** | Marsh McLennan subsidiary (management consulting) | Use "Oliver Wyman" unless paperwork confirms MMC billing |

If a project comes from one of these entities, file it under the entity that appears on the request, not automatically under marsh_mclennan/. If unsure, ask Alejandro.

**Oliver Wyman — MMC billing confirmed for project 7427** (2026-07-13): Smartsheet tracks it
as "MMC Oliver Wyman," and Alejandro confirmed Oliver Wyman is part of the MMC/MMA umbrella.
Filed under marsh_mclennan/ on that basis. This confirms the billing relationship for 7427
specifically — don't assume it extends to every future Oliver Wyman project without similar
confirmation, per the general rule above.

**Victor Insurance** — also filed under marsh_mclennan/ per Alejandro (2026-07-13): a
Mississauga service call coordinated through CBRE/Marsh, unrelated to project 7427 (Oliver
Wyman) despite both involving Mississauga offices. No InterWork project number confirmed for
Victor Insurance's job — see its project folder.

**McGriff is not one of these** — confirmed directly by Alejandro, 2026-07-10: McGriff is a
subsidiary of MMA/MMC, not a separate billing entity. File McGriff-referencing projects
under marsh_mclennan/ unless a specific project explicitly indicates separate billing.
(The former `memory/clients/mcgriff/` folder — project 7553 — was merged in here 2026-07-10;
see 7553 below.)

## Known Projects

| # | Name | Location | Status | Notes |
|---|---|---|---|---|
| 7189 | MMC Bermuda Inventory Hoboken NJ | 121 River St, Hoboken NJ | Scheduled Jul 1 | Field PM: Jairo Escalante. Multi-phase since Oct 2025. See project folder. |
| 7546 | MMC/MMA Dallas Conference Room Table Removal | 13155 Noel Rd, 11th Floor, Dallas TX | Intake/review — date unconfirmed, do not assume 7/9 | SOW PM: Frank Barrett. Quote #8482, $1,100. Do not use "5549" as the project number. See project folder. |
| 7060 | MMC Dallas Walnut Hill to Galleria | Dallas TX | In-progress (overdue) | Client unconfirmed; draft ready; 3 months overdue |
| 7378 | MMA Sepulveda 5th Floor (Phase 2 Decom) | Sepulveda Blvd, Van Nuys CA | Planning | Phase 1 complete; decom incoming. Evette Acosta. See project folder. |
| 7364 | MMC Allentown Move | Allentown PA | Scheduled (past-dated) | FastField submitted; likely done |
| 7431 | MMC Walkthrough Austin TX | Austin TX | Scheduled (past-dated) | Vendor confirmed; no FastField |
| 7521 | MMC Austin Restack | Austin TX | Planning | 105 desks, 154 monitors, crate work. Vendor transition to Monica. See project folder. |
| 7576 | Marsh Broomfield Motor Swap | Broomfield CO | Pending | Single service call — Mt. Wilson desk motor swap. Vendor: Mike (TBC). See project folder. |
| 7299 | MMC Alpharetta Monitor Arms | Alpharetta GA | Needs confirmation | Monitor arm install; details sparse. See project folder. |
| 7241 | MMC Allentown Move | Allentown PA | Needs confirmation | Relocation scope; details sparse. See project folder. |
| 7407 | MMC Install Service Call Phoenix | Phoenix AZ | Scheduled (past-dated) | External PM; vendor confirmed |
| 7437 | CRC Decom Internal Move | Virginia Beach VA | Scheduled (past-dated) | No signals — check if related to MMC |
| 7486 | MMA Austin TX | Austin TX | Scheduled (past-dated) | No signals |
| 7471 | MMA Decom + Move Loveland OH | Loveland OH | Scheduled (past-dated) | Frank Barrett PM; no FastField |
| 7418 | MMA Colleague Relocation Columbia MD | Columbia MD | Scheduled (past-dated) | No PM in pm_assigned field |
| 7354 | MMA Retrieve Tech Alpharetta GA | Alpharetta GA | Scheduled (past-dated) | External PM; vendor confirmed |
| 7434 | MMA Edina Office Refresh | 5050 Lincoln Drive Suite 460, Edina MN | Completed per 2026-07-10 handoff — Supabase status not yet reconciled | Full scope: C-bins, packing, decom, electrical, painting, furniture install, monitor arms, tech reconnect, shades, return cleanup visit. 2 open items: café furniture install, additional lockers quote. See project folder. |
| 7495 | MMA Move/Light Decom Charlotte NC | Charlotte NC | Scheduled (past-dated) | Melvin Hernandez PM; vendor confirmed |
| 7447 | MMA Tech Install Clearwater FL | Clearwater FL | Scheduled (past-dated) | Bad actual_end_at; fix held |
| 7191 | MMA Punch List Cape May NJ | Cape May NJ | Scheduled (past-dated) | No signals |
| 7347 | MMA McLean Consolidation / Wilmington Zoom Room AV Recovery | McLean VA → Wilmington NC | Active — AV recovery visit pending, week of 7/13 | Original May move looked done (fastfield submitted); recovery handoff 2026-07-10 found the Zoom Room AV system was never fully shipped. Removed from the pending Supabase batch-completion approval. See project folder. |
| 7553 | MMC Walk for Decom Dallas TX | 1717 Main St, Dallas TX, 44th Floor | Scheduled (past-dated) | Client POC Michael Durkin (Marsh/CBRE); PM Jairo Escalante; client_informed + access_confirmed + fastfield_submitted all true. Merged in 2026-07-10 from a former separate mcgriff/ folder — client entity was always MMC. See project folder. |
| 7427 | Oliver Wyman Mississauga Decom & Toronto Relocation | 5945 Airport Road, Mississauga ON → 120 Bremner Blvd 13th Fl, Toronto ON | In Progress — scheduled 7/13-7/15 | Client tracked as "MMC Oliver Wyman" in Smartsheet. Move/reconfig order Won (IWSQ8324, $9,241); decom quote Pending (IWSQ8524, $5,334). See project folder. |
| (none) | Victor Insurance Mississauga Service Call | Mississauga, ON | Operationally complete; admin/financial close-out open | No confirmed InterWork project number. Coordinated via CBRE/Marsh. Separate from 7427 despite same city. See project folder. |

## Known Contacts

| Name | Role | Contact |
|---|---|---|
| Hunter Barbieri | InterWork office assignee on several MMC projects | hunterb@interworkoffice.com |
| Jairo Escalante | Field PM for 7189 | jairoe@interworkoffice.com |

Client-side contacts vary by location and project. Check individual project cards.
No single primary MMC/MMA client contact identified yet.

## How to Use This Folder

1. Read `memory/company_knowledge/START_HERE.md` first
2. Read this file
3. Read the relevant project folder: `projects/<project_slug>/PROJECT_CARD.md`
4. If files are not accessible, ask Alejandro to paste the project card

Do not guess project details. Do not invent contact names or phone numbers.
