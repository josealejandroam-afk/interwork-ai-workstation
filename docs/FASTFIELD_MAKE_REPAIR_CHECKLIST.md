# FastField → Make → Supabase Repair Checklist
**Created:** 2026-06-28  
**Status:** PARTIAL — webhook channel open, rows arriving empty  
**Scope:** Local instructions only. No Make changes, no Supabase writes, no test trigger performed here.

---

## Schema Pre-Check (Completed — Read-Only)

`fastfield_webhook_events` confirmed in Supabase. Relevant columns:

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| `id` | uuid | NO | uuid_generate_v4() |
| `received_at` | timestamptz | NO | now() |
| `source` | text | NO | 'fastfield' |
| `form_name` | text | YES | null |
| `submission_id` | text | YES | null |
| `project_number_detected` | text | YES | null |
| `submitter_name` | text | YES | null |
| `submitted_at` | timestamptz | YES | null |
| `raw_payload` | **jsonb** | NO | '{}' |
| `processed` | boolean | NO | false |
| `processing_status` | text | NO | 'pending' |
| `matched_project_id` | uuid | YES | null |
| `matched_project_confidence` | text | YES | null |
| `error_message` | text | YES | null |

**No schema blocker.** `raw_payload` exists and is `jsonb` with default `'{}'`.  
The four shell rows from 2026-06-26 have `raw_payload = '{}'` (empty object) — not null, but empty.  
All parsed columns (`form_name`, `submission_id`, `submitter_name`, `submitted_at`) are nullable and currently null on all rows.

---

## Architecture Clarification (From Local Docs)

**Parsing does NOT belong in Make.**

Per `/fastfield-intake` command and `memory/references/fastfield_make_integration.md`:

- Make's only job: receive the webhook, write one row to `fastfield_webhook_events` with `source`, `received_at`, and the full incoming object in `raw_payload`.
- The `/fastfield-intake` command (downstream processor) reads `raw_payload`, extracts fields, and proposes project matches.
- `form_name`, `submitter_name`, `project_number_detected` etc. are **downstream-derived** — Make does not need to populate them.
- `project_number_detected` is explicitly a downstream field unless the FastField payload contains an authoritative project number key at the top level.

**The only field Make must get right is `raw_payload`.** The current rows have `raw_payload = '{}'`, which means either:
  - (a) Make is not mapping `raw_payload` to anything, so the jsonb default `'{}'` is being used, or
  - (b) Make is mapping to a path that resolves to an empty object

This is the repair target.

---

## Step 1 — Open the June 26 Execution History

1. Go to Make.com → Scenarios → open **scenario 5506328** (FastField Submission Intake)
2. Click **History** (top-right or left sidebar depending on Make version)
3. Find any of the four executions from **2026-06-26 around 23:04–23:08 UTC** (these are the known-good triggers — webhook was received, row was inserted)
4. Open one execution. You should see a module-by-module run log.

---

## Step 2 — Inspect Module 1: Incoming Webhook Bundle

Open the first module (the webhook trigger — "FastField Completed Submission", Hook ID 2508004).

In the output bundle panel, you will see a structured object. **Record only key names and nesting structure — do not copy values, payload content, personal data, URLs, or tokens.**

You are looking for:

**A. What is the top-level structure?**

Common FastField webhook shapes (only one will be correct — observe, do not guess):

```
Option A — flat body:
  { id, form_name, submitted_at, submitted_by, fields: [...], ... }

Option B — nested under "body":
  { body: { id, form_name, ... }, headers: {...}, method: "POST", query: {...} }

Option C — nested under "data":
  { data: { id, form_name, ... }, ... }

Option D — other nesting
  (record whatever key name sits above the submission content)
```

**B. What key name contains the full FastField submission object?**

This is the key you will map to `raw_payload`. It might be the entire bundle root, or it might be one level down (e.g., `body`, `data`, `payload`, `submission`).

**C. Is there an explicit `token` or `query` key at the root?**

Note it exists (yes/no) — this is the token filter key, not part of the payload. Do not record its value.

---

## Step 3 — Mapping Decision Tree for `raw_payload`

After observing the bundle structure in Step 2, apply this decision:

### Case A: Submission data is at the top level of the bundle (no nesting)

