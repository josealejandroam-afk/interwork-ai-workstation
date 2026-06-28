---
name: interwork-command-center-schema
description: "Supabase schema for interwork-command-center (project ref hskgrxhdtgowagkfkjsw) — tables, columns, enums, relationships"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: supabase-mcp
  review_after: 2026-09-01
  project_ref: hskgrxhdtgowagkfkjsw
  region: us-east-1
  db_version: PostgreSQL 17.6
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Command Center — Supabase Schema

**Project:** interwork-command-center  
**Ref:** `hskgrxhdtgowagkfkjsw`  
**URL:** `https://hskgrxhdtgowagkfkjsw.supabase.co`  
**Region:** us-east-1 | **Status:** ACTIVE_HEALTHY  
**Created:** 2026-03-17

---

## ⚠️ Security Advisory — RLS Disabled

**ALL 13 tables have Row Level Security disabled.**  
Anyone with the publishable (anon) key can read or modify every row.  
Do NOT enable RLS without first writing policies — enabling RLS with no policies blocks all access.

Remediation SQL (review before running — add policies first):
```sql
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.project_vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fastfield_forms ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.communications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smartsheet_sync ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.templates ENABLE ROW LEVEL SECURITY;
```

---

## Tables

### `projects` — Core operational table
The canonical source for all project state. Every other table links here.

| Column | Type | Notes |
|--------|------|-------|
| `id` | uuid PK | Auto-generated |
| `project_number` | text UNIQUE | **Required. Never create without this.** |
| `name` | text | Project name |
| `type` | enum | `workstation_relocation` · `decommission` · `installation` · `delivery` · `walkthrough` · `assessment` · `other` |
| `status` | enum | `inquiry` · `pending_approval` · `approved` · `scheduled` · `in_progress` · `completed` · `closed` · `cancelled` · `on_hold` · `planning` |
| `client_id` | uuid → clients | Required |
| `pm_id` | uuid → team_members | PM assigned |
| `client_poc_id` | uuid → contacts | Client point of contact |
| `onsite_poc_id` | uuid → contacts | On-site point of contact |
| `location_address/city/state/zip/building` | text | Job site location |
| `scope_summary` | text | Short scope description |
| `scope_detail` | text | Full scope |
| `item_count` | int | Number of workstations/items |
| `scheduled_date` | date | Scheduled work date |
| `scheduled_start_time` | time | |
| `actual_start_at / actual_end_at` | timestamptz | Actual execution window |
| `quote_amount` | numeric | |
| `po_number` | text | Client PO |
| `invoiced` | bool | |
| `vendor_confirmed` | bool | Vendor locked in |
| `client_confirmed` | bool | Client confirmed access/scope |
| `fastfield_submitted` | bool | Field form submitted |
| `completion_report_sent` | bool | |
| `pm_assigned` | bool | |
| `access_confirmed` | bool | Building access confirmed |
| `client_informed` | bool | |
| `smartsheet_row_id` | text | Link to Smartsheet row (read reference only) |
| `ai_summary` | text | Claude-generated summary |
| `vendor_name/vendor_lead_name/vendor_lead_phone` | text | Quick vendor fields |
| `priority` | text | default: `'normal'` |
| `tags` | text[] | |
| `internal_notes` | text | |

### `clients`
| Column | Type |
|--------|------|
| `id` | uuid PK |
| `name` | text |
| `short_name` | text |
| `industry` | text |
| `notes` | text |
| `active` | bool |

### `contacts` — All people (client, vendor, onsite, interwork)
| Column | Type |
|--------|------|
| `id` | uuid PK |
| `full_name` | text |
| `role` | enum: `client_poc` · `onsite_poc` · `vendor_lead` · `building_contact` · `interwork_pm` · `interwork_crew` |
| `company` | text |
| `client_id` | uuid → clients |
| `email / phone / phone_alt` | text |
| `preferred_contact` | text |

### `vendors`
| Column | Type |
|--------|------|
| `id` | uuid PK |
| `company_name` | text |
| `specialty` | text |
| `primary_contact_id` | uuid → contacts |
| `regions` | text[] |
| `rating` | int (1–5) |
| `preferred` | bool |

### `team_members` — InterWork staff
| Column | Type |
|--------|------|
| `id` | uuid PK |
| `full_name` | text |
| `role` | text |
| `email` | text UNIQUE |
| `phone` | text |

### `project_vendors` — Project ↔ Vendor assignments
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `vendor_id` | uuid → vendors |
| `contact_id` | uuid → contacts |
| `status` | enum: `identified` · `contacted` · `confirmed` · `declined` · `backup` |
| `crew_size` | int |

### `communications` — All inbound/outbound messages
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `source` | enum: `outlook` · `teams` · `manual` · `smartsheet` · `fastfield` · `phone_log` |
| `direction` | text (inbound/outbound) |
| `subject / body / body_preview` | text |
| `from_address` | text |
| `to_addresses` | text[] |
| `external_id / thread_id` | text | For dedup with Outlook/Teams |
| `occurred_at` | timestamptz |
| `linked_contact` | uuid → contacts |
| `important` | bool |
| `ai_summary` | text |

### `fastfield_forms` — Field inspection/completion forms
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `form_type` | enum: `pre_project` · `site_survey` · `work_completion` · `inventory` · `incident` · `sign_off` · `other` |
| `status` | enum: `not_submitted` · `submitted` · `reviewed` · `approved` |
| `data / raw` | jsonb |
| `submitted_by / submitted_at` | text / timestamptz |

### `documents` — Generated documents
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `doc_type` | enum: `scope_of_work` · `vendor_email` · `client_confirmation` · `work_completion_report` · `project_summary` · `inventory_list` · `other` |
| `content` | text |
| `file_url / file_name` | text |
| `generated_by_ai` | bool |
| `sent_to` | text[] |
| `version` | int |

### `checklist_items` — Per-project checklist
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `item` | text |
| `status` | text (pending/done) |
| `category` | text |
| `required_by` | timestamptz |
| `auto_generated` | bool |

### `activity_log` — Audit trail
| Column | Type |
|--------|------|
| `project_id` | uuid → projects |
| `actor` | text |
| `action` | text |
| `detail` | text |
| `source` | enum (same as communications.source) |
| `before_state / after_state` | jsonb |

### `smartsheet_sync` — Smartsheet import cache
| Column | Type | Notes |
|--------|------|-------|
| `project_id` | uuid → projects | |
| `project_number` | text | |
| `sheet_id / row_id` | text | Smartsheet identifiers |
| `cells / raw` | jsonb | Raw Smartsheet data |
| `sync_status` | text | pending/done/error |

**Smartsheet sync is read-only. Never write back to Smartsheet.**

### `templates` — Reusable document/checklist templates
| Column | Type |
|--------|------|
| `name` | text |
| `category` | text |
| `fields` | jsonb |

---

## Key Relationships

```
clients ──< projects >── team_members (pm_id)
              │
              ├──< project_vendors >── vendors >── contacts
              ├──< communications
              ├──< fastfield_forms
              ├──< documents
              ├──< checklist_items
              ├──< activity_log
              └──< smartsheet_sync
```

---

## Write Rules (from architecture reference)

- `project_number` is mandatory before any INSERT to `projects`
- Never overwrite confirmed boolean fields (`vendor_confirmed`, `client_confirmed`, etc.) without asking
- `smartsheet_row_id` is a reference field — never trigger writes to Smartsheet based on it
- `communications.external_id` / `thread_id` — use for dedup when ingesting from Outlook/Teams (Gmail is personal account, not a work source)
- `activity_log` — Claude should write an entry for every material change it makes
