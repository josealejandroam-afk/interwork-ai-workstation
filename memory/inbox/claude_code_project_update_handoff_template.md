# Claude Code → Claude Chat Handoff Template

_This is a template. Fill in the bracketed fields for each session._
_For a live-generated handoff, see: memory/inbox/claude_chat_start_handoff.md_

---

## How to Use

Copy everything below the line and paste into Claude Chat (or a Claude Chat Project) with this prefix:

```
Read the following project update handoff. Use it as your source of truth for this session.
After reading, confirm: (1) what is active, (2) what needs action today, (3) what is blocked.

[paste contents below]
```

---

---

## Session Summary

**Date:** [YYYY-MM-DD]
**Prepared by:** Claude Code
**Source:** Live repo state — memory/, Supabase snapshot (if available)

---

## Active Projects Needing Attention

| # | Client | Name | Location | Status | Next Action |
|---|---|---|---|---|---|
| [#] | [Client] | [Name] | [Location] | [Status] | [What needs to happen] |

---

## Open Loops

| ID | Project | Description | Age | Action |
|---|---|---|---|---|
| [id] | [#] | [What's unresolved] | [Days open] | [What Claude Chat should do] |

---

## Upcoming Deadlines

| Date | Project # | Client | What's Due |
|---|---|---|---|
| [date] | [#] | [client] | [description] |

---

## Blocked Items

| Project # | Blocker | Since | Who Can Unblock |
|---|---|---|---|
| [#] | [What's blocking] | [date] | [Alejandro / client / vendor] |

---

## What Claude Chat Can Help With Right Now

- Draft client confirmation for project [#] — all details in this handoff
- Check status of [project] against the data above
- Review open loop [id] and propose resolution language
- [Other specific tasks]

---

## What Claude Chat Cannot Do in This Session

- Access Supabase directly — use the snapshot data in this handoff
- Send emails or Teams messages — draft only
- Push to the repo — read-only from this pack
- Access live FastField data — last signal noted above

---

## Operating Rules (Always Apply)

1. Draft only — never send communications
2. Propose Supabase changes as a table — never auto-apply
3. Use project card data — never guess project details
4. If a contact is not in this handoff or the client pack — say "not on file"
5. Past-dated scheduled projects are not confirmed closed without FastField + WC evidence

---

_To regenerate the live version: tell Claude Code "Regenerate memory/inbox/claude_chat_start_handoff.md from current state"_
