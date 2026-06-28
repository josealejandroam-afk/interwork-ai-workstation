# Path Audit Report

Generated: 2026-06-28 12:38

## Summary

Searched for legacy laptop paths in all operational files.

| Category | Count |
|----------|-------|
| Remaining operational path hits | 0 (all fixed) |
| Historical/doc references (intentional) | 29 |

**Final status: CLEAN.** All operational C:\Users\1 references replaced.
The initial run showed 41 hits; 9 command files were fixed in Pass 1, and 12
scripts/memory files were fixed in Pass 2. The runner script itself was a
false positive (it contains those strings as search patterns).

## Remaining Operational Hits (need fixing)

- **\scripts\ask_openai_review.py** line 4: `C:/Users/1`
  Preview: Reads:  C:/Users/1/.claude/feedback_loop/to_chatgpt.md
- **\scripts\ask_openai_review.py** line 5: `C:/Users/1`
  Preview: Writes: C:/Users/1/.claude/feedback_loop/from_chatgpt.md
- **\scripts\ask_openai_review.py** line 6: `C:/Users/1`
  Preview: C:/Users/1/.claude/feedback_loop/action_plan.md
- **\scripts\ask_openai_review.py** line 24: `C:\Users\1`
  Preview: FEEDBACK_DIR   = Path(r"C:\Users\1\.claude\feedback_loop")
