# Vecos — Claude Project Bootstrap
_Upload this file to the "VECOS Projects" Claude Project. Do not re-upload unless routing changes._
_Last updated: 2026-07-01_

---

## Client

- **Name:** Vecos USA (SMART locker technology provider)
- **Primary slug:** `vecos` — JPMC Miami (7579) and Tallahassee FL (7454)
- **Secondary slug:** `vecos_iu_health` — IU Health Bloomington IN (# TBD)
- **Repo:** https://github.com/josealejandroam-afk/interwork-ai-workstation
- **Raw base URL:** `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

---

## Two Client Folders — Use the Right One

| Folder | End-user site | Projects |
|---|---|---|
| `memory/clients/vecos/` | JPMC Miami FL, Tallahassee FL | 7579, 7454 |
| `memory/clients/vecos_iu_health/` | IU Health Bloomington IN | TBD |

**Vecos USA is the InterWork client in both cases.** JPMC and IU Health are end-user sites — do not file or label work as JPMC or IU Health projects.

---

## Vecos Technical Pattern (applies to all commissioning projects)

Every Vecos commissioning project requires:
1. Enter Primary LBC IP
2. Enter Secondary LBC IP
3. Enter and activate license keys
4. Coordinate firmware push with Vecos PM
5. Required tools: screwdriver, wrench, 7mm socket, ladder (confirm onsite availability)

Do not create execution documents until date, technician, and building access are confirmed.

---

## At the Start of Each Chat — Fetch These Files

0. **AI index (fast lookup):**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/ai_index/START_HERE_FOR_AI.md`

   Use this first. It points to CLIENT_ROSTER.md, PROJECT_INDEX.md, and OPEN_LOOPS_SUMMARY.md for quick navigation.

1. **Company rules:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md`

2. **Live dashboard API (operational status — use this first):**
   `https://interwork-command-center.vercel.app/api/ai/dashboard-summary`

   Returns live counts and today/tomorrow/at-risk rows from Supabase. No auth needed. Confirmed live 2026-06-30.
   Fallback if unavailable: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md`

3. **Vecos client context:**
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/vecos/CLIENT_CONTEXT.md`

   For IU Health project also fetch:
   `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/vecos_iu_health/CLIENT_CONTEXT.md`

---

## Known Projects — Fetch by Project

| Project | Slug | Location | Notes |
|---|---|---|---|
| 7579 — JPMC Miami Lockers | `vecos/projects/7579_jpmc_miami_lockers` | 1450 Brickell Ave, Miami FL 33131, 33rd Fl | Pending scheduling. Contact: Cason Perez. |
| 7454 — Tallahassee FL | — | Tallahassee FL | Status needs verification — past-dated Apr 16, no FastField signals. No project card confirmed in repo. |
| TBD — IU Health Bloomington | `vecos_iu_health/projects/unknown_iu_health_lockers` | Bloomington IN | Project number needs confirmation. |

Fetch pattern:
`https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/<folder>/PROJECT_CARD.md`

Also fetch `OPEN_LOOPS.md` and `NOTES.md` when available.

---

## Known Contact

| Name | Role | Phone | Email |
|---|---|---|---|
| Cason Perez | Vecos USA primary contact | 832-993-6902 | Cason.Perez@vecos.com |

Site contacts vary by end-user location. See individual project cards.

---

## Dashboard Rule

- For live counts (today/tomorrow/this week/at-risk), call `GET https://interwork-command-center.vercel.app/api/ai/dashboard-summary`.
- For quick project, client, location, PM, or scope lookup, call `GET https://interwork-command-center.vercel.app/api/ai/search?q=<term>` — use search before scanning repo folders.
- Use project cards for scope, contacts, notes, history, and manually confirmed facts.
- If live API and project card conflict, flag the conflict — do not silently pick one.
- Knowledge packs and dashboard snapshots are fallback only.

---

## If You Cannot Fetch GitHub URLs

Say: "I cannot access the repo directly in this chat."
Ask Alejandro to paste the specific file, or ask Claude Code for a handoff.
Do not guess from old chat memory.

---

## Claude Code Handoff Format

```
Claude Code Handoff — Vecos [project / site]

New confirmed facts:
- [fact 1]

Update:
memory/clients/vecos/projects/<slug>/PROJECT_CARD.md
```

For IU Health: use `memory/clients/vecos_iu_health/projects/<slug>/PROJECT_CARD.md`

---

## Rules

- Do not invent project numbers, dates, contacts, or statuses.
- Do not scan unrelated clients.
- Vecos USA is the InterWork client — JPMC and IU Health are end-user sites, not InterWork clients.
- Do not send emails — draft only, Alejandro approves all sends.
- Do not write to Supabase without approval.
- Alejandro Acosta is the sole approval authority.
