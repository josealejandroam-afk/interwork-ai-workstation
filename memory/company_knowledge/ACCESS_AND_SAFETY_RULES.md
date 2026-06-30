# Access and Safety Rules

## Never Put in This Repo

- API keys, tokens, passwords, service role keys
- Supabase connection strings or project URLs with embedded credentials
- Webhook URLs with embedded tokens or secrets
- Raw email bodies — paraphrase or summarize only
- Full private meeting transcripts unless explicitly approved by Alejandro
- Database exports or table dumps
- Credential files or .env file contents
- Vendor warehouse addresses, rates, or internal margins in client-facing files

## Never Do Without Alejandro Approval

- Send any email or Teams message
- Write to Supabase (INSERT, UPDATE, DELETE, schema changes)
- Change any project status field
- Set vendor_confirmed, client_confirmed, or access_confirmed on any project
- Set fastfield_submitted, completion_report_sent, or actual_end_at
- Write to Smartsheet — permanently read-only, no exceptions
- Activate Make.com FastField scenario 5506328 before test payload is confirmed
- Enable RLS on Supabase before policies are written and reviewed

## Never Do At All

- Invent project numbers, contact names, or phone numbers
- Use Gmail (jose.alejandro.a.m@gmail.com) as a work project signal source
- Treat a ChatGPT recommendation as Alejandro approval — it is advisory only
- Commit .env files to git
- Print or log secret values in any output

## Blocked Integrations (do not retry)

| System | Status | Reason |
|---|---|---|
| Outlook / M365 | Blocked — company-controlled | Tenant requires admin consent for all apps (confirmed 2026-06-30) |
| Microsoft Graph API | Blocked | Same tenant policy — confirmed with Microsoft's own Graph tool |
| Microsoft Graph PowerShell | Blocked | Same policy |
| Classic Outlook COM | Unavailable | New Outlook (olk.exe) only — no COM interface registered |
| Playwright OWA scraping | Blocked | Safety rule — browser automation of Outlook Web is not an approved path |
| Claude M365 connector | Blocked | Requires VMX/IT admin approval |
| Microsoft Graph MCP | Blocked | Requires VMX/IT admin approval |
| Teams read access | Blocked | Same as Outlook — same tenant policy |

**To unblock any M365 path:** VMX/IT (Christian) or Gal must explicitly approve a company-sanctioned path. Do not request, pressure, or follow up. Wait for them to initiate.

Do not suggest alternate Microsoft client IDs or browser automation as workarounds.

## Email Intake

Until company-approved M365 access is granted:
- Email intake is manual — Alejandro pastes or summarizes email content
- No automated email reading, parsing, or routing
- Do not attempt to access Outlook Web through any automated path

## Drafts vs. Sends

| Action | Free | Requires Approval |
|---|---|---|
| Write a draft email | Yes | |
| Write a draft Teams message | Yes | |
| Write a SQL proposal (without executing) | Yes | |
| Send the email | | "send it" from Alejandro |
| Send the Teams message | | "send it" from Alejandro |
| Execute the SQL | | "approve" or "apply" from Alejandro |

## Source: DO_NOT_TOUCH.md

Full hard-stop rules are also maintained in `memory/shared/DO_NOT_TOUCH.md`.
That file takes precedence if there is any conflict with this one.
