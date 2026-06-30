# START HERE — InterWork AI Workstation

Every Claude session working on InterWork projects should read this folder first.

## Reading Order

1. `START_HERE.md` — this file
2. `INTERWORK_OVERVIEW.md` — what the company does and what the AI is for
3. `KEY_PEOPLE.md` — who is who at InterWork
4. `OPERATING_WORKFLOW.md` — how a project moves from quote to closeout
5. `COMMUNICATION_RULES.md` — tone, format, and what to include in every message type
6. `ACCESS_AND_SAFETY_RULES.md` — what is blocked, what requires approval, what never goes in the repo
7. `GLOBAL_OPEN_LOOPS.md` — system-level unresolved items affecting all projects

Then read the client folder:
`memory/clients/<client_slug>/CLIENT_CONTEXT.md`

Then read the project folder if applicable:
`memory/clients/<client_slug>/projects/<project_slug>/PROJECT_CARD.md`

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