The entire output of the webhook module IS the submission. Map `raw_payload` to:
```
{{1}}
```
(where `1` is the module number of the webhook trigger — confirm the actual number in Make's UI)

In Make's Supabase/HTTP module body field for `raw_payload`, use the **mapping picker** to select the entire output object of module 1. This serializes as JSON automatically for a jsonb column if Make's Supabase integration handles it natively.

If the Supabase module requires a text/string value for jsonb columns, use Make's `toString` or `json` function — but **only if the module documentation or UI confirms this is required**. Do not add a serialization function speculatively.

### Case B: Submission data is nested under a key (e.g., `body`)

Map `raw_payload` to the specific nested key:
```
{{1.body}}        ← if the key is "body"
{{1.data}}        ← if the key is "data"
{{1.payload}}     ← if the key is "payload"
{{1.<key_name>}}  ← substitute the actual key name you observed
```

Use Make's mapping picker to navigate to that key — do not type the path manually unless the picker confirms the path exists.

### Case C: You are unsure which key contains the submission

Do not guess. Map `raw_payload` to the entire module 1 output (`{{1}}`) as a safe default. This captures everything. The downstream `/fastfield-intake` processor can navigate to the correct nesting once you know the key names.

---

## Step 4 — Inspect the Supabase Insert Module

Open the module in scenario 5506328 that writes to `fastfield_webhook_events` (it will be an HTTP module or a Supabase native module).

Check:

1. **Which columns are being mapped?** List the column names that have a Make variable assigned.
2. **Is `raw_payload` in the list?** If not, that is the confirmed failure point.
3. **If `raw_payload` is mapped, what is it mapped to?** Note the variable path (e.g., `{{1.body}}`, `{{1}}`, empty, hardcoded `{}`).
4. **Is `source` hardcoded to `fastfield`?** It should be. If not, note it.
5. **Are `processed` or `processing_status` being set explicitly?** They should not be — the DB defaults (`false` and `'pending'`) handle this automatically.

---

## Step 5 — Correct the Mapping (When Ready to Edit)

When Alejandro is ready to edit the scenario, make only these changes to the Supabase insert module:

**Fields to set explicitly:**

| Column | Value | How |
|--------|-------|-----|
| `source` | `fastfield` | Hardcoded string (already likely set) |
| `raw_payload` | Full submission object | Map picker → module 1 output or nested key per Step 3 decision |

**Fields to leave unmapped (use DB defaults):**

| Column | Why |
|--------|-----|
| `processed` | DB default = false |
| `processing_status` | DB default = 'pending' |
| `id` | DB default = uuid_generate_v4() |
| `received_at` | DB default = now() |

**Fields to leave null for now (downstream parser fills these):**

- `form_name`
- `submission_id`
- `submitter_name`
- `submitted_at`
- `project_number_detected`
- `matched_project_id`
- `matched_project_confidence`
- `error_message`

**Do not set `processed = true` in Make.** That flag is set by `/fastfield-intake` after successful parsing and project matching.

---

## Step 6 — Idempotency Check (Before Production Activation)

Before activating the scenario for production, add a filter or router in Make that checks for duplicate `submission_id` values — to prevent the same FastField form from creating two rows if the webhook fires twice.

Implementation options (evaluate in Make UI):

- **Option A:** Add a Make filter before the Supabase insert: check if a row with the same `submission_id` already exists (requires a Supabase SELECT module upstream)
- **Option B:** Add a `UNIQUE` constraint on `submission_id` in Supabase and let the insert fail gracefully on duplicate (no schema change has been made for this — note it as a future consideration)
- **Option C:** Accept duplicates for the first test only; implement deduplication before full activation

For the first controlled test, Option C is acceptable.

---

## Step 7 — Controlled Test Procedure

**Requires explicit Alejandro approval before execution. This step creates a new row in `fastfield_webhook_events`.**

When approved:

1. Confirm scenario 5506328 is active (or activate it temporarily for the test only)
2. Submit exactly **one** FastField test form — use a test/dummy project or a clearly labeled test submission
3. Wait ~30 seconds for Make to process
4. Run this read-only Supabase query to verify:

```sql
SELECT
  id,
  received_at,
  source,
  form_name,
  submission_id,
  submitter_name,
  submitted_at,
  processing_status,
  processed,
  jsonb_typeof(raw_payload) AS raw_payload_type,
  raw_payload != '{}'::jsonb AS raw_payload_has_content
FROM fastfield_webhook_events
ORDER BY received_at DESC
LIMIT 1;
```

5. Verify against the success criteria below
6. Do NOT print `raw_payload` content

**Success criteria — first-stage row:**

| Field | Expected |
|-------|----------|
| `source` | `fastfield` |
| `received_at` | populated (current timestamp) |
| `raw_payload_has_content` | `true` |
| `raw_payload_type` | `object` |
| `processing_status` | `pending` |
| `processed` | `false` |
| `form_name` | null (acceptable at this stage) |
| `submission_id` | null (acceptable at this stage) |

If `raw_payload_has_content = false` after the fix, the mapping is still not capturing the payload — escalate to Step 2 re-inspection.

**After a passing first-stage row:** run `/fastfield-intake` to inspect `raw_payload` content and extract field names. That is the starting point for Phase 3 (field parsing).

**No project fields should change.** Verify with:

```sql
SELECT project_number, fastfield_submitted, updated_at
FROM projects
WHERE updated_at > now() - interval '5 minutes'
ORDER BY updated_at DESC
LIMIT 5;
```

Expected result: zero rows. If any project record was touched, stop and investigate before proceeding.

---

## Summary

| Item | Status |
|------|--------|
| `fastfield_webhook_events` table exists | ✅ Confirmed |
| `raw_payload` column is jsonb | ✅ Confirmed |
| Schema blocker | None |
| Parsing responsibility | Downstream (`/fastfield-intake`), not Make |
| Confirmed failure point | `raw_payload` arriving as `'{}'` (empty) — Make not mapping it |
| Module to inspect | Webhook trigger (module 1) + Supabase insert module |
| Bundle field to identify | Top-level key containing FastField submission (body/data/root — unknown until inspection) |
| Mapping decision | Observe bundle structure first; use mapping picker, not hardcoded paths |
| Test required | Yes — one controlled submission, requires Alejandro approval |
| No external changes performed | Confirmed — this is a local instruction document only |

---

*No Make.com changes made. No Supabase writes performed. No webhook triggered.*  
*All findings from read-only Supabase schema query and local documentation review.*
