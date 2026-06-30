# Client Index
_Last updated: 2026-06-30_

## Clients with Project Folders

| Client | Folder | Active Projects | Notes |
|---|---|---|---|
| Marsh McLennan (MMC / MMA) | marsh_mclennan/ | 7189, 7060, 7378, 7364, 7431, 7407, 7437, 7486, 7471, 7418, 7354, 7434, 7495, 7447, 7191, 7521, 7576, 7299, 7241 | MMC = Marsh McLennan Company; MMA = Marsh & McLennan Agency. Same parent. Multiple ongoing engagements across US offices. |
| Bentley Systems | bentley_systems/ | 7350, 7450 | Multi-phase engagement. 7350 = Phase 4 Final (July 1-2). 7450 = Framingham to Exton. |
| Vecos USA | vecos/ | 7579, 7454 | Locker commissioning. 7579 = JPMC Miami. Thin card also in jpmc/. |
| JPMC (JPMorgan Chase) | jpmc/ | 7579 (ref) | Reference card only. Full card in vecos/. |
| Pear VC | pear_vc/ | 7510 | 7510 = SF relocation to 600 Townsend (July 1). |
| Radian | radian/ | 7492 | 7492 = Denver decom. Comprehensive card updated 2026-06-30. |
| TierPoint | tierpoint/ | 7497 | Conflict: Supabase says "Radian TierPoint" / Cherry Hill vs. Philadelphia. Confirm with Alejandro. |
| Claritev / MultiPlan | claritev_multiplan/ | 7420, 6836, 6837, Chattanooga TBD | Parsippany NJ primary location. |
| Rothman Orthopaedics | rothman_orthopaedics/ | 7440, 7572 | Wayne PA and unknown second location. |
| Strategic Education | strategic_education/ | 7053, 7337, Guardian Lower Bucks TBD | SEI and possibly Guardian as subsidiary. |
| AmTrust Financial | amtrust/ | 7348 (pending), 7536 | Cleveland OH (7348 pending Teams send); NYC or Melville (7536). |
| Dropbox | dropbox/ | 7399, 7460, 7552 | SF-area offices. Possibly overlaps with Pear VC origin building. |
| Ingersoll Rand | ingersoll_rand/ | 7374 | FastField submitted; pending "approve batch complete 6" to close in Supabase. |
| Monster Energy | monster_energy/ | 7529 | Location Needs confirmation. |
| FAA Eastern Region | faa_eastern_region/ | 7559, EJM FAA (TBD) | Federal client. EJM FAA may be same or separate. |
| UiPath | uipath/ | Unknown | Project number not in export; check Supabase. |
| McGriff | mcgriff/ | 7553 | Dallas, TX decom. |
| Goldberg Segalla | goldberg_segalla/ | None on file | Law firm. No project details. |
| SS&C Technologies | ss_c_technologies/ | 7580 | No detail available. |
| Percheron Capital | percheron_capital/ | 7581 | No detail available. |
| Aerosphere | aerosphere/ | 7582 | No detail available. |
| BEC Online | bec_online/ | 7558 | No detail available. |
| Reckitt | reckitt/ | 7561 | No detail available. |
| Context Labs | context_labs/ | 7491 | No detail available. |
| Premier Orthopaedics | premier_orthopaedics/ | Unknown | No project number confirmed. |
| Vecos / IU Health | vecos_iu_health/ | Unknown | Bloomington IN locker commissioning. Separate from Vecos JPMC. |
| Tegna / Premion | tegna_premion/ | Unknown | No project number confirmed. |
| Lincoln / CRC Group | lincoln_crc_group/ | 7246 | No detail available. Note: separate from CRC Virginia Beach under MMC. |
| Teknion | teknion/ | 5156 | Historical project; low project number. |

## Unassigned / Ambiguous Projects

See `memory/clients/_unassigned/INDEX.md` for projects without a confirmed client or project number:
- Tampa packing supplies
- EJM FAA

## Other Known Clients (no project folder yet)

| Client | Known Projects | Notes |
|---|---|---|
| Warfel Construction | 7500 | White Marsh MD |
| Premier Workspaces | 7504 | NYC |
| Togetherwork / Kesef | 7512 | Montvale NJ |
| UPenn | 7425 | Philadelphia PA |
| Fox | 7490 | Location unknown |
| Resintech | 7381 | Camden NJ |
| The Team | 7474 | New York NY |
| Montebello | 7304 | West Berlin NJ |
| MMA (SD to Walnut Creek) | 7494 | San Diego to Walnut Creek (Jul 6) |
| MMA (Dallas conf. room) | 7546 | Dallas TX (Jul 9) |

## Creating a New Client Folder

When a new project card is created for a client that does not have a folder:

```
memory/clients/<client_slug>/
  CLIENT_CONTEXT.md
  projects/
    <project_number_slug>/
      PROJECT_CARD.md
      OPEN_LOOPS.md
      DRAFTS.md
      NOTES.md
```

Update this index when a new client folder is created.
