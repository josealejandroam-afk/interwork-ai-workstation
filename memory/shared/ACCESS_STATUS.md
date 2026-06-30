# Access & Integration Status
_Last updated: 2026-06-29_

---

| System | Account | Status | Used For | Blocked On | Next Step |
|--------|---------|--------|----------|------------|-----------|
| **GitHub** | josealejandroam-afk | ✅ Connected | Shared AI memory, repo commits, version control | — | In use |
| **Supabase** | interwork-command-center | ✅ Read-only confirmed | Canonical project DB (140 projects) | Writes require Alejandro approval | Approve held batch to test first write flow |
| **Smartsheet** | alejandroa@interworkoffice.com | ⚠️ MCP re-auth pending | Schedule/planning source only — never write | MCP session expired | Re-auth in Claude Code MCP panel |
| **Outlook / M365** | alejandroa@interworkoffice.com | ❌ Blocked — admin approval needed | Work email signals, WC reports, FF assignment detection | Claude M365 connector OR Microsoft Graph MCP requires VMX/IT approval | Send draft request to Christian (VMX/IT) — draft in `docs/drafts/m365_access_request.md` |
| **Teams** | alejandroa@interworkoffice.com | ❌ Blocked — same as Outlook | Project mentions, unread messages, pending replies | Same approval needed | Same as above |
| **Read AI** | (unknown account) | ❌ CLI auth incomplete | Meeting summaries, action items | MCP CLI auth | OAuth via /mcp or API key |
| **FastField** | (no API) | ❌ Manual only | Work completion forms; submission signals | No REST API exists | Make.com webhook is the path; needs one test payload first |
| **Make.com** | Scenario 5506328 | ⚠️ Inactive | FastField → Supabase webhook bridge | Test payload not yet confirmed | Send test FF submission, confirm lands in fastfield_webhook_events, then activate |
| **Gmail** | jose.alejandro.a.m@gmail.com | ⚠️ Personal only | NOT used for work | Wrong inbox for work | Do not use for InterWork project signals |
| **Vercel** | interwork-command-center.vercel.app | ✅ Live | Dashboard frontend | — | Read-only; writes go through Supabase |

---

## M365 Access — Correct Path (confirmed 2026-06-29)

The Outlook add-in store is NOT the right path. Those are productivity add-ins that run inside Outlook — they do not give Claude access to the mailbox.

**Two valid paths:**

| Path | What it is | Status | Notes |
|------|-----------|--------|-------|
| Claude Microsoft 365 connector | Native connector in Claude Settings → Connectors | Requires VMX/IT admin approval | Read-only; follows existing M365 permissions; covers Outlook, Teams, OneDrive, SharePoint |
| Microsoft Graph MCP connector | IT-approved OAuth app with delegated scopes | Requires VMX/IT admin approval | Request scopes: Mail.Read, Calendars.Read, User.Read, offline_access |

**Do not install:** AI MailMaestro, Ghostwriter, R2 Copilot, Sapling, Leah for Outlook — these are third-party add-ins, not the Claude access path.

**Draft IT request:** `docs/drafts/m365_access_request.md` — send to Christian (VMX/IT).

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
