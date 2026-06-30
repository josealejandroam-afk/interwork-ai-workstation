# Outlook Local Workaround — AI Intake Folder
_Last updated: 2026-06-29_
_Status: Active temporary workaround — pending Claude M365 connector or Microsoft Graph approval_

---

## What This Is

A local-only workflow that lets Alejandro manually place relevant Outlook emails into a controlled folder, then lets Claude read and summarize them without needing the Claude Microsoft 365 connector or IT-approved Graph access.

**This is temporary.** The clean long-term path is the Claude Microsoft 365 connector or a Microsoft Graph MCP connector with admin approval. This workaround gets useful email context into project memory now, without waiting for IT.

---

## Why Not the Outlook Add-In Store

The Outlook add-in store contains productivity add-ins that run inside Outlook — they do not give Claude access to the mailbox. They are not the right path.

The correct paths are:
1. **Claude Microsoft 365 connector** — Claude Settings → Connectors → Microsoft 365 (requires VMX/IT admin approval)
2. **Microsoft Graph MCP connector** — IT-approved OAuth app with `Mail.Read` + `Calendars.Read` scopes
3. **This local workaround** — manual folder export, read-only, no connector needed

---

## How It Works

```
Outlook (stays the source)
    │
    │  You search and manually drag/copy relevant emails
    ▼
"AI Intake" folder in Outlook
    │
    │  outlook_ai_intake_export.ps1 reads metadata + sanitized body
    ▼
local_sources/outlook_summaries/  ←── gitignored, stays local
    │
    │  Claude reads summaries, extracts facts
    ▼
memory/projects/project-XXXX.md  ←── sanitized facts committed to GitHub
```

**What stays local (never committed):** raw email bodies, .msg files, .eml files, full headers, attachment contents
**What gets committed:** sanitized summaries (subject, sender, date, key facts extracted by Claude)

---

## Setup — One Time

### Step 1: Create the "AI Intake" folder in Outlook

1. Open Classic Outlook (not New Outlook — COM automation requires Classic)
2. Right-click your mailbox → New Folder
3. Name it exactly: `AI Intake`
4. Place it at the top level of the mailbox, not inside another folder

### Step 2: Local folders (created automatically by script, gitignored)

```
D:\ai-workstation\local_sources\outlook_ai_intake\
D:\ai-workstation\local_sources\outlook_exports\
D:\ai-workstation\local_sources\outlook_summaries\
```

---

## Day-to-Day Workflow

### For any project:

1. **In Outlook:** Search by project number or client name:
   ```
   7189 OR Bermuda OR Hoboken
   7510 OR Pear OR Townsend
   7304 OR Montebello
   Frank Barrett
   Pedro Martinez
   ```

2. **Drag relevant emails** into the `AI Intake` folder in Outlook. Do not move originals — copy or drag from search results.

3. **Tell Claude:**
   ```
   Run the Outlook AI Intake export for project 7189 in dry-run first.
   Read-only only. Do not modify emails.
   ```

4. **If dry-run looks good:**
   ```
   Run the Outlook AI Intake export for project 7189.
   Summarize results into memory/projects/project-7189.md.
   Do not commit raw emails.
   ```

---

## Script

**File:** `scripts/outlook_ai_intake_export.ps1`

**What it does:**
- Connects to Classic Outlook via COM automation (read-only)
- Reads the `AI Intake` folder (or a specified folder name)
- Exports: subject, sender, date, recipients, attachment names, sanitized body preview
- Writes sanitized summary files to `local_sources/outlook_summaries/`
- Does NOT send, delete, move, archive, flag, or modify any message
- Supports `-DryRun` flag to preview without writing anything
- Supports `-ProjectNumber` to tag output files

**Test command (dry-run only — no files written):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\outlook_ai_intake_export.ps1 -FolderName "AI Intake" -ProjectNumber "7189" -DryRun
```

**Full run (writes summaries to local_sources/):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\outlook_ai_intake_export.ps1 -FolderName "AI Intake" -ProjectNumber "7189"
```

---

## Manual Fallback (if Classic Outlook COM is unavailable)

If the script exits with "Classic Outlook COM not available" (e.g., you're using New Outlook):

1. In Outlook, search by project number or client name
2. Select relevant emails
3. File → Save As → save as `.msg` or `.eml` into:
   ```
   D:\ai-workstation\local_sources\outlook_exports\project_7189\
   ```
4. Tell Claude:
   ```
   Read the .msg files in local_sources/outlook_exports/project_7189/ and summarize
   what is relevant to project 7189. Do not commit the raw files.
   ```

Claude can read `.msg` and `.eml` files locally. Raw files stay gitignored.

---

## Safety Rules

- Raw email bodies never go to GitHub
- `.msg`, `.eml`, `.pst`, `.ost`, `.mbox` files are gitignored
- `local_sources/` is gitignored
- Only sanitized summaries (subject, sender, date, key facts) are committed
- The script never sends, deletes, moves, archives, flags, or modifies any email
- Claude never sends emails from this workflow
- Supabase writes from email-derived data still require Alejandro approval

---

## Limitations

- Requires **Classic Outlook** (not New Outlook) for COM automation
- Manual step: Alejandro must search and move emails to `AI Intake` folder
- No real-time push — pull only, when Alejandro initiates
- Attachment contents are not read (filenames only)

---

## Long-Term Path

This workaround is replaced when either of these is approved:
1. **Claude Microsoft 365 connector** — Claude Settings → Connectors → Microsoft 365
2. **Microsoft Graph MCP** — IT-approved OAuth with Mail.Read + Calendars.Read

IT request draft: `docs/drafts/m365_access_request.md`
