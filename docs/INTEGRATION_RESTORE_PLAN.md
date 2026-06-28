# Integration Restore Plan

Generated: 2026-06-28 12:38

Restore order: each step unlocks the next tier of commands.

## Step 1 -- Set Windows User Env Vars (manual, by Alejandro)

Set these in PowerShell (never paste values into chat):

    [System.Environment]::SetEnvironmentVariable('SUPABASE_URL', '<value>', 'User')
    [System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', '<value>', 'User')
    [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', '<value>', 'User')
    [System.Environment]::SetEnvironmentVariable('HF_TOKEN', '<value>', 'User')

After setting: restart Claude Code session so env vars are picked up.

Unlocks: /dashboard-status, /project-health, /completion-backlog, /completion-intake,
/ff-sent, /ask-openai-review

## Step 2 -- Supabase MCP (in Claude Code)

Project ID: hskgrxhdtgowagkfkjsw (interwork-command-center)
Connect via Claude Code MCP panel. No extra config needed beyond env vars.

Test: run /dashboard-status and confirm project counts return.

## Step 3 -- M365 / Outlook / Teams OAuth

Re-authorize via Claude Code MCP panel (Microsoft 365 connector).
Work email: alejandroa@interworkoffice.com
Personal email (Gmail): jose.alejandro.a.m@gmail.com -- personal only, not for project work

Unlocks: /teams-brief, /brief-me (full mode), /project-brief (Tier 3)

## Step 4 -- Read AI MCP

Read AI is visible in claude.ai app but not yet available as Claude Code CLI MCP.
Check Claude Code MCP connector list for Read AI availability.
Until connected: /meeting-intake and /readai-brief work in Mode B (manual paste).

## Step 5 -- FastField / Make Webhook

Webhook URL and token secret stored in: D:\ai-workstation\scripts\fastfield_webhook_config.txt
If file not present (migrated from C: archive): recreate manually in Make.com.
Scenario ID: 5506328 | Webhook name: FastField Completed Submission | Hook ID: 2508004
Scenario was inactive on laptop -- activate only after test payload confirmed.

Unlocks: /fastfield-intake (full mode)

## Step 6 -- Smartsheet MCP

Re-authorize via Claude Code MCP panel.
RULE: Read-only. Never write to Smartsheet.
Unlocks: /brief-me Smartsheet source

## Step 7 -- Migrate feedback_loop/ from C: Archive

Source: C:\Users\Owner\.claude\feedback_loop\ (do not delete archive yet)
Target: D:\ai-workstation\feedback_loop\
Copy files manually; verify content before use with /ask-openai-review.

## Approval Rules (never changes)

Always requires Alejandro explicit approval:
- Any Supabase INSERT, UPDATE, DELETE
- Status field changes on projects
- vendor_confirmed / client_confirmed / access_confirmed updates
- Sending Outlook emails or Teams messages
- RLS policy changes
- Any Smartsheet write
- Deleting production data

Claude may do automatically:
- Read-only queries and status reports
- Memory/RAG writes and local file updates
- Review-only SQL drafts
- Script/doc/config updates inside D:\ai-workstation
