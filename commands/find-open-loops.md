# /find-open-loops

Read every open-loop file in `memory/open_loops/` and surface unfinished items grouped by source and urgency.

## Instructions

1. Read all `.md` files in `D:\ai-workstation\memory\open_loops\`
   - Skip `_template.md`
   - Skip files with `status: done`

2. Parse the frontmatter fields from each file:
   - `source` (teams | outlook | smartsheet | browser | manual)
   - `project`
   - `person`
   - `status` (waiting | action-needed | blocked)
   - `created` / `updated`
   - Body: summary and action-needed

3. Group first by **urgency**:
   - **Action-needed** — status is `action-needed` (ball is in Alejandro's court)
   - **Waiting** — status is `waiting` (waiting on someone else)
   - **Blocked** — status is `blocked` (needs more info or external dependency)

4. Within each urgency group, sub-group by **source** using emoji labels:
   - 💬 Teams
   - 📧 Outlook/M365
   - 📊 Smartsheet
   - 🌐 Browser
   - 📝 Manual

5. Output format:

```
## Open Loops — [date]

### Action-Needed
💬 **Teams** | [Project] | [Person] — [summary] — [age]
  Action: [what to do]
  File: open_loops/filename.md

📧 **Outlook/M365** | ...

### Waiting
...

### Blocked
...

Total: X action-needed, Y waiting, Z blocked
```

6. After listing, offer:
   - "Mark any as done?" → update `status: done` and `updated:` in the file
   - "Draft a reply?" → compose and show for approval before any send
