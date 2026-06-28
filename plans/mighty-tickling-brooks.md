# Plan: Teams Read/Navigation Capability + /teams-brief Command

## Context
Alejandro wants Teams integrated as a structured knowledge source — not just a browser tab. The goal is to read, search, and summarize Teams chats/channels using Microsoft Graph (primary), Playwright (fallback), and desktop PS1 scripts (last resort). A `/teams-brief` command will surface unread messages, open questions, project mentions, and suggested replies.

## What's Already Done
- `C:\Users\1\scripts\bring_teams_to_front.ps1` — brings Teams desktop window to foreground
- `C:\Users\1\scripts\screenshot_screen.ps1` — captures full screen to a PNG
- `C:\Users\1\scripts\click_at.ps1` — clicks at X,Y coordinates
- `C:\Users\1\.claude\commands\teams-brief.md` — `/teams-brief` skill with Graph → Playwright → PS1 priority chain, output format, and memory integration spec

## Remaining Steps

### 1. M365 MCP Authentication (user action)
User must run `/mcp` in Claude Code and select **"claude.ai Microsoft 365"**.  
This unlocks Graph tools (beyond the two auth stubs already loaded).

### 2. Verify Graph Tools for Teams
After auth, call available Graph tools to confirm they can:
- List the user's Teams chats and channels
- Fetch recent messages per conversation
- Search messages by keyword

If Teams messages are accessible via Graph → done; Playwright fallback is only used for edge cases.

### 3. Create Memory File for Pending Teams Items
Create `C:\Users\1\.claude\projects\C--Users-1\memory\open_loops\teams_pending.md`  
Format: one checkbox line per pending item from Teams.  
Update MEMORY.md index to point to it.

### 4. Update MEMORY.md
Add an entry under **Procedures** pointing to the teams-brief command and the teams_pending memory file.

## Verification
1. Run `/teams-brief` — it should attempt Graph first, then Playwright if Graph unavailable.
2. Confirm output matches the defined format (Waiting on You / Open Questions / Project Mentions / FYI).
3. Confirm `teams_pending.md` is updated after the brief.
4. Confirm no messages are sent without explicit approval.

## Permission Boundary
- Reading/summarizing Teams: auto-allowed (Level 1)
- Drafting replies: show user first (Level 2)  
- Sending messages: requires explicit "send it" (Level 3)
