# Dashboard Field Map
_Maps dashboard columns and status values to their meanings_
_Last updated: 2026-06-30_

---

## Column Definitions

| Dashboard Column | Description | Notes |
|---|---|---|
| **Project #** | Unique numeric project identifier assigned by InterWork | Format: 4-digit integer (e.g. 7553). Source of truth is Supabase `projects.project_number`. |
| **Client / Location** | Client name and site address | May be combined in one display column. Includes city when available. |
| **Type** | Project type classification | See Project Types below. |
| **Date / Time** | Scheduled execution date and start time | Format: M/D/YY–M/D/YY for date range; HH:MM AM/PM for time. Time may be omitted if unconfirmed. |
| **Execution Owner** | Person responsible for executing the work on-site | May be an InterWork PM (e.g. Juan Martinez, Melvin Hernandez, Frank Barrett) or "External PM" for third-party leads. |
| **Status** | Current workflow state of the project | See Status Values below. |
| **Readiness** | Whether the project is operationally ready to execute | See Readiness Values below. |
| **Alerts** | Count of projects needing attention | Includes at-risk, missing PM, stale scheduled, and other flags. |
| **Today** | Projects with execution date = today | Filter tab on dashboard. |
| **Tomorrow** | Projects with execution date = tomorrow | Filter tab on dashboard. |
| **This Week** | Projects with execution date within the current calendar week | Filter tab on dashboard. |
| **All** | All active projects regardless of date | Default dashboard view. |

---

## Project Types

| Type | Meaning |
|---|---|
| Relocation | Moving furniture/equipment within or between sites |
| Decom | Decommissioning — removal and disposal of furniture/equipment |
| Install | Installing new furniture or equipment |
| Delivery | Delivering items to a site without full install |
| Walkthrough | Site walkthrough or assessment, no physical work |
| Punchlist | Follow-up items from a prior project |
| Storage | Items moved to or retrieved from storage |
| Internal Relocation | Internal move within the same building or suite |

---

## Status Values

| Status | Meaning | Notes |
|---|---|---|
| **Scheduled** | Project has a confirmed date and is on the calendar | Does not guarantee readiness. |
| **In Progress** | Execution is currently underway | Set on execution day. |
| **Completed** | Work is done; may still need paperwork (FastField, WC) | Needs completion signal confirmation. |
| **Pending Approval** | Awaiting client or internal sign-off before proceeding | Block until approval received. |
| **On Hold** | Temporarily paused; reason should be in notes | Do not reschedule without checking hold reason. |
| **Cancelled** | Project will not proceed | May still appear in historical data. |
| **Needs confirmation** | Status is unresolved or unclear | _Used in this doc when exact logic is unknown._ |

---

## Readiness Values

| Readiness | Meaning | Notes |
|---|---|---|
| **Ready** | All required fields confirmed: date, PM, access, scope | Safe to execute. |
| **At Risk** | One or more required fields missing or unconfirmed | Needs follow-up before execution. Commonly: missing PM, unconfirmed access, incomplete scope. |

> **Note:** Exact readiness calculation logic (which fields trigger At Risk) is not fully documented.
> **Needs confirmation** from Supabase/dashboard logic review.

---

## Alert Logic

| Alert Type | Trigger | Notes |
|---|---|---|
| At Risk | Readiness = At Risk | Most common alert. |
| Missing PM | Execution Owner is blank or "TBD" | **Needs confirmation** — exact field name in Supabase. |
| Stale Scheduled | Status = Scheduled but date is past | **Needs confirmation** — exact staleness threshold unknown. |
| No FastField | Project is completed/past-dated but fastfield_submitted = false | **Needs confirmation** — may not be a live dashboard alert. |

---

## Filter Tabs

| Tab | Supabase logic (inferred) | Confirmed? |
|---|---|---|
| Today | `execution_date = CURRENT_DATE` | **Needs confirmation** |
| Tomorrow | `execution_date = CURRENT_DATE + 1` | **Needs confirmation** |
| This Week | `execution_date BETWEEN start_of_week AND end_of_week` | **Needs confirmation** |
| All | No date filter; status IN ('Scheduled', 'In Progress', 'Pending Approval', 'On Hold') | **Needs confirmation** |
| Alerts | Readiness = At Risk OR missing PM OR stale scheduled | **Needs confirmation** |

---

## Notes

- Field names above are human-readable dashboard labels. Actual Supabase column names may differ.
- See `memory/references/interwork_command_center_schema.md` for the full Supabase schema.
- Where logic is marked **Needs confirmation**, verify against the dashboard source code or Supabase view definitions before relying on them.
