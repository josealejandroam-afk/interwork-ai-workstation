# Do Not Touch — Hard Rules
_These apply in every session, every AI, every context._
_Last updated: 2026-06-29_

---

## Never Put in This Repo

- API keys, tokens, passwords, or service role keys
- Supabase connection strings or project URLs with embedded credentials
- Webhook URLs with embedded tokens or secrets
- Raw email bodies (paraphrase or summarize instead)
- Full private meeting transcripts (unless explicitly approved by Alejandro)
- Database exports or table dumps
- Credential files or `.env` file contents
- Vendor warehouse addresses, rates, or internal margins in client-facing files

---

## Never Do Without Alejandro Approval

- Send any email or Teams message
- Write to Supabase (INSERT, UPDATE, DELETE, schema changes, RLS, migrations)
- Change any project status field
- Set `vendor_confirmed`, `client_confirmed`, or `access_confirmed` on any project (NEVER auto-set)
- Set `fastfield_submitted`, `completion_report_sent`, or `actual_end_at`
- Write to Smartsheet (permanently read-only — no exceptions)
- Activate Make.com FastField scenario 5506328 before test payload is confirmed
- Enable RLS on Supabase before policies are written and reviewed

---

## Never Do At All

- Invent project numbers, contact names, or phone numbers
- Use Gmail (jose.alejandro.a.m@gmail.com) as a work project signal source
- Treat a ChatGPT recommendation as Alejandro approval — it is advisory only
- Commit `.env` files to git
- Print or log secret values in any output

---

## Drafting vs. Sending

| Action | Free | Requires Approval |
|--------|------|------------------|
| Write a draft email | ✅ | |
| Write a draft Teams message | ✅ | |
| Write a SQL proposal (without executing) | ✅ | |
| Send the email | | ✅ "send it" from Alejandro |
| Send the Teams message | | ✅ "send it" from Alejandro |
| Execute the SQL | | ✅ "approve" or "apply" from Alejandro |
