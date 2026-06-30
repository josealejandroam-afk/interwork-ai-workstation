# Repo Lookup Rules for Claude Chat
_Last updated: 2026-06-30_

The repo is public only so Claude Chat can read current InterWork memory. Do not browse the entire repo by default.

---

## Lookup Flow

### Step 1 — Always read company knowledge first

```
memory/company_knowledge/START_HERE.md
memory/company_knowledge/COMMUNICATION_RULES.md
memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md
```

These three files give general InterWork awareness. Read them before answering any project question.

### Step 2 — Determine the client

If the Claude Project name identifies the client, use that client directly.

| Claude Project name | Client folder |
|---|---|
| Radian Projects | memory/clients/radian/ |
| MMC Projects | memory/clients/marsh_mclennan/ |
| Bentley Projects | memory/clients/bentley_systems/ |
| Vecos Projects | memory/clients/vecos/ |
| Pear VC Projects | memory/clients/pear_vc/ |
| McGriff Projects | memory/clients/mcgriff/ |
| Dropbox Projects | memory/clients/dropbox/ |

If the client is not clear from the project name or the user's message, use `memory/clients/CLIENT_INDEX.md` to look it up. CLIENT_INDEX is a fallback — not a default starting point.

### Step 3 — Open only that client folder

```
memory/clients/<client_slug>/CLIENT_CONTEXT.md
```

Do not open other client folders unless explicitly asked.

### Step 4 — Locate the project

If Alejandro provides a project number, name, address, location, or scope clue, search only inside:

```
memory/clients/<client_slug>/projects/
```

### Step 5 — If the project folder exists, read only

```
PROJECT_CARD.md
OPEN_LOOPS.md
DRAFTS.md
NOTES.md
```

Do not read unrelated project folders.

### Step 6 — If no matching project folder exists

- Do not search unrelated clients
- Do not guess
- Draft a proposed project card stub
- Ask Alejandro to have Claude Code create the project folder

### Step 7 — Use CLIENT_INDEX only when client is unclear

`memory/clients/CLIENT_INDEX.md` is a fallback lookup. Use it when the client cannot be determined from the Claude Project name or the message.

### Step 8 — Use broader/global files only if

- The client is unknown after checking the Claude Project name and the message
- The project is not found in the client folder
- Alejandro asks for a cross-client view
- There is a conflict that needs checking across clients

### Step 9 — Never treat old chat memory as more reliable than the project card

If anything in this session's chat history conflicts with the project card, say what conflicts and use the project card as the source of truth.

### Step 10 — If repo facts and Alejandro's current message conflict

- Say what conflicts
- Treat Alejandro's current message as the newest source
- Recommend updating the project card through Claude Code

---

## Client-Specific Claude Project Startup Rule

When a chat starts inside a client-specific Claude Project, infer the client from the project name and go directly to that client folder. Do not read every client. Do not scan every project folder. Use the client folder as the main source of truth.

---

## Examples

**Example 1 — Radian project 7492**
```
Claude Project: Radian Projects
Read:
  memory/company_knowledge/START_HERE.md
  memory/company_knowledge/COMMUNICATION_RULES.md
  memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md
  memory/clients/radian/CLIENT_CONTEXT.md
Project 7492 mentioned:
  memory/clients/radian/projects/7492_radian_denver_decom/PROJECT_CARD.md
  memory/clients/radian/projects/7492_radian_denver_decom/OPEN_LOOPS.md
  memory/clients/radian/projects/7492_radian_denver_decom/DRAFTS.md
  memory/clients/radian/projects/7492_radian_denver_decom/NOTES.md
Do NOT load 7510, 7189, or 7350.
```

**Example 2 — MMC project 7189**
```
Claude Project: MMC Projects
Read:
  memory/company_knowledge/START_HERE.md
  memory/company_knowledge/COMMUNICATION_RULES.md
  memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md
  memory/clients/marsh_mclennan/CLIENT_CONTEXT.md
Project 7189 mentioned:
  memory/clients/marsh_mclennan/projects/7189_mmc_bermuda_hoboken/PROJECT_CARD.md
  memory/clients/marsh_mclennan/projects/7189_mmc_bermuda_hoboken/OPEN_LOOPS.md
  memory/clients/marsh_mclennan/projects/7189_mmc_bermuda_hoboken/DRAFTS.md
  memory/clients/marsh_mclennan/projects/7189_mmc_bermuda_hoboken/NOTES.md
Do NOT load 7521, 7060, or any other MMC project unless asked.
```

**Example 3 — Bentley, no project specified yet**
```
Claude Project: Bentley Projects
Read:
  memory/company_knowledge/START_HERE.md
  memory/company_knowledge/COMMUNICATION_RULES.md
  memory/company_knowledge/ACCESS_AND_SAFETY_RULES.md
  memory/clients/bentley_systems/CLIENT_CONTEXT.md
Wait for Alejandro to name a project before opening any project folder.
```

---

## What Not To Do

- Do not scan every client folder on startup
- Do not load every project for a client unless asked
- Do not pull in projects from unrelated clients because they are upcoming or globally relevant
- Do not invent project numbers, PMs, or status
- Do not treat old chat memory as more reliable than current project cards
