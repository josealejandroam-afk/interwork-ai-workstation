---
name: feedback-chatgpt-app-vs-browser
description: "Alejandro uses ChatGPT via the desktop app, not the browser — Playwright cannot reach it"
metadata: 
  node_type: memory
  type: feedback
  status: active
  confidence: high
  source: manual
  review_after: 2027-01-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

Alejandro talks to ChatGPT through the **desktop app**, not a browser tab.

**Why this matters:** Playwright only controls browser tabs. It cannot type into or
interact with the ChatGPT desktop app. Any attempt to send a message via Playwright
requires the conversation to be open in a Chrome/Chromium browser tab first.

**How to apply:**
- Never assume a ChatGPT conversation is reachable via Playwright unless Alejandro
  confirms it is open in a browser.
- If sending to ChatGPT via `send_to_chatgpt.py`: first ask Alejandro to open the
  conversation in Chrome and save its URL to `D:\ai-workstation\scripts\chatgpt_target_url.txt`.
- Until that URL file exists and that tab is open, use manual copy/paste between
  Claude Code and the ChatGPT app.
- Do not open a new ChatGPT conversation automatically — always target the saved URL.

[[feedback-chatgpt-message-method]]
