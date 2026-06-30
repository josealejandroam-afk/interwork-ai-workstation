# Microsoft Graph Read-Only Workaround
_Last updated: 2026-06-29_
_Status: Active prototype — preferred workaround while IT-approved access is pending_

---

## Why This Exists

**Classic Outlook COM automation is blocked.** Only New Outlook (`olk.exe`) is installed
on this machine. New Outlook is a web wrapper and does not expose a COM interface.
The `outlook_ai_intake_export.ps1` script fails with "Class not registered."

**Playwright OWA scraping is held.** Automating Outlook Web through a browser session
depends on cookies/session state, is fragile to UI changes, and could be interpreted
as bypassing the approved Microsoft 365 access path. Not using this until explicitly
re-evaluated and approved.

**Microsoft Graph delegated read-only access is the correct workaround.**

---

## What This Is

A delegated (user-signed-in) read-only connection to Microsoft Graph API. The signed-in
user is `alejandroa@interworkoffice.com`. No admin credentials. No application-level
access to other users' data.

First login requires Alejandro to complete a device code sign-in (visit a URL, enter a
short code, click Allow). After that, the refresh token is stored locally and future
sessions run automatically without any human step.

---

## Permission Model

| Scope | What it allows |
|---|---|
| `User.Read` | Read the signed-in user's profile to verify identity |
| `Mail.Read` | Read the signed-in user's inbox and messages |
| `Calendars.Read` | Read the signed-in user's calendar events |
| `offline_access` | Maintain access via refresh token without re-login |

**Explicitly NOT requested:** Mail.ReadWrite, Mail.Send, Calendars.ReadWrite,
Files.Read.All, Sites.Read.All, ChannelMessage.Read.All, any admin/application permissions.

---

## What Stays Local (Never Committed)

| Data | Location | Committed? |
|---|---|---|
| MSAL token cache | `local_sources/graph_cache/` | NO — gitignored |
| Raw email results | `local_sources/graph_mail/` | NO — gitignored |
| Raw calendar results | `local_sources/graph_calendar/` | NO — gitignored |
| Sanitized project summaries | `memory/projects/project-XXXX.md` | YES — after review |

---

## Scripts

| Script | Purpose |
|---|---|
| `scripts/graph_readonly_setup_check.py` | Pre-flight check: Python, msal, gitignore. No auth. |
| `scripts/graph_mail_reader.py` | Search and read inbox. Device code auth. Read-only. |
| `scripts/graph_calendar_reader.py` | Read calendar events (next N days). Same auth. |

---

## Usage

### Pre-flight check (safe, no auth)
```powershell
python scripts/graph_readonly_setup_check.py
```

### First auth + mail dry-run
```powershell
python scripts/graph_mail_reader.py --dry-run --max-results 5
```
You will see a URL and a short code. Open the URL in any browser, enter the code,
sign in with `alejandroa@interworkoffice.com`, click Allow. The script completes
automatically. Subsequent runs use the cached token — no sign-in required.

### Search by project number
```powershell
python scripts/graph_mail_reader.py --project-number 7510 --query "7510 OR Pear OR Frank Barrett" --max-results 10
python scripts/graph_mail_reader.py --project-number 7189 --query "7189 OR Bermuda OR Hunter Barbieri" --max-results 10
```

### Read calendar (next 14 days)
```powershell
python scripts/graph_calendar_reader.py --days 14
python scripts/graph_calendar_reader.py --days 14 --dry-run
```

---

## Tenant Consent

If `alejandroa@interworkoffice.com` is on a tenant with strict conditional access
or admin-only consent policies, the first login may fail with:

| Error | Meaning |
|---|---|
| `AADSTS65001` | Admin consent required for all apps |
| `AADSTS700016` | App not found in tenant |
| `AADSTS50158` | Conditional access policy blocking device code flow |

If any of these occur, escalate to IT (VMX/Christian). The IT request draft is at
`docs/drafts/m365_access_request.md`. Request either:
- Claude Microsoft 365 connector (Claude Settings → Connectors), OR
- A registered Graph app with `Mail.Read + Calendars.Read + User.Read` delegated scopes

---

## Long-Term Path

This workaround is replaced when either of these is approved:
1. **Claude Microsoft 365 connector** — native Outlook/Teams/OneDrive integration
2. **IT-registered Microsoft Graph app** — same scopes, registered app client_id

Both require VMX/IT admin approval. The draft request is ready to send.
