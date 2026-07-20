# Vendor Index

_Last updated: 2026-07-17_

Vendor profiles and engagement procedures are **not** part of the client/project lookup
flow — a chat working inside a client project will never discover these unless it's told to
check here, or a project card happens to link to one. Check this index whenever a vendor is
named in the conversation (by Alejandro, in a project card, or in relayed correspondence),
regardless of which client/project the chat is currently focused on.

| Vendor | Profile | Procedure/Workflow (if one exists) | Notes |
|---|---|---|---|
| Sunset Transportation | `memory/vendors/sunset.md` | `memory/procedures/sunset_transportation_workflow.md` | Freight/transportation coordinator only (now associated with Armada) — not a furniture/install labor provider unless a quote explicitly says so |
| Tier LLC | `memory/vendors/tier_llc.md` | — | See profile for capabilities/use cases |
| Just4Wheels | `memory/vendors/just4wheels.md` | — | Low confidence — see profile for caveats |

Template for adding a new vendor: `memory/vendors/_template.md`

## When a Vendor Comes Up But Isn't Listed Here

Don't assume no profile exists just because it's not in this table — check
`memory/vendors/` directly for a file that might not have been indexed yet, then flag to
Alejandro that this index needs updating rather than silently treating the vendor as unknown.

## Source Notes

- Created 2026-07-17 after Alejandro asked why some chat sessions didn't know about Sunset
  Transportation despite `memory/vendors/sunset.md` existing — root cause: no routing rule
  ever pointed chats at `memory/vendors/`, so it was only reachable if a project card
  happened to link to it directly.
