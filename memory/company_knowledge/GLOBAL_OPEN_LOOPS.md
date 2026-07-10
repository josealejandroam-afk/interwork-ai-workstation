# Global Open Loops — System Level

These are cross-client, infrastructure-level items that are unresolved and affect the full AI workstation.
Project-specific open loops live in the relevant project folder.

---

## Blocked — Waiting on Company Approval

| Loop | Status | What is needed |
|---|---|---|
| Outlook / M365 access (alejandroa@interworkoffice.com) | Blocked — company IT policy | VMX/IT (Christian) or Gal must explicitly approve a company-sanctioned connector or registered app |
| Microsoft Graph API / PowerShell | Blocked — same tenant policy | Same as above — confirmed with Microsoft's own tools on 2026-06-30 |
| Teams read access | Blocked — same policy | Same as above |
| Classic Outlook COM | Unavailable | New Outlook (olk.exe) only — no path here regardless of approval |

Draft IT access request is on file at `docs/drafts/m365_access_request.md`.
Do not resend without Alejandro instruction. Do not follow up on this.

---

## Inactive / Pending Test

| Loop | Status | Next step |
|---|---|---|
| Make.com scenario 5506328 (FastField webhook) | Inactive | Send one test FastField submission; confirm it lands in fastfield_webhook_events table; then activate |
| Smartsheet MCP re-auth | Pending | Re-auth in Claude Code MCP panel when ready |
| Read AI MCP auth | Incomplete | OAuth via /mcp or API key header |

---

## Supabase / Data Health

| Loop | Status | Notes |
|---|---|---|
| Batch status update: 7374, 7499, 7498, 7472, 7482 → completed | Held | Trigger phrase: "approve batch complete 6" (scope now 5 projects — 7347 removed 2026-07-10, see below) |
| 7347 MMA McLean Consolidation — Wilmington Zoom Room AV recovery | Open, not held | Full AV system left behind at former McLean office; recovery visit planned week of 7/13. Was in the batch above until a 2026-07-10 handoff surfaced this — see `memory/clients/marsh_mclennan/projects/7347_mma_mclean_consolidation/`. Do not mark completed. |
| Project 7447 — null out invalid actual_end_at | Held | Trigger phrase: "apply 7447 fix" |
| 48 past-dated projects with status=scheduled | Pending | Status backfill needed — creates noise in health view |
| v_project_health date calibration | Pending | SQL not yet drafted — false proximity alerts for past-dated records |
| RLS policies for Supabase | Held | Do not enable until policies are written and reviewed |
| communications table | Empty | Blocked on M365 OAuth |

---

## Scheduling — TBD-Dated Projects (from Smartsheet calendar read 2026-07-09)

| Loop | Location | PM | Next step |
|---|---|---|---|
| 7589 INNOVARE — Furniture Install (Acrisure, job #25793-F) | Miami Lakes, FL | Hunter Barbieri | Awaiting labor quote from Craig Bohres/Epic Office Installations; call scheduled. Items shipping direct to site, expected week of 7/13. Location corrected 2026-07-10 from "MN" per Outlook thread "7589 - Miami Lakes Labor request/quote" + Innovare quote-request doc (job 25793-F, install address 15050 NW 79th Court Suite 200, Miami Lakes FL 33016) — MN may have referred to a different Innovare job; flag to Alejandro if MN was a separate real job that also needs tracking. |
| 7593 Amtrust — Chair Move | Jersey City NJ | — | Confirm date on Smartsheet |
| 7541 Antidefamation League — Conference setup | — | — | Confirm date on Smartsheet |
| 7556 MMA — Art Work Hanging | Dallas TX | — | Confirm date on Smartsheet |
| 7549 Kensington Vanguard (KV) — Indianapolis Relocation | Indianapolis IN | Danielle Stingone (Lincoln Property Company, supporting KV) | Move 8/1, FDOB 8/3, crates delivered (increased to 10). Client corrected 2026-07-10 from "CRC" — that was a mislabel; confirmed client is Kensington Vanguard, unrelated to the CRC Group Tampa project (7537). See `memory/clients/kensington_vanguard/projects/7549_indianapolis_relocation/`. |

Full read on file at `memory/shared/CALENDAR_SNAPSHOT.md` (2026-07-09 snapshot).

---

## System / Memory

| Loop | Status | Notes |
|---|---|---|
| GitHub memory upkeep | Ongoing | After each major session, regenerate handoffs and commit |
| C:\\Users\\Owner\\.claude archive | Held | Do not delete — keep until fully operational on D: |
| Teams one-way alerts (Workflows) | Not tested | Inbound Teams Workflow → Claude pipeline not yet built |
