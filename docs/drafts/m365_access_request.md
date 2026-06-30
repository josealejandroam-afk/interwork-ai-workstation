# DRAFT — M365 Access Request to VMX/IT
_Status: DRAFT — do not send without Alejandro review and "send it"_
_Created: 2026-06-29_

---

**To:** Christian [VMX/IT — last name unknown; confirm before sending]
**From:** Alejandro Acosta
**Subject:** Request: Claude Microsoft 365 Connector Approval

---

Hi Christian,

I checked the Outlook app store, but the Outlook add-ins do not appear to be the right path for Claude access.

What we likely need is approval for the Claude Microsoft 365 connector, or an approved Microsoft Graph read-only connection, so Claude can search and summarize project-related information from my InterWork mailbox and calendar.

**Requested access:**
- Outlook mailbox read/search for alejandroa@interworkoffice.com
- Calendar read access
- Read-only only where possible
- No ability to send, delete, archive, move, or modify emails without approval
- No production writes
- No bypassing company controls

**Business purpose:**
This would support project coordination, client/vendor follow-up tracking, meeting/action item review, and operational reporting.

Please let me know what approval path VMX prefers for this.

Thank you,
Alejandro

---

## Background (for reference — not part of the email)

**Option 1 — Claude Microsoft 365 connector**
- Native connector inside Claude Settings → Connectors → Microsoft 365
- Covers: Outlook, Teams, OneDrive, SharePoint
- Access model: read-only, follows existing M365 user permissions
- Requires: admin approval in Microsoft 365 admin center or equivalent

**Option 2 — Microsoft Graph MCP connector**
- IT-approved OAuth application with delegated (user-level) scopes
- Minimum scopes to request: Mail.Read, Calendars.Read, User.Read, offline_access
- Optional later: Files.Read.All, Sites.Read.All, ChannelMessage.Read.All
- Start with Mail.Read and Calendars.Read only

**Do NOT install:** AI MailMaestro, Ghostwriter, R2 Copilot, Sapling, Leah for Outlook — these are third-party Outlook add-ins, not the Claude access path.
