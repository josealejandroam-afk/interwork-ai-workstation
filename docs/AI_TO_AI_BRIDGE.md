# AI-to-AI Bridge — Claude ↔ ChatGPT
_Last updated: 2026-06-29_

---

## What the Bridge Is

The bridge is the fast, live communication channel between Claude and ChatGPT. It has two working mechanisms built into this repo.

GitHub memory is the durable source of truth. The bridge is the working channel. Both are needed.

```
Claude  ──bridge──►  ChatGPT  (quick questions, drafts, second opinions)
   │                    │
   └──── GitHub ────────┘  (decisions, project memory, daily handoffs, open loops)
```

---

## Two Bridge Mechanisms

### Mechanism 1 — OpenAI API (ask_openai_review.py)
**Use this for:** structured reviews, action plan generation, advisory packets

- Claude writes a review packet to `feedback_loop/to_chatgpt.md`
- Script sends it to the OpenAI Responses API using `OPENAI_API_KEY`
- Response is saved to `feedback_loop/from_chatgpt.md` and `feedback_loop/action_plan.md`
- Claude reads the response and presents it to Alejandro
- Key: **secret scrubber runs automatically** before sending — aborts if JWT, API key, or service role detected

**Run it:**
```powershell
cd D:\ai-workstation
uv run python scripts\ask_openai_review.py
# or with model override:
uv run python scripts\ask_openai_review.py --model o4-mini
```

**Use slash command:** `/ask-openai-review` — handles packet building, sending, reading, and logging automatically.

**Files:**
- Input: `feedback_loop/to_chatgpt.md`
- Output: `feedback_loop/from_chatgpt.md`
- Action plan: `feedback_loop/action_plan.md`
- Log: `feedback_loop/loop_log.md`

---

### Mechanism 2 — Playwright Browser Bridge (send_to_chatgpt.py)
**Use this for:** live chat, quick questions, iterative drafting, fast back-and-forth

- Claude writes a message to a temp file
- Script uses Playwright to find the saved ChatGPT conversation tab in Chrome and type the message
- ChatGPT responds in the browser; Alejandro reads it and can copy the result back

**Prerequisites:**
1. ChatGPT conversation must be open in **Chrome** (not the desktop app — Playwright can't reach the app)
2. Target conversation URL saved to `scripts/chatgpt_target_url.txt`
3. Playwright installed in the RAG venv

**Run it:**
```powershell
# Write message to temp file first (never inline long messages)
$msg | Out-File -Encoding utf8 "$env:TEMP\chatgpt_msg.txt"
cd D:\ai-workstation
uv run python scripts\send_to_chatgpt.py --file "$env:TEMP\chatgpt_msg.txt"
```

**Current status:** Requires Alejandro to open the target ChatGPT conversation in Chrome first and confirm the URL is saved to `scripts/chatgpt_target_url.txt`. The desktop app is not reachable via Playwright.

---

## What the Bridge Is Good For

| Use Case | Mechanism | Notes |
|----------|-----------|-------|
| Quick second opinion on a draft | Either | Fast; no setup if API is live |
| Reviewing a SQL proposal before applying | API bridge | Include the SQL, context, and ask for risk review |
| Getting ChatGPT to draft an email | Either | Always save result to memory or inbox |
| Architecture questions | API bridge | Good for async structured review |
| Asking ChatGPT to flag gaps in a plan | API bridge | Include the plan context in `to_chatgpt.md` |
| Live iterative drafting | Playwright | Back-and-forth in a real conversation |
| Advisory before a risky Supabase write | API bridge | Get a second opinion before Alejandro approves |

---

## What the Bridge Is NOT Good For

| Do Not Send | Reason |
|-------------|--------|
| API keys, tokens, service role keys, passwords | Secrets — scrubber blocks these; never bypass it |
| Supabase connection strings | Same — treated as credentials |
| Webhook URLs with embedded tokens | Same |
| Raw email bodies | Contains personal/confidential data |
| Full private meeting transcripts | Confidential unless Alejandro explicitly approves |
| Client-sensitive scope or financial details beyond what's needed | Minimum necessary only |
| Anything that looks like a production write command | ChatGPT output is advisory — never execute without Alejandro approval |

---

## Bridge vs. GitHub Memory

| Question | Bridge | GitHub Memory |
|----------|--------|---------------|
| I need a quick draft | ✅ Use bridge | |
| I need ChatGPT's opinion on a risk | ✅ Use bridge | |
| I'm saving a decision for tomorrow | | ✅ Write to `memory/shared/DECISIONS_LOG.md` |
| I'm recording project facts | | ✅ Write to `memory/projects/project-XXXX.md` |
| I want both AIs to know something next session | | ✅ Write to `memory/shared/` or `memory/inbox/` |
| I need a structured action plan saved | | ✅ Also save to `feedback_loop/action_plan.md` |
| I need to remember what was decided | | ✅ GitHub is the record |

**The rule:** Bridge = speed and conversation. GitHub = truth and memory.

---

## When to Save Bridge Results to GitHub

Save to GitHub when the bridge conversation produces:
- A decision Alejandro confirmed
- A project fact that should persist (address, contact, scope detail)
- An action plan item that will be executed
- A risk flag that hasn't been resolved
- A template or draft that will be reused

**Where to save:**
| Result type | Save to |
|-------------|---------|
| Decisions | `memory/shared/DECISIONS_LOG.md` |
| Project facts | `memory/projects/project-XXXX.md` |
| Open loops / action items | `memory/shared/OPEN_LOOPS.md` |
| ChatGPT → Claude handoff | `memory/inbox/chatgpt_to_claude.md` |
| Claude → ChatGPT context | `memory/inbox/claude_to_chatgpt.md` |
| Structured review response | `feedback_loop/from_chatgpt.md` (auto-saved by script) |
| Approved action plan | `feedback_loop/action_plan.md` (auto-saved by script) |

---

## Safety Rules

1. **Secret scrubber always runs** before API bridge sends — never bypass it
2. **Write long messages to a temp file** first; never pass them inline on the command line (quoting breaks)
3. **ChatGPT output is advisory only** — never auto-execute any recommendation without Alejandro approval
4. **ChatGPT cannot approve production changes** — only Alejandro can
5. **Do not open a new ChatGPT conversation automatically** — always target the saved URL in `scripts/chatgpt_target_url.txt`
6. **Playwright requires a browser tab** — the ChatGPT desktop app is not reachable
7. **Do not send client names + financial details together** — use project numbers where sufficient
8. If the scrubber aborts: fix the packet, do not retry with a bypass

---

## Practical First Use

The most useful immediate use of the bridge is sending the current `claude_to_chatgpt.md` handoff as an API review packet:

1. Copy `memory/inbox/claude_to_chatgpt.md` content into `feedback_loop/to_chatgpt.md`
2. Run `/ask-openai-review`
3. Read the response in `feedback_loop/from_chatgpt.md`
4. Save any confirmed decisions or flags back to `memory/shared/`

This gets ChatGPT up to speed on current state without Alejandro manually copying context.
