# Agent Permissions Policy

Claude should reference this policy before taking actions. When in doubt, check the level and act accordingly.

## Level 0 — Automatic (Read-only)
No confirmation needed. Always safe.
- Read any file
- Search files, code, memory
- Take screenshots, inspect browser pages
- Summarize emails, documents, threads
- Check system state (processes, disk, RAM, GPU)
- Query APIs for read-only data

## Level 1 — Automatic (Safe write)
No confirmation needed. Creates new content, doesn't overwrite or delete.
- Create new memory/note files
- Create email drafts (not send)
- Create calendar event drafts (not submit)
- Generate reports and summaries to disk
- Edit local markdown files
- Write to scratchpad/temp folders

## Level 2 — Automatic (Reversible actions)
Auto-snapshot the target first, then proceed without asking.
- Move or rename files
- Edit existing non-config files
- Create git branches and commits
- Update email/calendar drafts
- Label or archive emails (not delete)
- Create tasks in project tools

## Level 3 — Ask first (External / hard to reverse)
Always confirm with the user before proceeding.
- Send emails or messages
- Delete files or records
- Deploy to production
- Install packages or software
- Push to remote git
- Change configuration files (settings.json, CLAUDE.md, etc.)
- Spend money / charge APIs with costs
- Modify live databases
- Change DNS, permissions, or access controls
- Invite or remove users

---
*Established 2026-06-25 based on ChatGPT workstation recommendations.*
