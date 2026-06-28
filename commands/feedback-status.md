# /feedback-status

Read-only status check of the AI feedback loop. Shows what's pending, what's been reviewed, and what actions are waiting.

---

## Step 1 — Check file timestamps and content

Read these files and report their status:

| File | Path | Check |
|------|------|-------|
| Input packet | `feedback_loop/to_chatgpt.md` | exists? size? last modified? |
| Last response | `feedback_loop/from_chatgpt.md` | exists? timestamp in header? |
| Action plan | `feedback_loop/action_plan.md` | exists? how many items? |
| Loop log | `feedback_loop/loop_log.md` | how many loops run? last run? |

---

## Step 2 — Check whether response is fresh

Compare the modification time of `to_chatgpt.md` vs `from_chatgpt.md`:
- If `to_chatgpt.md` is newer → input has been updated, response is stale → suggest running `/ask-openai-review`
- If `from_chatgpt.md` is newer or same age → response is current

---

## Step 3 — Count action plan items

From `action_plan.md`, count:
- Total numbered items
- Items marked [PRIORITY: high]
- Items marked [PRIORITY: medium]
- Items marked [PRIORITY: low]

List the high-priority items directly in the output.

---

## Output format

```
## Feedback Loop Status — [current date]

### Files
| File | Status | Last Updated | Size |
|------|--------|-------------|------|
| to_chatgpt.md | ✅ ready | 2026-06-26 18:00 | 1234 chars |
| from_chatgpt.md | ✅ current | 2026-06-26 18:05 | 3456 chars |
| action_plan.md | ✅ 5 items | 2026-06-26 18:05 | 789 chars |
| loop_log.md | ✅ 2 loops | last: 2026-06-26 18:05 | — |

### Response freshness
✅ Response is current (from_chatgpt.md is newer than to_chatgpt.md)
OR
⚠️ Input has been updated since last response. Run /ask-openai-review to refresh.

### Pending action items (high priority)
1. [PRIORITY: high] ...
2. [PRIORITY: high] ...

### Next step
Say /ask-openai-review to send the current input packet to OpenAI.
Say "do item N" to execute a specific approved action.
```

---

## Rules

- Read-only. Does not call OpenAI.
- Does not modify any files.
- Does not execute action items.
