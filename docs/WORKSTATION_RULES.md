# Workstation Operating Rules

These rules govern how Claude interacts with tools, data, and external systems on this workstation.

---

## 1. Role Separation

| Component | Role |
|-----------|------|
| **Claude** | Operations engine — executes tasks, writes code, manages files, calls tools |
| **Dashboard / UI** | Interface only — display and input, not the source of truth |
| **Supabase** | Canonical write target for structured data |
| **Smartsheet** | Read-only — never write to Smartsheet unless Alejandro explicitly approves |
| **Memory / RAG** | Stores history, decisions, procedures, and lessons learned — not live data |

---

## 2. Data Integrity

- **Supabase is the write target.** All structured data that needs to persist goes to Supabase, not to local files or dashboards.
- **Do not overwrite confirmed fields silently.** If a field has been confirmed correct, flag the conflict before overwriting — never silently replace it.
- **No project status updates without a confirmed project number and explicit approval.** Status is high-stakes; always verify the project identifier before writing.
- **Smartsheet is read-only.** Use it to read data only. Do not push updates unless instructed.

---

## 3. Memory and RAG

Memory and RAG are for:
- Lessons learned from past sessions
- Approved procedures and runbooks
- Decision records (what was decided and why)
- Historical context that should persist across sessions

Memory and RAG are **not** for:
- Live project status (use Supabase)
- Real-time field values
- Secrets or credentials of any kind

---

## 4. Secrets

See `docs/SECRETS_POLICY.md` for the full policy.

Summary:
- Secrets are **local per machine** and never committed to git
- Each machine has its own `.env` — never share `.env` across machines
- No API keys, tokens, or service keys in any committed file

---

## 5. External Actions

**All external actions require Alejandro's explicit approval before execution**, including:
- Sending messages (email, Slack, Teams)
- Posting or updating records in external systems
- Publishing content
- Modifying shared infrastructure
- Triggering webhooks

Claude may prepare the action, confirm the details, and wait — but never fire without approval.

---

## 6. Change Safety

- Never silently mutate confirmed data
- Never delete without explicit instruction
- Never push to remote without instruction
- When in doubt, report and wait

---

*Last updated: 2026-06-28*
