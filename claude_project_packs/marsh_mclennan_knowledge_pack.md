# Marsh McLennan — Claude Chat Knowledge Pack

_Generated: 2026-06-30 | Source: memory/clients/marsh_mclennan/_

---

## How to Use This Pack

Upload this file to a Claude Chat Project named "Marsh McLennan" or "MMC."
Start every session by telling Claude: "You have the Marsh McLennan knowledge pack loaded. Use it as your source of truth for all MMC/Marsh/MMA projects."

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

## Active and Recent Projects

| # | Name | Location | Status | Notes |
|---|---|---|---|---|
| 7189 | MMC Bermuda Inventory Hoboken NJ | 121 River St, Hoboken NJ | Scheduled Jul 1 | Field PM: Jairo Escalante. Multi-phase since Oct 2025. |
| 7060 | MMC Dallas Walnut Hill to Galleria | Dallas TX | In-progress (overdue) | Client unconfirmed; draft ready; 3 months overdue |
| 7378 | MMA Sepulveda 5th Floor (Phase 2 Decom) | Sepulveda Blvd, Van Nuys CA | Planning | Phase 1 complete; decom incoming. Evette Acosta contact. |
| 7521 | MMC Austin Restack | Austin TX | Planning | 105 desks, 154 monitors, crate work. Vendor transition to Monica. |
| 7576 | Marsh Broomfield Motor Swap | Broomfield CO | Pending | Single desk motor swap. Vendor: Mike (TBC). |

## Past-Dated / Needs Confirmation

| # | Name | Location | Notes |
|---|---|---|---|
| 7364 | MMC Allentown Move | Allentown PA | FastField submitted; likely done |
| 7431 | MMC Walkthrough Austin TX | Austin TX | Vendor confirmed; no FastField |
| 7299 | MMC Alpharetta Monitor Arms | Alpharetta GA | Monitor arm install; details sparse |
| 7241 | MMC Allentown Move | Allentown PA | Relocation scope; details sparse |
| 7407 | MMC Install Service Call Phoenix | Phoenix AZ | External PM; vendor confirmed |
| 7486 | MMA Austin TX | Austin TX | No signals |
| 7471 | MMA Decom + Move Loveland OH | Loveland OH | Frank Barrett PM; no FastField |
| 7418 | MMA Colleague Relocation Columbia MD | Columbia MD | No PM in pm_assigned field |
| 7354 | MMA Retrieve Tech Alpharetta GA | Alpharetta GA | External PM; vendor confirmed |
| 7434 | MMA Paint Scope Edina MN | Edina MN | No FastField; status unclear |
| 7495 | MMA Move/Light Decom Charlotte NC | Charlotte NC | Melvin Hernandez PM; vendor confirmed |
| 7447 | MMA Tech Install Clearwater FL | Clearwater FL | Bad actual_end_at field; fix held |
| 7191 | MMA Punch List Cape May NJ | Cape May NJ | No signals |

---

## Known Contacts

| Name | Role | Contact |
|---|---|---|
| Hunter Barbieri | InterWork office PM — multiple MMC projects | hunterb@interworkoffice.com |
| Jairo Escalante | Field PM — project 7189 | jairoe@interworkoffice.com |

Client-side contacts vary by location. Ask Alejandro for project-specific contacts.

---

## Operating Rules for This Client

1. **Never invent contacts.** If a contact is not in this pack or pasted by Alejandro, say "contact not on file."
2. **Never reference a project's details from memory alone.** Ask for the project card if needed.
3. **Use the exact entity name on the paperwork** — do not automatically write "MMC" for MMA projects.
4. **Past-dated projects are not confirmed closed** unless there is a FastField completion + WC report.
5. **Do not send any communication** — draft only, then Alejandro reviews and sends.
6. **Do not write to Supabase** — propose changes in a table, wait for approval.

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