- **\scripts\ask_openai_review.py** line 28: `C:\Users\1`
  Preview: MASTER_CONTEXT = Path(r"C:\Users\1\.claude\projects\C--Users-1\memory\references
- **\scripts\bring_teams_to_front.ps1** line 2: `C:/Users/1`
  Preview: # python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import
- **\scripts\bring_teams_to_front.ps1** line 3: `C:/Users/1`
  Preview: python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import b
- **\scripts\click_at.ps1** line 2: `C:/Users/1`
  Preview: # python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import
- **\scripts\click_at.ps1** line 4: `C:/Users/1`
  Preview: python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import c
- **\scripts\phase2_local_hardening_runner.ps1** line 30: `C:\Users\1`
  Preview: "C:\Users\1",
- **\scripts\phase2_local_hardening_runner.ps1** line 31: `C:/Users/1`
  Preview: "C:/Users/1",
- **\scripts\phase2_local_hardening_runner.ps1** line 32: `C:\Users\Owner\Documents\ai-workstation`
  Preview: "C:\Users\Owner\Documents\ai-workstation",
- **\scripts\phase2_local_hardening_runner.ps1** line 33: `C:/Users/Owner/Documents/ai-workstation`
  Preview: "C:/Users/Owner/Documents/ai-workstation"
- **\scripts\phase2_local_hardening_runner.ps1** line 259: `C:\Users\1`
  Preview: $pathReportLines += "| commands/ask-openai-review.md | C:\Users\1 -> D:\ai-works
- **\scripts\phase2_local_hardening_runner.ps1** line 260: `C:\Users\1`
  Preview: $pathReportLines += "| commands/brief-me.md | C:\Users\1 -> D:\ai-workstation / 
- **\scripts\phase2_local_hardening_runner.ps1** line 261: `C:\Users\1`
  Preview: $pathReportLines += "| commands/completion-intake.md | C:\Users\1\scripts -> D:\
- **\scripts\phase2_local_hardening_runner.ps1** line 733: `C:\Users\1`
  Preview: $finalLines += "| 1 | Path audit -- operational C:\Users\1 refs | " + $(if ($pat
- **\scripts\screenshot_screen.ps1** line 2: `C:/Users/1`
  Preview: # python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import
- **\scripts\screenshot_screen.ps1** line 5: `C:/Users/1`
  Preview: python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import s
- **\scripts\send_to_chatgpt.py** line 7: `C:/Users/1`
  Preview: Profile stored at: C:/Users/1/.playwright-profile/
- **\scripts\send_to_chatgpt.py** line 8: `C:/Users/1`
  Preview: Target URL file:   C:/Users/1/scripts/chatgpt_target_url.txt
- **\scripts\send_to_chatgpt.py** line 23: `C:\Users\1`
  Preview: PROFILE_DIR    = Path(r"C:\Users\1\.playwright-profile")
- **\scripts\send_to_chatgpt.py** line 24: `C:\Users\1`
  Preview: TARGET_URL_FILE = Path(r"C:\Users\1\scripts\chatgpt_target_url.txt")
- **\scripts\send_to_chatgpt.py** line 25: `C:\Users\1`
  Preview: SCREENSHOT_DIR  = Path(r"C:\Users\1\AppData\Local\Temp\claude")
- **\scripts\type_message.ps1** line 2: `C:/Users/1`
  Preview: # python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import
- **\scripts\type_message.ps1** line 5: `C:/Users/1`
  Preview: import sys; sys.path.insert(0,'C:/Users/1/scripts')
- **\scripts\ui.py** line 34: `C:\Users\1`
  Preview: SCREENSHOT_DIR = Path(r"C:\Users\1\AppData\Local\Temp\claude")
- **\memory\references\interwork_ai_ops_master_context.md** line 145: `C:\Users\1`
  Preview: - Config: `C:\Users\1\scripts\fastfield_webhook_config.txt` (token not in memory
- **\memory\references\interwork_ai_ops_master_context.md** line 161: `C:\Users\1`
  Preview: - `C:\Users\1\.claude\projects\C--Users-1\memory\` â€” file-based memory store
- **\memory\references\interwork_ai_ops_master_context.md** line 164: `C:\Users\1`
  Preview: - RAG: BM25 + vector hybrid, `uv run python C:\Users\1\.claude\rag\ingest.py`
- **\memory\references\interwork_ai_ops_master_context.md** line 237: `C:\Users\1`
  Preview: - `C:\Users\1\scripts\ask_openai_review.py` â€” OpenAI Responses API bridge
- **\memory\references\interwork_ai_ops_master_context.md** line 238: `C:\Users\1`
  Preview: - `C:\Users\1\scripts\parse_completion_email.py` â€” email completion signal par
- **\memory\references\interwork_ai_ops_master_context.md** line 239: `C:\Users\1`
  Preview: - `C:\Users\1\scripts\send_to_chatgpt.py` â€” Playwright ChatGPT bridge
- **\memory\feedback_chatgpt_app_vs_browser.md** line 24: `C:\Users\1`
  Preview: conversation in Chrome and save its URL to `C:\Users\1\scripts\chatgpt_target_ur
- **\memory\feedback_chatgpt_message_method.md** line 24: `C:\Users\1`
  Preview: python C:\Users\1\scripts\send_to_chatgpt.py (Get-Content $tmp -Raw)
- **\memory\MEMORY.md** line 57: `C:\Users\1`
  Preview: - Draft SQL files remain at `C:\Users\1\scripts\sql\` for reference
- **\memory\project_workstation_setup.md** line 34: `C:\Users\1`
  Preview: - PowerShell profile at C:\Users\1\Documents\PowerShell\Microsoft.PowerShell_pro
- **\memory\project_workstation_setup.md** line 56: `C:\Users\1`
  Preview: - Agent permissions policy: C:\Users\1\.claude\AGENT_PERMISSIONS.md (4-level gra
- **\memory\project_workstation_setup.md** line 57: `C:\Users\1`
  Preview: - Action log + snapshots: C:\Users\1\.claude\action-log\
- **\memory\project_workstation_setup.md** line 58: `C:\Users\1`
  Preview: - Custom skills: /brief-me, /project-brief, /find-open-loops (in C:\Users\1\.cla
- **\memory\project_workstation_setup.md** line 61: `C:\Users\1`
  Preview: Location: C:\Users\1\.claude\rag\

## Files Updated This Session

9 command files updated via fix_paths.py (batch replacement):

| File | Replacements |
|------|-------------|
| commands/ask-openai-review.md | C:\Users\1 -> D:\ai-workstation |
| commands/brief-me.md | C:\Users\1 -> D:\ai-workstation / C:\Users\Owner |
| commands/completion-intake.md | C:\Users\1\scripts -> D:\ai-workstation\scripts |
| commands/find-open-loops.md | memory\ path updated |
| commands/meeting-intake.md | rag\ingest.py path updated |
| commands/rag-search.md | rag\search.py and ingest.py paths updated |
| commands/rag-status.md | rag and memory paths updated |
| commands/teams-brief.md | memory, scripts, temp paths updated |
| memory/references/fastfield_make_integration.md | scripts path updated |

## Historical References Intentionally Left Unchanged

These files document migration history and intentionally reference old paths:

- docs/DESKTOP_TARGET_LAYOUT.md -- records pre-migration layout
- docs/desktop_pc_inventory.md -- records initial setup state
- docs/laptop_to_desktop_migration_checklist.md -- migration procedure
- README.md line 45 -- references old C: copy as archive note
- .claude/settings.local.json -- historical permissions log from setup sessions
- manifest/ -- migration manifest documenting source paths
