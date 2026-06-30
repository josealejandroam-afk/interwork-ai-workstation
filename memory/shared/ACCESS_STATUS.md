# Access & Integration Status
_Last updated: 2026-06-29_

---

| System | Account | Status | Used For | Blocked On | Next Step |
|--------|---------|--------|----------|------------|-----------|
| **GitHub** | josealejandroam-afk | ✅ Connected | Shared AI memory, repo commits, version control | — | In use |
| **Supabase** | interwork-command-center | ✅ Read-only confirmed | Canonical project DB (140 projects) | Writes require Alejandro approval | Approve held batch to test first write flow |
| **Smartsheet** | alejandroa@interworkoffice.com | ⚠️ MCP re-auth pending | Schedule/planning source only — never write | MCP session expired | Re-auth in Claude Code MCP panel |
| **Outlook / M365** | alejandroa@interworkoffice.com | 🚫 Blocked — company-controlled. Do not retry. | Work email signals, WC reports, FF assignment detection | Tenant admin consent required for ALL apps (confirmed 2026-06-30). Classic Outlook COM also unavailable (New Outlook only). | Wait for VMX/IT or Gal to approve a company-sanctioned path. Do not request again. |
| **Teams** | alejandroa@interworkoffice.com | 🚫 Blocked — same as Outlook | Project mentions, unread messages, pending replies | Same tenant policy | Same as above |
| **Microsoft Graph API** | alejandroa@interworkoffice.com | 🚫 Blocked — admin consent required | Programmatic mail/calendar read | Tenant requires admin approval for all apps incl. Microsoft's own Graph tools (confirmed 2026-06-30) | Do not retry. Unblocked only if VMX/IT or Gal explicitly approves. |
| **Playwright OWA** | — | 🚫 Blocked — safety rule | Browser-based Outlook automation | Held: fragile, policy bypass risk | Not an approved workaround. Do not use. |
| **Read AI** | (unknown account) | ❌ CLI auth incomplete | Meeting summaries, action items | MCP CLI auth | OAuth via /mcp or API key |
| **FastField** | (no API) | ❌ Manual only | Work completion forms; submission signals | No REST API exists | Make.com webhook is the path; needs one test payload first |
| **Make.com** | Scenario 5506328 | ⚠️ Inactive | FastField → Supabase webhook bridge | Test payload not yet confirmed | Send test FF submission, confirm lands in fastfield_webhook_events, then activate |
| **Gmail** | jose.alejandro.a.m@gmail.com | ⚠️ Personal only | NOT used for work | Wrong inbox for work | Do not use for InterWork project signals |
| **Vercel** | interwork-command-center.vercel.app | ✅ Live | Dashboard frontend | — | Read-only; writes go through Supabase |

---

## M365 Access — Status (confirmed 2026-06-30)

**ALL M365/Outlook/Graph access is blocked by tenant admin policy. Do not retry.**

Tested 2026-06-30: Microsoft "Approval required" screen appeared for Microsoft Graph
Command Line Tools (Microsoft's own verified app). Tenant requires admin consent for
every application without exception.

**Current access state:**

| Path | Status |
|------|--------|
| Classic Outlook COM | Unavailable — New Outlook (olk.exe) only; no COM interface |
| Microsoft Graph PowerShell | Blocked — tenant admin consent required |
| Microsoft Graph API (Python MSAL) | Blocked — same policy |
| Playwright OWA scraping | Blocked — safety rule, not an approved path |
| Claude M365 connector | Blocked — requires VMX/IT admin approval |
| Microsoft Graph MCP connector | Blocked — requires VMX/IT admin approval |

**To unblock:** VMX/IT (Christian) or Gal must explicitly approve a company-sanctioned
path. Do not request, pressure, or follow up. Wait for them to initiate.

**Draft IT request on file:** `docs/drafts/m365_access_request.md` — do not resend without Alejandro instruction.

---

## Integration Unlock Priority Order

```
1. ✅ Env vars set (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY)
2. ✅ Supabase read confirmed (2026-06-28)
3. ⏳ 6-project batch approval → first Supabase write test
4. ❌ M365 access → send IT request to Christian (VMX) → unlocks Teams + Outlook + WC report parser + FF assignment detection
5. ❌ Smartsheet MCP re-auth → schedule rows readable
6. ❌ Read AI MCP auth → meeting summary auto-ingest
7. ❌ FastField webhook test → confirm Make.com scenario 5506328 before activating
```
