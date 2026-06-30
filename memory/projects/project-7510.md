---
project_number: 7510
client: Pear
status: scheduled
pm: Frank Barrett
risk: medium
last_updated: 2026-06-29
---

# Project 7510 — Pear Relocation San Francisco CA

## Key Facts
- **Client:** Pear (pear.vc)
- **Location:** 600 Townsend, San Francisco CA
- **Scheduled Date:** 2026-07-01
- **Scheduled End:** 2026-07-02
- **Start Time:** 8 AM (confirmed by client)
- **PM (lead):** Frank Barrett — frankb@interworkoffice.com, 718-775-6242
- **Account manager (InterWork):** Jill Buchman — jillb@interworkoffice.com, 609-744-8911
- **Vendor/Crew:** Not yet identified in Supabase — Frank Barrett is PM but crew not named
- **Vendor Required:** Yes (per Supabase)
- **Scope:** Office relocation to 600 Townsend SF. Earlier move leg was 5/27. ~6 small plants moving to new space; large plants staying in "Owens." TVs are NOT wall-mounted — no unmounting labor needed.
- **Previous phase:** Pear internal shift (Frank's team previously moved plants for client)

## Confirmation Status
| Field | Value | Notes |
|-------|-------|-------|
| vendor_confirmed | ❌ false (Supabase) | Crew not named |
| client_confirmed | ❌ false (Supabase) | **Mel confirmed Jul 1 + 8AM in email** — propose update |
| access_confirmed | ❌ false | COI sent to client; building access not explicitly confirmed |
| fastfield_submitted | ❌ false | Job hasn't happened yet |
| completion_report_sent | ❌ false | Job hasn't happened yet |

## Client POC
- **Name:** Mel Apostol
- **Email:** mel@pear.vc
- **Phone:** unknown
- **Notes:** Primary contact. Has been communicating with Jill Buchman via email. Responsive.

## InterWork Account Contact
- **Name:** Jill Buchman
- **Email:** jillb@interworkoffice.com
- **Phone:** 609-744-8911
- **Role:** Appears to be account manager / sales-side contact for this engagement

## Vendor / Team POC
- **Lead PM:** Frank Barrett (718-775-6242)
- **Crew:** Not confirmed — follow up with Frank

## Known Facts (from email thread 2026-06-23 through 2026-06-26)
- Jul 1 confirmed by client in writing (Mel Apostol, Jun 23)
- 8 AM start time confirmed by client (Mel Apostol, Jun 26)
- COI for 600 Townsend required; COI-LPC West.pdf sent by Jill to Mel on Jun 26
- Mel sent back COI requirements (as PDF attachment) for 600 Townsend
- ~6 small plants in scope; large plants staying in "Owens"
- TVs are NOT wall-mounted — no unmounting labor; quote line item may need revision
- Quote was sent to Mel on Jun 25 and is under review
- CC'd on emails: Francisco Vinueza, InterWork Operations, Alejandro Acosta, David Steinbrecher

## Missing Information
- [ ] Crew/vendor crew composition — who is physically doing the move?
- [ ] Is the COI accepted by the building at 600 Townsend?
- [ ] Is building access for Frank confirmed for 8 AM Jul 1?
- [ ] Has the quote been accepted/PO issued?
- [ ] TV scope revision — does quote need to be reissued?
- [ ] Mel's phone number

## Open Questions
1. Who is the crew? Frank is PM but someone needs to execute — is this a vendor crew or InterWork team?
2. Has 600 Townsend building management confirmed the COI and access for Jul 1 at 8 AM?
3. Has Mel accepted the quote or is it still pending?
4. Does the TV line in the quote need to be corrected before the job?

## Proposed Supabase Updates (requires Alejandro approval)
- `client_confirmed = true` — Mel confirmed Jul 1 + 8 AM explicitly in email
- `location_address = '600 Townsend'` — confirmed from email
- No other booleans should change yet

## Drafts
See `docs/july1_readiness_report_2026-06-29.md` for Teams message draft to Frank Barrett.

## Next Actions
1. Contact Frank Barrett (Teams or 718-775-6242) — confirm crew, confirm he has building access for 8 AM Jul 1
2. Alejandro: approve `client_confirmed = true` and address update for 7510 when ready
3. Verify COI was accepted by building management
4. Check if quote needs TV line revision before job

## Source References
- Supabase record: created 2026-06-26, source=smartsheet
- Email thread: "Inquiry: Pear Move to 600 Townsend" — Jill Buchman ↔ Mel Apostol, Jun 23–26 2026
- Memory file created: 2026-06-29
