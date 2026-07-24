---
name: post-fastfield-teams-notification-standard
description: "Canonical Teams notification sent after Alejandro submits a field PM's FastField assignment"
metadata:
  node_type: memory
  type: procedure
  status: active
  confidence: high
  source: alejandro-confirmed-teams-examples
  review_after: 2027-01-24
---

# Post-FastField Teams Notification Standard
_Last updated: 2026-07-24_

Use this format for the Teams notification sent **after** Alejandro submits a field PM's FastField assignment.

## Three Distinct Events

| Event | Meaning | Evidence |
|---|---|---|
| FastField assignment submitted by Alejandro | Alejandro created/dispatched the assignment to the PM | FastField assignment record or Alejandro confirmation |
| Post-FF Teams notification sent | Alejandro notified the PM in Teams that the assignment is ready | Sent Teams message |
| Completed FastField submitted by PM | The PM completed and returned the field report | FastField webhook/export or other confirmed completion evidence |

Never merge these events.

- The FastField assignment is the operational form and detailed instructions.
- The Teams message is only the notification sent after the assignment.
- The PM's completed FastField submission is the completion evidence.

## Canonical Template

```text
Project #[PROJECT NUMBER], [CLIENT / PROJECT NAME]

Hi [PM FULL NAME],

The FF has been submitted for Project #[PROJECT NUMBER], [CLIENT / PROJECT NAME].

Date: [DAY OF WEEK, MONTH DAY]
Start Time: [TIME]
Location: [LOCATION NAME, IF CONFIRMED]
[FULL ADDRESS]

Site Contact:
[CONTACT NAME], [PHONE]

Scope includes:

- [FIELD-READY SCOPE ITEM]
- [FIELD-READY SCOPE ITEM]
- [FIELD-READY SCOPE ITEM]

[SPECIAL RESTRICTION OR CLARIFICATION, IF APPLICABLE]

Please review the FF and let me know if anything needs to be clarified.
```

## Fixed Wording

Always use:

> The FF has been submitted for Project #[PROJECT NUMBER], [CLIENT / PROJECT NAME].

Always close with:

> Please review the FF and let me know if anything needs to be clarified.

Do not replace these sentences with alternate wording unless Alejandro asks for a project-specific revision.

## Field Order

Use this order:

1. Project heading
2. PM greeting
3. FF-submitted sentence
4. Date or dates
5. Start time
6. Location, starting location, destination, or route
7. Field PM phone, only when operationally useful
8. Site contact or contacts
9. Scope bullets
10. Special restriction or clarification
11. Fixed closing

## Formatting Rules

- Use the PM's full name in the greeting.
- Use `Date:` for one date and `Dates:` for a date range.
- Use `Location:` for one site.
- Use `Starting Location:` and `Destination:` for a move.
- Use `Route:` when the work has multiple confirmed stops.
- Use `Site Contact:` for one contact and `Site Contacts:` for multiple contacts.
- Keep scope as practical action bullets.
- Include exclusions, cancellations, access restrictions, and "do not move" instructions after the scope.
- Omit any field that is not confirmed. Never leave a blank placeholder in the final message.
- Use "today" or "tomorrow" only when verified against the current date. Include the calendar date whenever possible.
- Do not include vendor names, rates, internal costs, or unconfirmed details.
- Keep the message readable on mobile. Include only information the PM needs to execute the assignment.

## Status Meaning

In this PM-facing notification, "The FF has been submitted" means Alejandro submitted or dispatched the FastField assignment to the PM before sending the Teams message.

The Teams notification:

- is not the FastField assignment itself;
- does not replace the scope and instructions inside FastField;
- does not prove the PM reviewed the assignment;
- does not mean the PM completed and returned the field report; and
- does not independently set `fastfield_submitted = true`.

Completed FastField status still requires confirmed PM submission evidence.

## Approval Rule

Drafting this message is allowed automatically. Sending it in Teams requires Alejandro's explicit instruction.
