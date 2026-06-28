# /teams-brief

Summarize recent Microsoft Teams activity: important messages, project mentions, open questions, people waiting on a response, and suggested replies.

**IMPORTANT — read/summarize only. Never send a Teams message without explicit user approval. Sending is Level 3.**

---

## Architecture (priority order)

1. **Microsoft Graph via M365 MCP** — structured, fast, no browser needed
2. **Playwright → Teams web** — fallback when Graph cannot surface the info
3. **PS1 desktop scripts** — last resort for desktop app interaction

Teams is a structured knowledge source. Summaries get saved to project memory and linked to open loops.

---

## Step 1 — Microsoft Graph (primary)

Check whether Graph tools (beyond authenticate/complete_authentication) are available. They appear automatically after OAuth via `/mcp` → "claude.ai Microsoft 365".

If Graph tools are available:

```
1. List the user's Teams chats and joined channels (get unread counts).
2. For each conversation with recent activity (last 24–48 h):
   a. Fetch the last 20 messages.
   b. Extract:
      - Open questions directed at the user (ends with ?, "can you", "do you know")
      - Waiting-on signals ("let me know", "waiting on you", "please confirm", "any update")
      - Project/ticket number mentions (#XXXX, project names from memory)
      - Action items ("please", "can you", "need you to")
      - FYI / info-only messages
3. De-duplicate across chats.
4. Compile the brief (Output Format section below).
5. Save a summary entry to memory:
   - File: D:\ai-workstation\memory\open_loops\teams_pending.md
   - Include: sender, chat, message snippet, timestamp, action needed
```

---

## Step 2 — Playwright fallback (Teams web)

Use only when Graph tools are unavailable or cannot surface the needed content (e.g. file previews, rich cards).

```
1. Navigate to https://teams.microsoft.com
2. Snapshot to confirm auth state — stop and tell user if not logged in.
3. For each chat/channel with unread badge:
   a. Click to open → snapshot → read visible messages.
   b. Note sender, timestamp, content.
4. Use Teams search (Ctrl+E) for project keyword lookups.
5. Screenshots saved to C:\Users\Owner\AppData\Local\Temp\claude\teams-screenshots\
6. Compile the brief (Output Format section below).
```

---

## Step 3 — Desktop Teams PS1 scripts (last resort)

```powershell
# Bring Teams to front
powershell -File D:\ai-workstation\scripts\bring_teams_to_front.ps1

# Screenshot
powershell -File D:\ai-workstation\scripts\screenshot_screen.ps1

# Click at coordinates identified from screenshot
powershell -File D:\ai-workstation\scripts\click_at.ps1 -X <x> -Y <y>
```

Re-screenshot after each click to read the resulting content.

---

## Output Format

```
## Teams Brief — [date]

### Waiting on You
- **[Person]** in [Chat/Channel] — "[quote]" — [time]
  → Suggested reply: ...

### Open Questions
- **[Person]** asked: "[question]" — [Chat/Channel] — [time]

### Project Mentions
- [Project name / #] mentioned by [Person] in [Chat] — [summary]

### FYI / No Action
- [brief summary]

### Saved to Memory
- open_loops/teams_pending.md updated

### Source
- Graph API / Teams web / screenshot: [path or URL]
```

---

## Memory integration — unified open-loop queue

After generating a brief, write each pending item to the unified queue at:
`D:\ai-workstation\memory\open_loops\`

**One file per item.** Filename: `teams_{YYYY-MM-DD}_{slug}.md`

Each file uses this frontmatter (see `_template.md`):
```yaml
---
source: teams
project: [project name if known]
person: [sender name]
status: waiting          # or action-needed
created: [ISO timestamp]
updated: [ISO timestamp]
---
```

**Before creating a new file:** check for an existing `teams_*.md` file with the same `person` + `project` combination — update it instead of duplicating.

**When an item is resolved:** set `status: done` and update the `updated` field. Do not delete the file.

---

## Permissions

| Action | Level | Rule |
|--------|-------|------|
| Read messages | 1 — auto | Always allowed |
| Summarize / brief | 1 — auto | Always allowed |
| Draft a reply | 2 — show user | Show draft, wait for approval |
| Send a message | 3 — explicit | Must have "send it" instruction |
