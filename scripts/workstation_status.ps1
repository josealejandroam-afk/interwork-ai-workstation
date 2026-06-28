# workstation_status.ps1
# One-shot local status report for D:\ai-workstation.
# Reports only local state -- never connects externally, never prints secret values.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\workstation_status.ps1

$REPO = "D:\ai-workstation"
$RAG_DIR = "$REPO\rag"
$SCRIPTS_DIR = "$REPO\scripts"
$DOCS_DIR = "$REPO\docs"
$COMMANDS_USER = "C:\Users\Owner\.claude\commands"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Workstation Status -- D:\ai-workstation" -ForegroundColor Cyan
Write-Host " Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# --- Repo ---
Write-Host "--- Repository ---" -ForegroundColor Yellow
$repoParts = Split-Path $REPO -Leaf
if (Test-Path "$REPO\.git") {
    Push-Location $REPO
    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    $commit = git log -1 --oneline 2>$null
    $status = git status --short 2>$null
    Pop-Location
    Write-Host ("  Path:    " + $REPO)
    Write-Host ("  Branch:  " + $branch)
    Write-Host ("  Commit:  " + $commit)
    if ($status) {
        Write-Host ("  Uncommitted changes: YES") -ForegroundColor Yellow
    } else {
        Write-Host ("  Working tree: Clean") -ForegroundColor Green
    }
} else {
    Write-Host ("  WARNING: No .git found at " + $REPO) -ForegroundColor Red
}
Write-Host ""

# --- RAG Index ---
Write-Host "--- RAG Index ---" -ForegroundColor Yellow
$chromaPath = "$RAG_DIR\stores\chroma"
$metaPath   = "$RAG_DIR\stores\metadata.sqlite"
$memoryPath = "$REPO\memory"

$mdCount = 0
if (Test-Path $memoryPath) {
    $mdCount = (Get-ChildItem -Path $memoryPath -Filter "*.md" -Recurse -ErrorAction SilentlyContinue).Count
}

if (Test-Path $chromaPath) {
    Write-Host "  ChromaDB store: Found" -ForegroundColor Green
} else {
    Write-Host "  ChromaDB store: NOT FOUND -- run rag_reindex.ps1" -ForegroundColor Red
}

if (Test-Path $metaPath) {
    $metaKb = [math]::Round((Get-Item $metaPath).Length / 1024)
    Write-Host ("  SQLite metadata: Found (" + $metaKb + " KB)") -ForegroundColor Green
} else {
    Write-Host "  SQLite metadata: NOT FOUND" -ForegroundColor Yellow
}

Write-Host ("  Memory files (.md): " + $mdCount)

# Quick health test via uv
if (Test-Path "$RAG_DIR\search.py") {
    Push-Location $RAG_DIR
    $ragOut = uv run python search.py "workstation status check" 2>&1 | Out-String
    Pop-Location
    if ($ragOut -match "score=") {
        Write-Host "  Index health:   Healthy (results returned)" -ForegroundColor Green
    } else {
        Write-Host "  Index health:   NO RESULTS -- may need reindex" -ForegroundColor Yellow
    }
} else {
    Write-Host "  search.py: NOT FOUND" -ForegroundColor Red
}
Write-Host ""

# --- Environment Variables ---
Write-Host "--- Environment Variables (present/missing only, no values) ---" -ForegroundColor Yellow

$vars = @(
    @{ Name = "SUPABASE_URL";              Required = $true  },
    @{ Name = "SUPABASE_SERVICE_ROLE_KEY"; Required = $true  },
    @{ Name = "OPENAI_API_KEY";            Required = $true  },
    @{ Name = "HF_TOKEN";                  Required = $false }
)

$allRequired = $true
foreach ($v in $vars) {
    $val = [System.Environment]::GetEnvironmentVariable($v.Name, "User")
    $present = ($null -ne $val -and $val.Trim().Length -gt 0)
    $label = if ($v.Required) { "[required]" } else { "[optional]" }
    if ($present) {
        Write-Host ("  " + $v.Name.PadRight(28) + " PRESENT  (value hidden)  " + $label) -ForegroundColor Green
    } else {
        $color = if ($v.Required) { "Red" } else { "Gray" }
        Write-Host ("  " + $v.Name.PadRight(28) + " MISSING                  " + $label) -ForegroundColor $color
        if ($v.Required) { $allRequired = $false }
    }
}

if ($allRequired) {
    Write-Host "  All required env vars present." -ForegroundColor Green
} else {
    Write-Host "  Some required env vars missing. Run set_required_env_vars_interactive.ps1 then restart Claude Code." -ForegroundColor Yellow
}
Write-Host ""

# --- Installed Local Command Files ---
Write-Host "--- Installed Claude Code Commands ---" -ForegroundColor Yellow
$localCommands = @("rag-search.md", "rag-status.md", "find-open-loops.md")
foreach ($cmd in $localCommands) {
    $path = "$COMMANDS_USER\$cmd"
    if (Test-Path $path) {
        Write-Host ("  " + $cmd.PadRight(24) + " INSTALLED") -ForegroundColor Green
    } else {
        Write-Host ("  " + $cmd.PadRight(24) + " NOT FOUND at $path") -ForegroundColor Yellow
    }
}
Write-Host ""

# --- Escalation Packet ---
Write-Host "--- Escalation Packet ---" -ForegroundColor Yellow
$packetPath = "$DOCS_DIR\CHATGPT_ESCALATION_PACKET.md"
if (Test-Path $packetPath) {
    $packetMtime = (Get-Item $packetPath).LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    Write-Host ("  CHATGPT_ESCALATION_PACKET.md: EXISTS (last modified " + $packetMtime + ")") -ForegroundColor Yellow
    Write-Host "  Review this file -- an unresolved blocker may be waiting." -ForegroundColor Yellow
} else {
    Write-Host "  CHATGPT_ESCALATION_PACKET.md: Not present (no active blockers)" -ForegroundColor Green
}
Write-Host ""

# --- Next Recommended Step ---
Write-Host "--- Next Recommended Step ---" -ForegroundColor Yellow
if (-not $allRequired) {
    Write-Host "  1. Run set_required_env_vars_interactive.ps1 in a local PowerShell window" -ForegroundColor Cyan
    Write-Host "     powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1" -ForegroundColor Gray
    Write-Host "  2. Restart Claude Code after setting env vars" -ForegroundColor Cyan
    Write-Host "  3. Run /dashboard-status to test Supabase connection" -ForegroundColor Cyan
} else {
    Write-Host "  Env vars are set. Restart Claude Code if not done, then run /dashboard-status." -ForegroundColor Cyan
}
Write-Host ""
Write-Host "  For full return sequence: docs\FIRST_DAY_RUNBOOK.md" -ForegroundColor Gray
Write-Host "  For action queue:         docs\NEXT_ACTION_QUEUE.md" -ForegroundColor Gray
Write-Host "  For command tiers:        docs\SAFE_COMMANDS_REFERENCE.md" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " End of status report" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
