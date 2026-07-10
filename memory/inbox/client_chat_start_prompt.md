# Client Chat Start Prompt
_Reusable prompt for starting a Claude Chat session focused on a specific InterWork client or project_
_Last updated: 2026-06-30 (bootstrap model update)_

---

## Architecture Note — Bootstrap / AI Index / Repo / Pack

**Preferred model (current):**

```
Bootstrap file (uploaded once to Claude Project)
        ↓ tells Claude Chat: here is the repo + index URLs
memory/ai_index/START_HERE_FOR_AI.md  ← fetch this first
        ↓ navigates to
CLIENT_ROSTER.md → PROJECT_INDEX.md → exact PROJECT_CARD.md
```

1. Upload `claude_project_bootstraps/<client_slug>_bootstrap.md` to each Claude Project (once).
2. At session start, bootstrap says: fetch `memory/ai_index/START_HERE_FOR_AI.md`.
3. From there, navigate to the specific client/project files.
4. The GitHub repo is the source of truth — all changing facts live there.

**Fallback model (when URL fetch unavailable):**
Full knowledge packs in `claude_project_packs/` are available but stale.
Use packs only when URL fetch is completely unavailable.
Check the `Generated:` date — packs go stale within days.

**If URL fetch fails completely:**
Say so clearly. Ask Alejandro to paste the specific file or route to Claude Code for a handoff.
Do NOT use an uploaded pack as if it were current.

**Access priority:**
1. Live Supabase / Vercel API (future — Phase 2)
2. Raw GitHub URLs: `memory/ai_index/` and `memory/clients/`
3. Uploaded knowledge pack (fallback only)

**The key principle:**
> The uploaded Claude Project file is a map, not the territory.
> The GitHub repo is the territory. The AI index is the fast-lookup layer on top of it.

See `docs/CLAUDE_PROJECT_BOOTSTRAP_MODEL.md` and `docs/HANDS_EYES_EARS_MODEL.md` for full architecture.

---

## How to Use

This prompt is for sessions where a bootstrap is not yet uploaded, or as a manual override.
Do not paste this as a "read everything" list — the prompt tells Claude to route, not scan.

Replace `<client>` with the actual client name (e.g. Radian, MMC, Bentley).
Replace `<project number or name>` with the project if known, or omit it.

If you are starting a general InterWork session (not client-specific), use:
`memory/inbox/claude_chat_start_handoff.md` instead.

---

## Prompt — For Claude Project Instructions (paste into Project settings)

```
This Claude Project is client-specific for InterWork Office Solutions.

At the start of each chat:

0. Source of truth orientation — read this first:

   The uploaded bootstrap file (or this prompt) is a map, not the territory.
   The GitHub repo is the source of truth for all changing project facts.

   If a bootstrap is uploaded to this project, follow its fetch instructions.
   If no bootstrap is uploaded, follow the steps below.

   Before answering any operational status question, fetch the dashboard snapshot:
   https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/dashboard/CURRENT_DASHBOARD_STATUS.md

   Use it for: project counts, today/tomorrow/this week counts, at-risk counts, today's row detail.
   If the snapshot "Last Updated" is more than 1 day old, warn it may be stale.

   After checking the snapshot, fetch:
   1. The client context from the repo (not from an uploaded pack)
   2. The relevant project card from the repo
   3. Open loops for that project from the repo

   If URL fetch is unavailable: say so clearly, then ask Alejandro to paste the specific repo file.
   Do not rely on an uploaded pack as if it were current — packs go stale.

   If the dashboard snapshot conflicts with a project card, flag the conflict.
   Do not silently pick one source over the other.

1. Fetch and read these three files for general InterWork rules:
   https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/START_HERE.md
   https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/COMMUNICATION_RULES.md
   https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md

2. Infer the client from this Claude Project name.
   Example: "Radian Projects" means use memory/clients/radian/.
   Example: "MMC Projects" means use memory/clients/marsh_mclennan/.
   Example: "Bentley Projects" means use memory/clients/bentley_systems/.

3. Fetch and read only that client folder:
   https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/memory/clients/<client_slug>/CLIENT_CONTEXT.md

4. When a project number, project name, address, or scope clue is provided,
   fetch only that project's files inside:
   memory/clients/<client_slug>/projects/

5. If the project folder exists, read only:
   PROJECT_CARD.md, OPEN_LOOPS.md, DRAFTS.md, NOTES.md

6. If no matching project folder exists:
   - Do not search unrelated clients
   - Do not guess
   - Draft a proposed project card stub
   - Tell me to have Claude Code create the folder

7. Do not scan unrelated clients or the whole repo unless I ask for a cross-client search.

8. Do not trust old chat memory over the current project card.

Rules:
- Do not invent project numbers, PMs, dates, contacts, or statuses
- Do not send emails or Teams messages without Alejandro saying "send it"
- Do not write to Supabase without Alejandro saying "approve" or "apply"
- Alejandro Acosta is the sole approval authority for all sends and writes
- If there is a conflict between sources, say what conflicts and ask for confirmation
```

---

## Routing Reference — Raw GitHub URLs

Base URL: `https://raw.githubusercontent.com/josealejandroam-afk/interwork-ai-workstation/main/`

| File | URL suffix |
|---|---|
| START_HERE | memory/company_knowledge/START_HERE.md |
| COMMUNICATION_RULES | memory/company_knowledge/COMMUNICATION_RULES.md |
| ACCESS_AND_SAFETY_RULES | memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md |
| REPO_LOOKUP_RULES | memory/company_knowledge/REPO_LOOKUP_RULES.md |
| CLIENT_INDEX | memory/clients/CLIENT_INDEX.md |
| Radian context | memory/clients/radian/CLIENT_CONTEXT.md |
| MMC context | memory/clients/marsh_mclennan/CLIENT_CONTEXT.md |
| Bentley context | memory/clients/bentley_systems/CLIENT_CONTEXT.md |
| Vecos context | memory/clients/vecos/CLIENT_CONTEXT.md |
| Pear VC context | memory/clients/pear_vc/CLIENT_CONTEXT.md |
| Radian 7492 card | memory/clients/radian/projects/7492_radian_denver_decom/PROJECT_CARD.md |
| MMC 7189 card | memory/clients/marsh_mclennan/projects/7189_mmc_bermuda_hoboken/PROJECT_CARD.md |

---

## Available Client Folders

| Client | Folder slug |
|---|---|
| Marsh McLennan (MMC / MMA) | marsh_mclennan |
| Bentley Systems | bentley_systems |
| Vecos USA | vecos |
| Pear VC | pear_vc |
| Radian | radian |
| TierPoint | tierpoint |
| Dropbox | dropbox |
| McGriff (MMA/MMC subsidiary — no separate folder, confirmed 2026-07-10) | marsh_mclennan |
| Rothman Orthopaedics | rothman_orthopaedics |
| Strategic Education | strategic_education |
| AmTrust Financial | amtrust |
| Claritev / MultiPlan | claritev_multiplan |
| Ingersoll Rand | ingersoll_rand |
| FAA Eastern Region | faa_eastern_region |

See `memory/clients/CLIENT_INDEX.md` for the full list.
