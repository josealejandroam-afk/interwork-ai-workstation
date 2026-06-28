---
name: interwork-communication-rules
description: "How Claude drafts and handles InterWork communications — tone, content rules, approval gates, and message templates"
metadata: 
  node_type: memory
  type: reference
  status: active
  confidence: high
  source: claude-code-session
  review_after: 2026-12-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

# InterWork Communication Rules
_Last updated: 2026-06-26_

---

## Tone and Style

- Use concise, corporate tone.
- Write in complete sentences. Keep messages practical and action-focused.
- Do not use em dashes (—). Use commas, colons, or short sentences instead.
- Do not use exclamation marks in professional correspondence.
- Do not use filler phrases: "I hope this finds you well", "Please don't hesitate", "As per my last email".
- Do not use passive voice when active is clearer.
- Spell out numbers under 10 in prose. Use numerals for dates, addresses, and quantities.

---

## Approval Rules

| Action | Allowed? |
|--------|----------|
| Draft an email or Teams message | Yes — automatic |
| Send an email | No — requires Alejandro approval |
| Send a Teams message | No — requires Alejandro approval |
| Update `client_confirmed` | No — requires Alejandro approval |
| Update `vendor_confirmed` | No — requires Alejandro approval |
| Commit InterWork to a date, price, or scope | No — requires Alejandro approval |
| Update `access_confirmed` | No — requires Alejandro approval |

**Always:** Draft first, surface to Alejandro, wait for "send it" or explicit approval.

---

## Client Communications

**What to include:**
- Project reference (project number or scope description)
- Confirmed date and arrival time window
- PM full name and phone number (if known — check `memory/references/interwork_people_map.md`)
- On-site POC expectations
- Any access instructions (dock, freight elevator, building security)
- Next step or confirmation request

**What to exclude:**
- Vendor names, rates, or subcontractor details
- Internal cost or margin information
- Other clients or unrelated project details
- Phrasing that commits to a scope not yet confirmed

**Vendor reference rule:**
Never call a vendor "local vendor" or name a vendor to the client.
Use "our team" or "InterWork" instead.

**Example — client scheduling confirmation:**
> Hi [Name], this is to confirm our team will be on-site at [address] on [date] starting at [time]. [PM full name] will be your point of contact on-site and can be reached at [phone]. Please ensure [access instructions]. Let us know if anything changes before then.

---

## Vendor Communications

**What to include:**
- Project number and job name
- Full site address, floor, suite
- Date and arrival time
- Scope of work (concise)
- Truck and equipment requirements
- Client POC name and phone (on-site contact only — not internal contacts)
- Special instructions (dock, freight elevator, parking, COI, after-hours)
- Request for confirmation of crew size, arrival time, and any questions

**What to exclude:**
- Client billing or pricing information
- Rate discussions in project-specific emails (handle separately)
- Other vendor assignments

**Example — vendor confirmation request:**
> Hi [Name], please confirm your availability for the following job. Project: [#] [name]. Date: [date]. Address: [full address]. Scope: [summary]. Arrival: [time]. Crew: [size]. Truck: [type]. On-site POC: [name], [phone]. Please confirm crew and arrival time by [date].

---

## Field PM Teams Messages

**What to include:**
- Project number and job name
- Full address with floor/suite
- Date and arrival time
- Scope summary (brief, field-focused)
- Client on-site POC name and phone
- Truck/equipment assigned
- Parking/loading dock info
- Special instructions (fragile items, building restrictions, etc.)
- Any photos or documents attached

**Keep it short.** PMs read these on mobile. One screen max.

**Example:**
> 7374 - Ingersoll Rand Buffalo NY | [date] | Arrive: [time] | [full address, floor] | Scope: [summary] | POC: [name] [phone] | Truck: [type] | [any special notes]

---

## Open Loop and Action Item Messages

When surfacing an open loop or pending action to Alejandro:
- State the project number and name
- State what is pending and why it matters
- State the proposed action
- Ask for approval or direction

---

## Security and Privacy Rules

- Never include API keys, tokens, service role keys, or credentials in any message.
- Never expose internal system architecture, Supabase project IDs, or RAG index details in client-facing content.
- Never share one client's information with another client.
- Limit email/Teams content to what the recipient needs for their role.
- When pasting meeting notes or emails into Claude, they stay in memory only — never forwarded externally without approval.

---

## Phrasing That Requires Approval Before Sending

Any message containing these commitments must be reviewed by Alejandro before sending:

- A specific date or time commitment ("we will arrive on...")
- A price or cost reference
- A scope expansion ("we can also handle...")
- A guarantee or promise of outcome
- An apology that implies InterWork fault
- Anything referencing a vendor by name to a client
