# START HERE — InterWork AI Workstation

Every Claude session working on InterWork projects should read this folder first.

## Routing Model — Read Only What You Need

**Do not scan the entire repo.** Use the routing model:

1. Read the three required company knowledge files (below)
2. Identify the client from the Claude Project name or the message
3. Open only that client folder
4. Open only the named project folder if a project is specified
5. Use CLIENT_INDEX only if the client is unclear

See `REPO_LOOKUP_RULES.md` in this folder for the full routing flow with examples.

## Required Company Knowledge (always read these three)

1. `START_HERE.md` — this file (routing entry point)
2. `COMMUNICATION_RULES.md` — tone, format, message type rules
3. `ACCESS_AND_SAFETY_RULES.md` — what is blocked, what requires approval, what never goes in the repo

## Additional Company Knowledge (read when relevant)

- `REPO_LOOKUP_RULES.md` — how to navigate the repo without scanning everything
- `INTERWORK_OVERVIEW.md` — what the company does and what the AI is for
- `KEY_PEOPLE.md` — who is who at InterWork
- `OPERATING_WORKFLOW.md` — how a project moves from quote to closeout
- `GLOBAL_OPEN_LOOPS.md` — system-level unresolved items affecting all projects

## Client and Project Files (route to these, do not scan)

Client folder:
`memory/clients/<client_slug>/CLIENT_CONTEXT.md`

Project folder (if a project is specified):
`memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md`
`memory/clients/<client_slug>/projects/<project_slug>/OPEN_LOOPS.md`
`memory/clients/<client_slug>/projects/<project_slug>/DRAFTS.md`
`memory/clients/<client_slug>/projects/<project_slug>/NOTES.md`

## If Files Are Not Accessible

If you cannot access this folder or any file it references, do not guess.
Ask Alejandro to paste the relevant handoff or project card directly into the chat.

## What This System Is

This GitHub repo is the shared memory for all AI sessions working on InterWork projects.
Only Claude Code writes to it. Claude Chat, Claude Cowork, and ChatGPT read from it.

Claude Code is the only session with repo access, script execution, and Supabase write capability.

## Approval Authority

Alejandro Acosta is the sole approval authority for:
- Sending emails or Teams messages
- Writing to Supabase
- Any production action that cannot be undone

Do not take these actions without his explicit instruction.
