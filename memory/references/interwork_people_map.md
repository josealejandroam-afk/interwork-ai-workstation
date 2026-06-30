---
name: interwork-people-map
description: "Key people at InterWork Office and client/vendor contacts — roles, responsibilities, when to involve them, contact info"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork People Map
_Last updated: 2026-06-26 | Update as reliable information is learned_

---

## Core InterWork Team

### Alejandro Acosta
- **Title:** Operations Project Manager
- **Email:** alejandroa@interworkoffice.com
- **Personal email:** jose.alejandro.a.m@gmail.com
- **Role in system:** Primary operator. Project coordination. Final approval authority for all Claude actions that involve Supabase writes, status changes, client/vendor messages, or business commitments.
- **When to involve:** Before any Supabase write, status change, confirmation boolean update, email or Teams send, pricing decision, or anything that commits InterWork to a date/scope/price.
- **Notes:** Work communications via Outlook/M365 and Teams. Gmail (jose.alejandro.a.m@gmail.com) is personal only — no project data there. Primary point of contact for day-to-day AI operations engine decisions.

### Hunter Barbieri
- **Title:** Operations Project Manager
- **Role:** Operations and project support. Scheduling, project coordination, Smartsheet and calendar entry support.
- **Notes:** Handles project scheduling and coordination support. Peer to Alejandro on operations.

### Stephanie Sprinkel
- **Title:** unknown — scheduling/project support
- **Role:** Calendar and project entry support. Scheduling assistance.
- **Notes:** Update role title when confirmed.

### Francisco Vinueza
- **Role:** Operations Manager. Field leadership and project guidance. Escalation point for field issues.
- **Notes:** Senior operations oversight. Escalate unresolved field or vendor issues here.

### David Steinbrecher
- **Role:** Internal leadership and project oversight.
- **Notes:** Executive/leadership layer. Involve on major scope, budget, or client escalations.

---

## Field PMs

Field PMs lead crews on-site. Include name, phone, and project associations as known.

| PM Name | Email | Phone | Notes |
|---------|-------|-------|-------|
| Frank Barrett | frankb@interworkoffice.com | 718-775-6242 | PM — confirmed from Supabase 2026-06-29 |
| Pedro Martinez | pedrom@interworkoffice.com | unknown | PM |
| Juan Martinez | juanm@interworkoffice.com | unknown | PM — assigned to 7053 Strategic Education DC |
| Melvin Hernandez | melvinh@interworkoffice.com | unknown | PM |
| Jairo Escalante | jairoe@interworkoffice.com | unknown | PM — field PM for 7189 MMC Bermuda Hoboken |
| Manny Gonzalez | mannyg@interworkoffice.com | unknown | PM |
| Christian Zuniga | (unknown) | unknown | PM — in team_members; no projects seen yet |
| Oli Martinez | eunisesm@interworkoffice.com | unknown | PM — email address differs from display name; verify |
| Eucladio Calero | (unknown) | unknown | PM — in team_members; no email on record |
| Hunter Barbieri | hunterb@interworkoffice.com | unknown | PM — office assignee for 7189 MMC Bermuda |
| Francisco Vinueza | franciscov@interworkoffice.com | 609-744-1467 | Operations Manager — PM for 7189 in Supabase |

**Rules:**
- Do not invent phone numbers. Mark unknown if not confirmed.
- When sending PM Teams/scheduling messages, include full name and phone in client confirmations when the number is known.
- Update this table as phone numbers are confirmed from Teams, emails, or Smartsheet.

---

## Client Contacts

Track as learned from meetings, emails, Smartsheet, and Read AI.

| Project # | Client | Contact Name | Role | Phone | Email | Notes |
|-----------|--------|-------------|------|-------|-------|-------|
| 7492 | Radian | John Smith | unknown | unknown | unknown | Open Teams loop as of 2026-06-26; awaiting response |
| (add as learned) | | | | | | |

---

## Vendor Contacts

Track as learned. Never expose vendor identity or rates to clients.

| Vendor | Region | Contact | Phone | Notes |
|--------|--------|---------|-------|-------|
| (add as learned) | | | | |

**Rule:** Always refer to vendors as "our team" or "InterWork" in client-facing communications.

---

## Building / Site Contacts

Track site-specific contacts (dock managers, building security, facilities) as encountered.

| Project # | Address | Contact | Phone | Notes |
|-----------|---------|---------|-------|-------|
| (add as learned) | | | | |

---

## Other Groups

| Group | Contact | Notes |
|-------|---------|-------|
| Accounting | unknown | Track for invoice/PO follow-up |
| Sustainability | unknown | e-waste, donation, recycling disposal plans |
| IT / Facilities | unknown | Client-side IT coordination for tech-heavy projects |

---

## Lookup Rules for Claude

1. When drafting a client scheduling confirmation, check this file for the PM's phone number.
2. When matching a project to a person from a Teams or email thread, update the relevant project file (`memory/projects/project-XXXX.md`) and note the contact here if new.
3. When a Read AI meeting introduces a new contact, add them to the appropriate section.
4. If a field PM's phone is confirmed via Teams or email, update the table above.
5. Never invent contact information. Unknown = unknown.
