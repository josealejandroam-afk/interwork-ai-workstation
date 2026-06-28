# /brief-me

Generate a morning briefing from all connected data sources and write it to `C:\Users\1\today.md`.

## Instructions

### 1. Open Loops (from unified queue)
Read all `.md` files in `C:\Users\1\.claude\projects\C--Users-1\memory\open_loops\`
- Skip `_template.md` and files with `status: done`
- Parse frontmatter: `source`, `project`, `person`, `status`
- Group by source with counts: 💬 Teams (N) | 📧 Outlook (N) | 📊 Smartsheet (N) | 📝 Manual (N)
- List top 5 by `action-needed` status first, then `waiting`

### 2. Fresh data (pull live if tools available)
In priority order, call what's connected:
- **M365 MCP / Graph** → recent Teams messages + Outlook sent/received email; run `/teams-brief` logic inline. If not authorized: note "Integration gap: Outlook/M365 Graph API not authorized" and skip — do not force permission.
- **Gmail MCP** → personal account only; skip for work items. Do not use Gmail as a project signal source.
- **Smartsheet MCP** → sheets with recent changes or assigned rows
- If none available, note which sources are offline

For each new pending item found: write a new open-loop file to `open_loops/` using the standard format (`_template.md`). Check for duplicates before creating (match on source + person + project).

### 3. Recent memory updates
List memory files modified in the last 7 days (use file system or git log).

### 4. Suggested next actions
Based on open loops and project memory, propose 3–5 concrete next steps. Prioritize `action-needed` items over `waiting`.

### 5. System status
Quick check: disk space, any background processes of note.

---

## Output — write to `C:\Users\1\today.md` then print summary

```
## Morning Brief — [Day], [Date]

### Open Loops  (X total — Y need action)
💬 Teams (N) | 📧 Outlook (N) | 📊 Smartsheet (N) | 📝 Manual (N)

**Action-needed:**
- [Person] — [summary] — [source] — [age]
  Action: ...

**Waiting:**
- ...

### New Items Found This Run
- [N new open loops added to queue]

### Recent Memory Updates
- [file] — [what changed] — [N days ago]

### Suggested Next Actions
1. ...
2. ...
3. ...

### System Status
- Disk: X GB free
- Background tasks: none / [list]
```

---

## Permission boundary
- Reading and summarizing: auto-allowed
- Drafting replies: show user, wait for approval
- Sending anything: requires explicit "send it"
