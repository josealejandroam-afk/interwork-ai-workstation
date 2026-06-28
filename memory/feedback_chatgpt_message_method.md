---
name: feedback-chatgpt-message-method
description: "How to send messages to ChatGPT — use temp file, not inline command"
metadata: 
  node_type: memory
  type: feedback
  status: active
  confidence: high
  source: manual
  review_after: 2027-01-01
  originSessionId: a49556ae-3f91-4870-a82e-d7b4506b952d
---

Do not send long messages to ChatGPT as a single inline PowerShell command argument.

**Why:** Long multi-line strings passed inline break quoting, encoding, and readability.

**How to apply:** Always write the message to a temp file first, then pass the file path to `send_to_chatgpt.py`. Example:

```powershell
$msg = "...message..."
$tmp = "$env:TEMP\chatgpt_msg.txt"
$msg | Out-File -Encoding utf8 $tmp
python D:\ai-workstation\scripts\send_to_chatgpt.py (Get-Content $tmp -Raw)
```

Or extend `send_to_chatgpt.py` to accept a `--file` flag that reads the message from disk.

[[send_to_chatgpt_script]]
