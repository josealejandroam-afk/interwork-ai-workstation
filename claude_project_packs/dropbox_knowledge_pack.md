# Dropbox — Claude Chat Knowledge Pack

_Generated: 2026-06-30 (dashboard snapshot update) | Source: memory/clients/dropbox/_

---

## How to Use This Pack

Upload this file to a Claude Chat Project named "Dropbox."
Start every session by telling Claude: "You have the Dropbox knowledge pack loaded. Use it as your source of truth for all Dropbox projects."

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

### Dropbox Projects in Today's Dashboard

| Project # | Client | Location | Type | Date Range | Time | Execution Owner | Status | Readiness |
|---|---|---|---|---|---|---|---|---|
| 7552 | Dropbox | 1800 Owens St, San Francisco, CA 94117 | Relocation | 6/22/26–6/30/26 | 9:00 AM | Frank Barrett | Scheduled | **At Risk** |

> **Readiness: At Risk** — project 7552 is on today's dashboard flagged At Risk.
> This means one or more required fields are missing or unconfirmed. Investigate before execution.
>
> **For dashboard/status questions:** use the counts and rows above for today's operational status.
> Then check the project card below for context, contacts, and open loops.
> If this snapshot conflicts with the project card, flag the conflict — do not silently pick one.
> For live operational status, dashboard/Supabase wins. For scope, contacts, notes, and history, the project card wins.
>
> Full snapshot: `memory/dashboard/CURRENT_DASHBOARD_STATUS.md`
> Rules for reconciling sources: `memory/dashboard/DASHBOARD_CHECK_RULES.md`

---

## Client Overview

Dropbox is a cloud storage and collaboration company. InterWork has multiple projects for Dropbox, including work related to their San Francisco offices and a Seattle studio move.

**Address overlap note:** Dropbox's former HQ was at 1800 Owens St, San Francisco — the same building listed as the origin address in Pear VC project 7510. The move from 1800 Owens to 600 Townsend may overlap with or be adjacent to the Pear VC relocation. These are tracked as separate projects. Confirm with Alejandro if scope or crew overlaps.

---

## Known Projects

| # | Name | Location | PM | Date | FastField | Status |
|---|---|---|---|---|---|---|
| 7399 | Dropbox Project | Possibly SF, CA | TBD | TBD | Unknown | Needs confirmation |
| 7460 | Dropbox Project | Needs confirmation | TBD | TBD | Unknown | Needs confirmation |
| 7467 | Seattle Studio Move | Seattle, WA | Francisco Vinueza | 2026-04-27 | false | Past-dated — no signals |
| 7552 | Dropbox SF Relocation | 1800 Owens St, San Francisco, CA 94117 | Frank Barrett | 6/22/26–6/30/26 | Unknown | Active — on today's dashboard, **At Risk** |

---

## Project 7552 — Key Details

- **Location:** 1800 Owens St, San Francisco, CA 94117 (confirmed from dashboard)
- **Date range:** 6/22/26–6/30/26 (per dashboard)
- **Time:** 9:00 AM
- **PM:** Frank Barrett (confirmed from dashboard)
- **Type:** Relocation
- **Readiness:** At Risk — reason unknown; investigate before execution

---

## Data Quality Notes

- Project 7552 location, PM, and date confirmed from dashboard snapshot 6/30/26.
- At Risk flag reason not captured — run live refresh or ask Alejandro.
- Projects 7399 and 7460 remain sparse — no scope, dates, or PM confirmed.
- Project 7467 Seattle is past-dated with no completion signals.
- Do not guess details for sparse projects.

---

## Known Contacts

No contacts on file. Ask Alejandro before drafting any client communication.

---

## Operating Rules for This Client

1. **7552 is on today's dashboard (6/30/26)** — Scheduled, **At Risk**, Frank Barrett, 9:00 AM.
2. **At Risk means something is unconfirmed** — do not assume the project is safe to execute without checking.
3. **If asked about operational status** — check the dashboard snapshot section above first.
4. **If dashboard status conflicts with project card** — flag it, ask Alejandro to confirm.
5. **Do not conflate Dropbox and Pear VC projects** even though both reference the 1800 Owens St address.
6. **Do not send communication** — draft only, Alejandro reviews and sends.
7. **Do not write to Supabase** — propose changes, wait for approval.
8. **If asked for project details not in this pack** — say "not on file" and ask Alejandro to paste the project card.

---

_To refresh this pack: tell Claude Code to regenerate claude_project_packs/dropbox_knowledge_pack.md_
