# rag_reindex.ps1
# Re-index the local memory files into ChromaDB.
# Runs incremental by default (skips unchanged files).
# Usage: .\rag_reindex.ps1
#        .\rag_reindex.ps1 -Force    (full rebuild)

param(
    [switch]$Force
)

$RAG_DIR = "D:\ai-workstation\rag"
$MEMORY_DIR = "D:\ai-workstation\memory"

if (-not (Test-Path $RAG_DIR)) {
    Write-Error ("RAG directory not found: " + $RAG_DIR)
    exit 1
}

if (-not (Test-Path $MEMORY_DIR)) {
    Write-Error ("Memory directory not found: " + $MEMORY_DIR)
    exit 1
}

Set-Location $RAG_DIR

if ($Force) {
    Write-Host "Running full rebuild (--force)..."
    & uv run python ingest.py --force
} else {
    Write-Host "Running incremental index (skips unchanged files)..."
    & uv run python ingest.py
}
