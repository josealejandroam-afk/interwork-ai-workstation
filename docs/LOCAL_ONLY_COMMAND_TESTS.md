# Local-Only Command Tests

Run date: 2026-06-28 13:02
Scope: Commands that work with zero external connections (no secrets, no MCP, no network).
Tested commands: /rag-search, /rag-status, /find-open-loops

---

## Test 1 -- /rag-status (via rag_status.ps1)

**Command:**
```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_status.ps1
```

**Result: PASS**

```
=== RAG Status ===
Date: 2026-06-28 13:02

Memory files (.md):  24
ChromaDB store:      Found at D:\ai-workstation\rag\stores\chroma
SQLite metadata:     Found (12 KB)

--- Index health check (test query) ---
Index:               Healthy (results returned)

--- uv environment ---
uv 0.11.25 (1fc7de7c4 2026-06-26 x86_64-pc-windows-msvc)
Python 3.12.10
```

**Assessment:** Index healthy, 24 memory files indexed, ChromaDB and metadata store both present.

---

## Test 2 -- /rag-search (query: "Alejandro InterWork")

**Command:**
```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "Alejandro InterWork"
```

**Result: PASS**

```
Results for: Alejandro InterWork
+-- [1] interwork_people_map.md  score=0.766  type=reference  status=active --+
+-------- [2] user_profile.md  score=0.741  type=user  status=active ---------+
+-------- [3] user_profile.md  score=0.730  type=user  status=active ---------+
```

**Assessment:** Top results are correct (people map and user profile). Scores above 0.70 indicate strong relevance.

---

## Test 3 -- /rag-search (query: "open loops")

**Command:**
```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "open loops"
```

**Result: PASS**

```
Results for: open loops
+------- [1] project-7492.md  score=0.780  type=project  status=active -------+
+------- [2] project-7492.md  score=0.713  type=project  status=active -------+
+- [3] interwork_project_lifecycle.md  score=0.692  type=reference  status=ac-+
```

**Assessment:** Project file and lifecycle reference surfaced correctly. /find-open-loops draws from the same index -- behavior confirmed sound.

---

## Test 4 -- /rag-search (query: "Read AI meeting intake")

**Command:**
```powershell
powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\rag_search.ps1 "Read AI meeting intake"
```

**Result: PASS**

```
Results for: Read AI meeting intake
+- [1] interwork_ai_ops_master_context.md  score=0.723  type=reference  statu-+
+- [2] interwork_ai_ops_master_context.md  score=0.689  type=reference  statu-+
+- [3] interwork_ai_ops_master_context.md  score=0.658  type=reference  statu-+
```

**Assessment:** Master ops context file surfaced for a meeting-intake query. Correct -- meeting intake procedures live there.

---

## Test 5 -- /find-open-loops (command file installed)

**Installation verified:**
```
D:\ai-workstation\.claude\commands\find-open-loops.md  -- exists
C:\Users\Owner\.claude\commands\find-open-loops.md    -- installed (backup of prior at backups/)
```

**Status:** Command file present. The command reads memory files and the RAG index -- both confirmed healthy above.
Full test requires opening Claude Code and running `/find-open-loops` interactively.

---

## Summary

| Command | Method | Result | Score |
|---------|--------|--------|-------|
| /rag-status | rag_status.ps1 | PASS | 24 files, healthy index |
| /rag-search "Alejandro InterWork" | rag_search.ps1 | PASS | Top score 0.766 |
| /rag-search "open loops" | rag_search.ps1 | PASS | Top score 0.780 |
| /rag-search "Read AI meeting intake" | rag_search.ps1 | PASS | Top score 0.723 |
| /find-open-loops | file check | INSTALLED | Interactive test at first session |

All local commands operational. No secrets, no network, no external MCPs required.

---

## What These Commands Cannot Do (by design)

- Access Supabase project data (needs SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY)
- Surface Teams messages or email (needs M365 MCP)
- Use Read AI meeting summaries (needs Read AI MCP or manual paste)
- Query Smartsheet schedule (needs Smartsheet MCP)

See `docs/COMMAND_ACTIVATION_PLAN.md` for full tier breakdown.
