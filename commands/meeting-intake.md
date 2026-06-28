# /meeting-intake

Deep intake for a single meeting. Saves a meeting note to memory, proposes open
loops, and re-indexes RAG. Never modifies project data or sends messages.

Usage:
  Mode A (live MCP):   `/meeting-intake <MEETING_ULID>`
  Mode B (no MCP):     `/meeting-intake --paste`  then paste content when prompted
                       `/meeting-intake --file <path>`  to read from a file

---

## Mode detection

If a ULID is provided: try `get_meeting_by_id`. If it succeeds → Mode A.
If it errors or MCP is unavailable → announce Mode B, prompt for pasted content.

If `--paste` or `--file` is given: go directly to Mode B.

---

## Mode A — Live Read AI MCP

### Step 1 — Fetch meeting

```
get_meeting_by_id(
  id=<ULID>,
  expand=["summary","action_items","key_questions","topics"]
)
```

**Transcript rule:** Do NOT request `transcript` unless:
- Alejandro explicitly asks for it, OR
- Both `summary` and `action_items` return empty or clearly insufficient

If transcript is pulled: note it in output as "Transcript: pulled (user-requested)" or
"Transcript: pulled (summary insufficient)".

---

## Mode B — Manual input

Accept any of the following:

| Source | What to do |
|--------|-----------|
| `--paste` | Prompt: "Paste the meeting content and press Enter twice when done" |
| `--file <path>` | Read the file at path; accept .txt, .md, .json, .csv |
| Read AI email | Parse subject → title, body → summary + action items + questions |
| Raw transcript | Extract speakers, topics, action items, decisions |

Parse to extract:
- `meeting_id`: use filename, email Message-ID, or generate `manual-<YYYYMMDD>-<slug>`
- `title`, `date`, `participants`, `duration`
- `summary`, `topics`, `action_items`, `key_questions`
- Note source type in memory file

---

## Shared steps (both modes)

### Step 2 — Project matching

Priority order:
1. **Project number** in title, notes, or attendee context → high confidence
2. **Client name / location / date** fuzzy match → medium confidence
3. **Participant email domain** → medium/low confidence
4. **Name similarity only** → low confidence

```sql
SELECT id, project_number, name, status, scheduled_date
FROM public.projects
WHERE status NOT IN ('completed','closed','cancelled')
  AND (
      name ILIKE '%<keyword>%'
      OR project_number = '<number>'
  );
```

### Step 3 — Save meeting note to memory

#### If project matched → append to project memory file

File: `memory/projects/project-<NUMBER>.md`

```markdown
## Meeting — <Title> — <Date>
Source: Read AI [Mode A / Mode B: <input type>] | ID: <meeting_id>
Participants: <names>
Match confidence: high / medium / low

**Summary:** <summary>

**Topics:** <topics>

**Action Items:**
- [ ] <item> — <person> — due: <date or unspecified>

**Key Questions:**
- <question>

**Flags:** <anything needing attention>
```

#### If unmatched → save to open_loops as unmatched reference

File: `memory/open_loops/readai_unmatched_<YYYYMMDD>_<slug>.md`

```markdown
---
id: readai-<YYYYMMDD>-<NNN>
source: readai
project:
person:
status: action-needed
priority: medium
created: <datetime>
updated: <datetime>
meeting_id: <id>
meeting_title: <title>
match_confidence: none
---

# Unmatched Meeting — <title> — <date>

<summary>

**Action Items:**
- <items>

**Key Questions:**
- <questions>

Note: No Supabase project match found. Review and link manually if applicable.
```

### Step 4 — Propose open loops

For each action item and each unanswered key question, draft an open loop entry.

Write to `memory/open_loops/readai_<YYYYMMDD>_<slug>.md`:

```markdown
---
id: readai-<YYYYMMDD>-<NNN>
source: readai
project: <project_number or blank>
person: <assigned person or blank>
status: open
priority: medium        # high if deadline ≤7 days
created: <datetime>
updated: <datetime>
meeting_id: <id>
meeting_title: <title>
match_confidence: high/medium/low/none
next_action: <what needs to happen>
---

<action item or question text>
```

**Do not insert to Supabase `open_loops` table without Alejandro approval.**
Write the `.md` file automatically (Level 1). Propose Supabase INSERT as a separate draft.

### Step 5 — Re-index RAG

```
uv run python D:\ai-workstation\rag\ingest.py
```

Confirm: `N new chunks indexed`.

---

## Output format

```
## Meeting Intake — <Title>
ID: <id> | Date: <datetime> | Mode: A (live MCP) / B (<input type>)
Participants: <names>
Project match: #<XXXX> <name> — confidence: high/medium/low | unmatched

### Summary
<summary>

### Topics
<topics>

### Action Items
- [ ] <item> — <person> — due: <date>

### Key Questions (open)
- <question>

### Transcript pulled: yes / no / not applicable

---

### Memory saved
✅ memory/projects/project-<NUMBER>.md  (or readai_unmatched_...)
✅ open loop files written: N

### RAG re-indexed
✅ N new chunks indexed — total: N

### Proposed Open Loops (memory .md files written above)
| Loop | Project | Priority | Next Action |
|------|---------|----------|-------------|
| <action> | #XXXX | medium | <what to do> |

### Proposed Supabase inserts (not applied — require approval)
> Say "insert open loops to Supabase" to get the INSERT SQL for review.
- open_loops: N rows ready

### Proposed Supabase project updates (not applied — require approval)
> These require explicit confirmation before any write.
- None identified / [list if meeting content implies a field update]

### Flags
- [anything needing attention]
```

---

## Rules

- Read AI is read-only — Mode A and Mode B are intake only
- Do not write to Smartsheet
- Do not change Supabase project fields without approval
- Do not change confirmed fields (vendor_confirmed, client_confirmed, access_confirmed)
- Do not send emails or Teams messages
- Memory writes (`memory/`) happen automatically — no approval needed
- Supabase `open_loops` inserts and project updates require Alejandro approval
- Log any approved Supabase writes to `activity_log` with `actor='claude'`, `source='readai'`
- See `memory/references/interwork-command-center.md` for full permission policy
