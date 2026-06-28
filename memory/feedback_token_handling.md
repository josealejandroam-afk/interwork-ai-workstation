---
name: feedback-token-handling
description: "Never print webhook tokens, secrets, or full webhook URLs in terminal output, chat, diffs, memory, or RAG"
metadata: 
  node_type: memory
  type: feedback
  status: active
  confidence: high
  source: alejandro-correction-2026-06-26
  review_after: 2027-01-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

Never print TOKEN_SECRET or full webhook URLs (containing a token) in:
- Terminal output (PowerShell/Bash commands)
- Chat / text response
- File diffs or summaries
- Memory files
- RAG index

**Why:** Tokens exposed in terminal, screenshots, or conversation history are compromised. This happened twice in the same session with the FastField webhook token.

**How to apply:**
- When generating or rotating tokens: write directly to the config file via script; print only "Config updated." — never the token value
- When referencing in chat: display `TOKEN_SECRET=REDACTED` and `WEBHOOK_URL=https://hook.../...REDACTED...`
- Tell Alejandro to copy the actual URL only from the local config file, never from chat
- Make.com tool call parameters are unavoidable (the token must be passed to update the filter), but keep it out of all text responses
- If Read tool output would expose a token: use the value internally only; never echo it in text
