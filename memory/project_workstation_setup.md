---
name: project-workstation-setup
description: Windows AI coding and automation workstation setup — fully complete as of 2026-06-25
metadata: 
  node_type: memory
  type: project
  status: active
  confidence: high
  source: user
  created: 2026-06-25
  updated: 2026-06-25
  review_after: 2026-09-25
  originSessionId: 4a088d6c-1904-4cd5-80e7-c02aab2ef3e1
---

Windows laptop set up as a complete AI coding/automation workstation.

**Why:** Full-stack AI dev environment for coding and automation work.

## Installed Tools

Windows (via Scoop/winget/npm):
- Scoop 0.5.3, jq 1.8.2, GitHub CLI 2.95.0
- Node.js v26.4.0 + npm 11.17.0
- ripgrep 15.1.0, fd 10.4.2, make 4.4.1, SQLite3 3.53.2
- uv 0.11.24 (Python package manager)
- ffmpeg 8.1.1, pandoc 3.10
- Docker Desktop 4.78.0 (WSL2 backend confirmed)
- Playwright 1.61.1 (Chromium, Firefox, WebKit)
- Ollama 0.30.10 (local LLM runner, smollm:135m pulled and tested)
- direnv 2.37.1, starship 1.25.1, fzf 0.73.1, zoxide 0.9.9, bat 0.26.1, delta 0.19.2

Shell config:
- PowerShell profile at C:\Users\1\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
- starship prompt, zoxide, fzf (Ctrl+T/Ctrl+R via PSFzf), direnv hook, git delta
- git configured globally to use delta for diffs

WSL2 / Ubuntu (user: alejandro):
- Ubuntu running WSL2 with systemd enabled
- Docker CE 29.6.0 (auto-starts via systemd, alejandro in docker group)
- starship 1.25.1, zoxide 0.9.9, fzf 0.67.0, bat 0.25.0, delta 0.19.2, direnv 2.37.1
- ~/.bashrc configured with all tool hooks
- Python 3.14.4, Git 2.53.0, curl 8.18.0

## MCP Servers Connected
- Playwright (browser automation — navigate, click, type, screenshot, snapshot)
- Gmail, Google Drive
- Smartsheet
- Supabase
- Vercel
- Make.com
- Microsoft 365

## Agent Infrastructure (added 2026-06-25)
- Memory system restructured with subfolders: profile/ projects/ procedures/ decisions/ contacts/ preferences/ open_loops/ mistakes/ tool_notes/
- Agent permissions policy: C:\Users\1\.claude\AGENT_PERMISSIONS.md (4-level graduated autonomy)
- Action log + snapshots: C:\Users\1\.claude\action-log\
- Custom skills: /brief-me, /project-brief, /find-open-loops (in C:\Users\1\.claude\commands\)

## RAG Stack (added 2026-06-25) ✅
Location: C:\Users\1\.claude\rag\
- ChromaDB (persistent vector store, cosine similarity)
- BAAI/bge-small-en-v1.5 embedding model
- BM25S keyword search
- SQLite metadata tracker (file hashes, mtime, chunk counts)
- Hybrid scoring: 0.55 × vector + 0.35 × BM25 + 0.10 × recency/status boost
- Scripts: ingest.py, search.py, rebuild.py, watch.py
- Commands: `uv run python ingest.py` / `uv run python search.py "query"`
- Auto-reindex on file change via watch.py

Memory indexed: 3 files, 6 chunks (grows as memory expands)

**Next Up for RAG:** Index PDFs, DOCX, Google Drive exports; add /rag-search skill

**How to apply:** Workstation setup is complete. Use RAG search to answer questions about projects/preferences without reading files one by one.
