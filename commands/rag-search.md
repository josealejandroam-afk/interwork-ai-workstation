# /rag-search

Search the local memory RAG index with hybrid BM25 + vector retrieval.

## Usage

```
/rag-search QUERY
```

## Instructions

When the user runs `/rag-search <query>`:

Run: `uv run python "D:\ai-workstation\rag\search.py" "<query>"` from the rag directory.

Display the results with their citations and scores. Use the results to answer the user's question if relevant.

The RAG index contains:
- All memory files (profile, projects, procedures, decisions, open loops, etc.)
- Will grow as more files are indexed

To re-index after memory changes: `uv run python "D:\ai-workstation\rag\ingest.py"`
To full rebuild: `uv run python "D:\ai-workstation\rag\rebuild.py"`
To watch for changes: `uv run python "D:\ai-workstation\rag\watch.py"`
