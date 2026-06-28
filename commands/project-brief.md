# /project-brief

Generate a full project brief by layering three information tiers:
- **Supabase** — current operational state (canonical)
- **Memory / RAG** — historical context, decisions, past lessons
- **Outlook/M365 / Teams / Drive** — live signals from the last 7–14 days

Usage: `/project-brief PROJECT_NUMBER_OR_NAME`

---

## Information Tiers

### Tier 1 — Current State (Supabase, authoritative)
Query Supabase for the project record matching the number or name:
- Project number, name, client, location
- Status, phase, PM assigned
- Schedule: start date, key milestones, completion date
- Any confirmed field values (treat these as ground truth)

If no Supabase record exists: note it and do not invent one.
If a project number is ambiguous: stop and ask before proceeding.

### Tier 2 — Historical Context (Memory / RAG)
1. Check `memory/projects/project-{NUMBER}.md` if it exists — read it fully.
2. Run `/rag-search "{project name or number}"` for related decisions, lessons, and notes.
3. Surface:
   - Key decisions made and why
   - Past issues or delays and how they were resolved
   - Vendor or subcontractor history
   - Any recorded lessons learned

### Tier 3 — Live Signals (Outlook/M365, Teams, Drive)
Pull signals from the last 7–14 days:
- **Outlook/M365** (if Graph API authorized): search sent and received email for project number and client name — surface vendor updates, BOLs, WC reports, open questions. If M365 not authorized, note as integration gap and skip.
- **Teams** (if M365 MCP available): search chats and channels for project number mentions — surface open questions, waiting items
- **Drive** (if MCP available): list recently modified documents for this project

**Do not use Gmail for project signals.** Gmail is Alejandro's personal account. Work email is Outlook/M365 (`alejandroa@interworkoffice.com`). If M365 access is unavailable, note: "Integration gap: Outlook/M365 Graph API not authorized" and proceed with Teams + memory signals only.

For each signal: note sender/source, date, and what action (if any) is implied.

---

## Output Format

```
## Project Brief — [Project Number] [Project Name]
Generated: [date] | Sources: Supabase ✅ | Memory ✅/⚠️ | Outlook/M365 ✅/⚠️/❌ | Teams ✅/⚠️/❌

### Current State  (Supabase)
- Status: ...
- Phase: ...
- PM: ...
- Client: ...
- Location: ...
- Schedule: Start [date] → Completion [date]
- Milestones: ...

### Historical Context  (Memory / RAG)
- Key decisions: ...
- Past issues: ...
- Vendor/sub history: ...

### Live Signals  (last 14 days)
📧 Outlook/M365:
  - [sender] — [subject/summary] — [date] → Action: [what's implied]
  - (or: "Integration gap: Outlook/M365 Graph API not authorized — email signals unavailable")

💬 Teams:
  - [person] in [chat] — [summary] — [date] → Action: [what's implied]

📁 Drive:
  - [document name] — modified [date] by [person]

### Open Loops
- [ ] [item] — source: [outlook/teams/memory] — [date]

### Next Actions
1. [most urgent]
2. ...

### Conflicts / Flags
- [any field in a live signal that contradicts the Supabase record — do NOT overwrite without confirmation]
```

---

## Write Rules

- **Memory**: Always update `memory/projects/project-{NUMBER}.md` with new signals after generating the brief.
- **Open loops**: Any unanswered question or pending item goes to `open_loops/{source}_{date}_{slug}.md`.
- **Supabase**: If a live signal contains data that should update a Supabase field, flag it clearly in "Conflicts / Flags" and ask for confirmation before writing.
- **Smartsheet**: Never write. Read schedule data only.
- **Outlook / Teams**: Never send. Drafts are shown for approval.

See `memory/reference/interwork-command-center.md` for the full architecture and permission policy.
