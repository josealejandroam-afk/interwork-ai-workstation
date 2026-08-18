# Module 3 — Systems and Sources of Truth
These are the human-operated business systems — the tools you'll actually log into. The AI/repo layer built on top of them is Module 4, deliberately kept separate.

_Sources used: `memory/company_knowledge/OPERATING_WORKFLOW.md` ("Tools Used" table), `docs/EXTERNAL_INTEGRATION_GATES.md` and `docs/DASHBOARD_URL.md` (verified against current state — see the note at the bottom on what's stale in those source docs)._

## The systems

| System | What it's for | Who touches it | Write access |
|---|---|---|---|
| **QuickQuo** | Quote generation and project number assignment | Account manager, coordinators | Manual entry |
| **Smartsheet** | Project calendar and scheduling — the schedule of record | Coordinators, PMs | Normal read/write for staff. (A separate, permanent rule blocks any AI tool from ever writing to it — covered in Module 4, not a constraint on you as a person.) |
| **Supabase** | The canonical operational database — current status, confirmation flags, dates | Coordinators (via the dashboard or approved write paths) | Status/field changes go through the approved write process, not ad hoc |
| **Command Center dashboard** | `https://interwork-command-center.vercel.app/` — the user-facing view of Supabase | Everyone, as a read tool day one | Read-only unless a write action is explicitly approved |
| **FastField** | The field form the Field PM submits after execution | Field PM | No API — it's a mobile form, submitted directly by the person on-site |
| **Make.com (FastField → Supabase bridge)** | Automatically flips `fastfield_submitted` when a form comes in | Nobody directly — it's a background bridge | Currently inactive; until it's active, that flag is set manually |

## Why the dashboard and Supabase aren't "two sources"

The Command Center dashboard is a **view into Supabase**, not an independent database. When you look something up on the dashboard, you're looking at Supabase data through a browser. If the dashboard and Supabase ever seem to disagree, that's a display or caching issue to flag — not two competing facts to reconcile.

## Why Smartsheet is reference, not truth

Smartsheet is where a job first gets scheduled, and it's genuinely useful for a calendar view. But once a project exists in Supabase, **Supabase is the operational truth** — statuses, confirmation flags, and dates live there. Smartsheet can drift out of sync with what's actually confirmed. Use it to see what's coming up; verify anything you're about to act on against Supabase/the dashboard.

## Confirmation fields — what they mean and who sets them

| Field | Meaning |
|---|---|
| `client_confirmed` | The client has confirmed the job date |
| `vendor_confirmed` | The vendor/crew has confirmed availability |
| `access_confirmed` | Building access is confirmed for execution day |
| `fastfield_submitted` | The Field PM submitted FastField after execution |
| `completion_report_sent` | The WC report was sent to the client |

These are never set on assumption — only on direct evidence (an email, a call, a confirmed form). This is true for you as a person using these systems directly, independent of any AI-assisted write process (which has its own, stricter approval rule — Module 4).

## A note on what's current vs. stale in the source docs

`docs/EXTERNAL_INTEGRATION_GATES.md` describes some of these systems' *AI-connector* status (e.g. whether Claude's Smartsheet MCP is reauthorized) — that document is about the AI layer, not about whether you, a person, can log into Smartsheet normally. Don't read that file as a statement about your own access; Module 4 covers what it actually means for the AI tools, with the current (not stale) status.

## Knowledge Check

No formal check for this module — the real test is using these systems correctly during Module 5's guided practice. Before moving to Module 4, be able to answer: if the dashboard shows a project as "scheduled" but you know the client just confirmed a date change over the phone, which one do you trust, and what do you do next?
