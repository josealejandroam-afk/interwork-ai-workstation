# rag_status.ps1
# Check the health and coverage of the local RAG index.
# Usage: .\rag_status.ps1

$RAG_DIR = "D:\ai-workstation\rag"
$MEMORY_DIR = "D:\ai-workstation\memory"
$CHROMA_DIR = "D:\ai-workstation\rag\stores\chroma"
$SQLITE_DB = "D:\ai-workstation\rag\stores\metadata.sqlite"

Write-Host ""
Write-Host "=== RAG Status ===" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Host ""

# 1. Memory file count
if (Test-Path $MEMORY_DIR) {
    $mdFiles = (Get-ChildItem -Path $MEMORY_DIR -Recurse -Filter "*.md" | Measure-Object).Count
    Write-Host "Memory files (.md):  $mdFiles" -ForegroundColor Green
} else {
    Write-Host "Memory directory NOT FOUND: $MEMORY_DIR" -ForegroundColor Red
}

# 2. Store presence
if (Test-Path $CHROMA_DIR) {
    Write-Host "ChromaDB store:      Found at $CHROMA_DIR" -ForegroundColor Green
} else {
    Write-Host "ChromaDB store:      NOT FOUND — run rag_reindex.ps1" -ForegroundColor Yellow
}

if (Test-Path $SQLITE_DB) {
    $dbSize = (Get-Item $SQLITE_DB).Length
    Write-Host "SQLite metadata:     Found ($([math]::Round($dbSize/1KB, 1)) KB)" -ForegroundColor Green
} else {
    Write-Host "SQLite metadata:     NOT FOUND — run rag_reindex.ps1" -ForegroundColor Yellow
}

# 3. Quick search health check
Write-Host ""
Write-Host "--- Index health check (test query) ---" -ForegroundColor Cyan
if (Test-Path $RAG_DIR) {
    Set-Location $RAG_DIR
    $result = & uv run python search.py "InterWork" 2>&1 | Select-String -Pattern "score=" | Select-Object -First 1
    if ($result) {
        Write-Host "Index:               Healthy (results returned)" -ForegroundColor Green
    } else {
        Write-Host "Index:               No results — may need reindex" -ForegroundColor Yellow
    }
} else {
    Write-Host "RAG directory NOT FOUND: $RAG_DIR" -ForegroundColor Red
}

Write-Host ""
Write-Host "--- uv environment ---" -ForegroundColor Cyan
& uv --version
& uv run python --version

Write-Host ""
Write-Host "To reindex:  .\rag_reindex.ps1"
Write-Host "To search:   .\rag_search.ps1 `"your query`""
Write-Host ""
