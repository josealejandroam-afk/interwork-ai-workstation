# Microsoft Graph Read-Only Workaround
_Last updated: 2026-06-30_
_Status: BLOCKED — pending company-approved access. Do not retry._

---

## Decision (2026-06-30)

**Microsoft Graph mailbox/calendar access is blocked. Do not pursue further without explicit company approval.**

The M365 tenant (interworkoffice.com) requires admin consent for ALL applications,
including Microsoft's own "Microsoft Graph Command Line Tools." This is a company
IT policy, not a technical limitation. It is not to be worked around.

**Do not:**
- Retry Graph API auth attempts
- Request approval again or follow up with IT
- Try alternate client IDs (first-party or otherwise)
- Use Playwright or browser automation to access OWA
- Scrape Outlook Web in any form
- Attempt to bypass admin consent through unofficial methods

If VMX/IT or Gal explicitly approves a company-sanctioned path, this status will be
updated at that time and only at that time.

---

## What Was Tested (2026-06-30)

| Attempt | Result |
|---|---|
| Classic Outlook COM (`outlook_ai_intake_export.ps1`) | Failed — only New Outlook (olk.exe) installed, no COM interface |
| Microsoft Graph PowerShell module (`graph_powershell_readonly_test.ps1`) | Hit Microsoft "Approval required" admin consent screen — blocked by tenant policy |
| Python MSAL device code flow (`graph_mail_reader.py`) | Not completed — stopped after PowerShell path confirmed the block |
| Playwright OWA scraping | Held by safety rule — not attempted |

**No tokens, auth cache, or email data were saved.** All test runs failed before any
data was written locally.

---

## What Is Needed to Unblock

The IT admin (Christian at VMX) or Gal must approve one of these:

| Path | What to approve |
|---|---|
| Claude Microsoft 365 connector | In Claude Settings → Connectors → Microsoft 365; requires M365 admin approval |
| Registered Azure AD app | Custom app registration with Mail.Read + Calendars.Read delegated scopes |
| Microsoft Graph PowerShell | Approve "Microsoft Graph Command Line Tools" service principal in Entra admin center |

IT request draft: `docs/drafts/m365_access_request.md`

---

## Current Access Status

- **Outlook/M365 email:** Blocked — admin approval required
- **Calendar:** Blocked — same
- **Teams read:** Blocked — same
- **Classic Outlook COM:** Unavailable — New Outlook only, no COM
- **Playwright OWA:** Blocked by safety rule
- **Microsoft Graph API:** Blocked — tenant admin consent required

---

## Scripts in This Repo (kept for when access is approved)

| Script | Purpose | Status |
|---|---|---|
| `scripts/graph_readonly_setup_check.py` | Pre-flight check; no auth | Safe to run |
| `scripts/graph_mail_reader.py` | Python MSAL mail reader | Kept; needs registered app client_id from IT |
| `scripts/graph_calendar_reader.py` | Python MSAL calendar reader | Kept; same |
| `scripts/graph_powershell_readonly_test.ps1` | PowerShell Graph module reader | Kept; needs tenant admin approval |
| `scripts/outlook_ai_intake_export.ps1` | Classic Outlook COM export | Kept; needs Classic Outlook installed |

These scripts are retained in the repo so they are ready when approval arrives.
They are not to be run again until access is approved.
