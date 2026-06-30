# InterWork Overview

## Company

**InterWork Office Solutions** is a commercial furniture moving and installation company.

Services include:
- Office relocations (full moves, phased moves, internal restacks)
- Furniture decommissions (pickup, disposal, donation coordination)
- Furniture installations and service calls (workstations, monitor arms, media carts, whiteboards)
- Site walkthrough and inventory projects
- IT equipment relocation (switches, firewalls, access points)
- Storage and asset management
- Work completion reporting
- Vendor and crew coordination
- Disposal, recycling, and sustainability coordination (notify Jade early for decom scopes)
- Client-facing scheduling and status updates

**InterWork Warehouse:** 439 Commerce Lane, West Berlin, NJ 08091
Used for storage, staging, asset holding, and pickup/delivery coordination. Full address used in field notices. Not disclosed to clients unless explicitly appropriate.

## Alejandro's Role

**Alejandro Acosta** is the Operations Coordinator at InterWork.

He manages the full project lifecycle from quote to closeout:
- Receives project requests from account managers (e.g., Jill Buchman)
- Coordinates PMs and vendors for execution
- Communicates with clients before, during, and after jobs
- Reviews FastField submissions and work completion reports
- Maintains project data in Supabase and Smartsheet

## The AI Workstation

The AI workstation is an operations support system built for Alejandro.

It reads live project data from Supabase (140+ projects), maintains structured project memory in this GitHub repo, generates drafts for client and team communications, and helps Alejandro stay ahead of scheduling gaps, missing confirmations, and overdue statuses.

Claude Code is the operator session — it has repo access, executes scripts, queries Supabase, and commits memory updates. Claude Chat is the conversation assistant — it needs the handoff pasted in to be current.

## Project Types (common abbreviations used in project names)

| Term | Meaning |
|---|---|
| Relocation / Move | Full office move from one address to another |
| Decom | Decommission — remove and dispose of furniture or assets |
| Install | Deliver and install furniture at a location |
| Service Call | Single-task visit (repair, swap, minor adjustment) |
| Walkthrough | Site visit for inventory, scoping, or inspection |
| Punch List | Follow-up visit to complete outstanding items |
| FF | FastField — the field form submitted by the on-site PM after work |
| WC Report | Work Completion Report — delivered to the client after job closure |
| HA Desk | Height-Adjustable Desk |
| LBC | Locker Base Controller (Vecos SMART locker system) |

## Project Lifecycle (brief)

Quote issued → Project number assigned in QuickQuo → Smartsheet entry created → PM and vendor assigned → FastField submitted after execution → Work completion report generated → Completion email sent to client → Supabase status set to completed

See `OPERATING_WORKFLOW.md` for the full sequence.
