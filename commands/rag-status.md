# /rag-status

Check the health and coverage of the local RAG index.

## Instructions

When the user runs `/rag-status`:

### 1. Index health
Run: `uv run python "D:\ai-workstation\rag\search.py" "test" 2>&1`
- If it returns results → index is healthy
- If it errors → diagnose: missing dependencies, empty index, or broken config

### 2. Coverage check
Count files in memory vs files indexed:
```
memory files:  dir /s /b D:\ai-workstation\memory\*.md | find /c ".md"
open loops:    count .md files in open_loops\ (excluding _template.md)
projects:      count .md files in projects\ (excluding _template.md)
```

Compare against what the RAG index actually contains (if the index exposes a count endpoint).

### 3. Staleness check
List memory files modified more recently than the last ingest run.
If any exist: suggest running `uv run python "D:\ai-workstation\rag\ingest.py"`

### 4. Output format

```
## RAG Status — [date]

Index:      ✅ healthy / ❌ error: [message]
Documents:  N indexed
Memory:     N .md files (M unindexed or stale)
Open loops: N active items
Projects:   N project files

Stale files (modified since last ingest):
  - [file] — [N days ago]

Next action:
  - Run /rag-search "test query" to verify retrieval
  - Run ingest.py if stale files listed above
```

### 5. If RAG is not set up at all
Report: "RAG index not found at C:\\Users\\1\\.claude\\rag\\ — run /rag-search to initialize or check setup."
Do not error out — just report clearly.
