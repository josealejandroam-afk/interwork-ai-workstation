# Operating Workflow — InterWork Project Lifecycle

## Standard Sequence

```
1. Quote issued (QuickQuo)
   Project number assigned.
   Quote sent to client by account manager (e.g., Jill Buchman).

2. Project created in Smartsheet
   Scheduling entry added to the calendar.
   Supabase record created (often from Smartsheet sync).

3. PM and vendor assigned
   Office PM identified (administrative owner).
   Field PM identified (on-site execution lead).
   Vendor or crew confirmed if required.

4. Pre-execution confirmation
   Client confirmation obtained (client_confirmed).
   Building access confirmed (access_confirmed).
   Vendor/crew confirmed (vendor_confirmed).
   FastField prepared for field PM.
   Teams dispatch sent to field PM.
   Client confirmation email sent.
   Calendar entry created.

5. Execution
   Field PM submits FastField form on or after execution day.
   fastfield_submitted flips to true in Supabase (via Make.com webhook when active).

6. Closeout
   Work completion report (WC Report) generated from FastField data.
   Completion email sent to client with attached WC Report.
   Supabase status set to completed.
   actual_end_at populated.
```

## Tools Used

| Tool | Purpose | Access |
|---|---|---|
| QuickQuo | Quote generation and project number assignment | Manual — Alejandro/Jill |
| Smartsheet | Project calendar and scheduling source | Read-only for Claude — MCP re-auth pending |
| Supabase | Canonical project database | Claude reads live; writes require Alejandro approval |
| FastField | Field form submitted by on-site PM after execution | Manual only — no API |
| Make.com (scenario 5506328) | FastField → Supabase webhook bridge | Inactive — needs test payload before activating |
| Teams | PM dispatch and client coordination messages | Blocked for Claude — send manually |
| Outlook/M365 | Client emails, WC reports | Blocked for Claude — send manually |
| GitHub repo | Shared AI memory and project context | Claude Code reads/writes; other sessions read |
| Vercel dashboard | Live project status view | Read-only |

## Pre-Execution Site Confirmation Checklist

Before field work begins, confirm the following where applicable:

- [ ] Loading dock available at site?
- [ ] Liftgate required (if no dock)?
- [ ] Freight elevator available and reserved?
- [ ] COI requirements confirmed and COI submitted before dispatch?
- [ ] Union restrictions at this site?
- [ ] Building hours and after-hours access restrictions?
- [ ] On-site POC name and phone number confirmed?
- [ ] Crew check-in location confirmed?
- [ ] Parking or loading zone instructions provided?
- [ ] Floor protection required?
- [ ] Broom-clean or clean-condition required on departure?
- [ ] For decommissions: Jade notified for sustainability/donation coordination?
- [ ] E-waste disposal responsibility confirmed (COD or InterWork)?
- [ ] Cabling scope defined (IDF/MDF only; risers excluded unless explicitly included)?

Not all items apply to every project. Use as a reference for pre-execution review.

## Drafting vs. Sending

Claude can draft any document freely without approval.
Claude cannot send anything — email, Teams message, or Supabase write — without Alejandro's explicit instruction.

Trigger phrases:
- `"send it"` — send a prepared email or Teams message
- `"approve [item]"` or `"apply [item]"` — execute a Supabase write

## FastField Notes

FastField is the form the field PM completes on-site or after execution.
There is no REST API — it is a mobile form app.
Submission signals reach Supabase only through the Make.com webhook (currently inactive).
Until activated, fastfield_submitted must be updated manually.

## Confirmation Booleans (Supabase fields)

| Field | Meaning | Who sets it |
|---|---|---|
| client_confirmed | Client has confirmed the job date | Claude (with Alejandro approval) or Alejandro |
| vendor_confirmed | Vendor/crew has confirmed availability | Claude (with Alejandro approval) or Alejandro |
| access_confirmed | Building access is confirmed for execution day | Claude (with Alejandro approval) or Alejandro |
| fastfield_submitted | Field PM submitted FastField after execution | Make.com webhook (when active) or manual |
| completion_report_sent | WC report sent to client | Manual |

Never auto-set any confirmation boolean without explicit Alejandro approval.
