# Project Memory Files — Format Guide
_One file per active project. File name: `project-XXXX.md`_
_Last updated: 2026-06-29_

---

## When to Create a Project File

Create a project file when:
- A project needs detailed tracking beyond what the PROJECT_INDEX provides
- There are known contacts, scope details, or open loops specific to this project
- Drafts or decisions are accumulating for this project
- The project is high-risk, in-progress, or has a known issue

---

## Standard Project Card Format

```markdown
---
project_number: XXXX
client: Client Name
status: scheduled | in_progress | completed | on_hold | pending_approval
pm: PM Name
risk: low | medium | high | critical
last_updated: YYYY-MM-DD
---

# Project XXXX — [Name]

## Key Facts
- **Client:** 
- **Location:** 
- **Scheduled Date:** 
- **Scheduled End:** 
- **PM (office):** 
- **Field PM:** 
- **Vendor/Team:** 
- **Vendor Required:** yes / no
- **Scope:** 

## Confirmation Status
| Field | Value |
|-------|-------|
| vendor_confirmed | ✅ / ❌ |
| client_confirmed | ✅ / ❌ |
| access_confirmed | ✅ / ❌ |
| fastfield_submitted | ✅ / ❌ |
| completion_report_sent | ✅ / ❌ |

## Client POC
- Name: 
- Email: 
- Phone: 

## Vendor / Team POC
- Name: 
- Phone: 
- Notes: 

## Known Facts
- 

## Missing Information
- [ ] 

## Open Questions
- 

## Drafts
- [link or inline]

## Next Actions
1. 

## Source References
- Supabase record updated: YYYY-MM-DD
- Smartsheet row: [row ID if known]
- Memory file created: YYYY-MM-DD
```

---

## Existing Project Files

| File | Project | Client | Status |
|------|---------|--------|--------|
| [project-7492.md](project-7492.md) | 7492 Radian Decom Denver CO | Radian | active — open Teams loop |

---

## Rules

- Never invent contact names, phone numbers, or email addresses
- Mark unknown fields as "unknown" — do not leave blank
- Update "last_updated" when the file changes
- Do not put secrets, credentials, or vendor rates in these files
- Confirmation booleans reflect Supabase state — do not update here without Supabase being updated (or note as "unconfirmed" in text)
