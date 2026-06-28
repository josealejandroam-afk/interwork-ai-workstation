# rag_search.ps1
# Search the local RAG memory index.
# Usage: .\rag_search.ps1 "your query here"
# Example: .\rag_search.ps1 "FastField Make integration"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Query
)

$RAG_DIR = "D:\ai-workstation\rag"

if (-not (Test-Path $RAG_DIR)) {
    Write-Error "RAG directory not found: $RAG_DIR"
    exit 1
}

Set-Location $RAG_DIR
& uv run python search.py $Query
