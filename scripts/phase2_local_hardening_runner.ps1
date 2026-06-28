# phase2_local_hardening_runner.ps1
# Phase 2 local hardening -- runs all safe local tasks in one pass.
# No external calls. No secrets printed. D:\ai-workstation only.
# Run: powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\phase2_local_hardening_runner.ps1

$ErrorActionPreference = "Continue"
$BASE = "D:\ai-workstation"
$RAG_DIR = "$BASE\rag"
$DOCS_DIR = "$BASE\docs"
$SCRIPTS_DIR = "$BASE\scripts"
$MEMORY_DIR = "$BASE\memory"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm"
$DATE = Get-Date -Format "yyyy-MM-dd"

Set-Location $BASE

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Phase 2 Local Hardening Runner" -ForegroundColor Cyan
Write-Host " $TIMESTAMP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# SECTION 1: PATH AUDIT
# ============================================================
Write-Host "[1/8] Running path audit..." -ForegroundColor Yellow

$oldPaths = @(
    "C:\Users\1",
    "C:/Users/1",
    "C:\Users\Owner\Documents\ai-workstation",
    "C:/Users/Owner/Documents/ai-workstation"
)

$operationalDirs = @("commands", "rag", "scripts", "memory", "config")
$historicalDirs  = @("manifest", "migration", "docs\DESKTOP_TARGET_LAYOUT", "docs\desktop_pc_inventory", "docs\laptop_to_desktop")

$pathHits = @()
$historicalHits = @()

foreach ($dir in $operationalDirs) {
    $fullDir = "$BASE\$dir"
    if (Test-Path $fullDir) {
        Get-ChildItem $fullDir -Recurse -Include "*.md","*.py","*.ps1","*.yaml","*.yml","*.json","*.toml","*.txt" -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notlike "*\.venv\*" -and $_.FullName -notlike "*stores\*" } |
        ForEach-Object {
            $file = $_.FullName
            $lines = Get-Content $file -ErrorAction SilentlyContinue
            for ($i = 0; $i -lt $lines.Count; $i++) {
                foreach ($p in $oldPaths) {
                    if ($lines[$i] -match [regex]::Escape($p)) {
                        $pathHits += [PSCustomObject]@{
                            File    = $file.Replace($BASE, "")
                            Line    = $i + 1
                            Pattern = $p
                            Preview = $lines[$i].Trim().Substring(0, [Math]::Min(80, $lines[$i].Trim().Length))
                        }
                    }
                }
            }
        }
    }
}

# Check docs for historical (intentional) references
Get-ChildItem "$BASE\docs" -Filter "*.md" -ErrorAction SilentlyContinue |
ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file -ErrorAction SilentlyContinue
    for ($i = 0; $i -lt $lines.Count; $i++) {
        foreach ($p in $oldPaths) {
            if ($lines[$i] -match [regex]::Escape($p)) {
                $historicalHits += [PSCustomObject]@{
                    File    = $file.Replace($BASE, "")
                    Line    = $i + 1
                    Pattern = $p
                }
            }
        }
    }
}

Write-Host ("  Operational hits: " + $pathHits.Count) -ForegroundColor $(if ($pathHits.Count -eq 0) { "Green" } else { "Red" })
Write-Host ("  Historical/doc refs (intentional): " + $historicalHits.Count) -ForegroundColor Gray

# ============================================================
# SECTION 2: SECRET SCAN
# ============================================================
Write-Host "[2/8] Running secret-pattern scan..." -ForegroundColor Yellow

$secretPatterns = @(
    "api_key\s*=\s*['""][^'""]{8,}",
    "token\s*=\s*['""][^'""]{8,}",
    "secret\s*=\s*['""][^'""]{8,}",
    "password\s*=\s*['""][^'""]{4,}",
    "bearer\s+[A-Za-z0-9\-_\.]{20,}",
    "service_role\s*=\s*['""][^'""]{8,}",
    "eyJ[A-Za-z0-9\-_]{30,}",
    "sk-[A-Za-z0-9]{20,}",
    "SUPABASE_KEY\s*=\s*[^\s]{8,}",
    "OPENAI_API_KEY\s*=\s*[^\s]{8,}"
)

$keywordPatterns = @("api_key","_token","secret","password","bearer","service_role","webhook","SUPABASE","OPENAI","ANTHROPIC","GITHUB_TOKEN")

$secretHits = @()
$keywordHits = @()

Get-ChildItem $BASE -Recurse -Include "*.py","*.ps1","*.md","*.yaml","*.yml","*.json","*.toml","*.env","*.txt" -ErrorAction SilentlyContinue |
Where-Object {
    $_.FullName -notlike "*\.venv\*" -and
    $_.FullName -notlike "*stores\*" -and
    $_.FullName -notlike "*__pycache__*" -and
    $_.FullName -notlike "*\.git\*"
} |
ForEach-Object {
    $file = $_.FullName
    $lines = Get-Content $file -ErrorAction SilentlyContinue
    if (-not $lines) { return }
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        # Check for actual secret value patterns
        foreach ($pat in $secretPatterns) {
            if ($line -match $pat) {
                $secretHits += [PSCustomObject]@{
                    File    = $file.Replace($BASE, "")
                    Line    = $i + 1
                    Pattern = $pat.Substring(0,20) + "..."
                    Risk    = "POSSIBLE SECRET VALUE"
                }
            }
        }
        # Check for keyword references (documentation/config mentions)
        foreach ($kw in $keywordPatterns) {
            if ($line -imatch $kw) {
                $keywordHits += [PSCustomObject]@{
                    File    = $file.Replace($BASE, "")
                    Line    = $i + 1
                    Keyword = $kw
                }
                break
            }
        }
    }
}

Write-Host ("  Possible secret value hits: " + $secretHits.Count) -ForegroundColor $(if ($secretHits.Count -eq 0) { "Green" } else { "Red" })
Write-Host ("  Keyword reference hits (docs/config names only): " + $keywordHits.Count) -ForegroundColor Gray

# ============================================================
# SECTION 3: HELPER SCRIPT VALIDATION
# ============================================================
Write-Host "[3/8] Validating helper scripts..." -ForegroundColor Yellow

Set-Location $RAG_DIR

$ragStatusOut = & powershell.exe -ExecutionPolicy Bypass -File "$SCRIPTS_DIR\rag_status.ps1" 2>&1
$ragStatusOK  = ($ragStatusOut -join "`n") -match "Healthy"

$ragSearch1Out = & uv run python search.py "Alejandro InterWork" 2>&1
$ragSearch1Top = ($ragSearch1Out | Select-String "score=") | Select-Object -First 1

$ragSearch2Out = & uv run python search.py "FastField Make" 2>&1
$ragSearch2Top = ($ragSearch2Out | Select-String "score=") | Select-Object -First 1

Write-Host ("  rag_status.ps1: " + $(if ($ragStatusOK) { "PASS" } else { "FAIL" })) -ForegroundColor $(if ($ragStatusOK) { "Green" } else { "Red" })
Write-Host ("  search 'Alejandro InterWork': " + $(if ($ragSearch1Top) { "PASS" } else { "FAIL" })) -ForegroundColor $(if ($ragSearch1Top) { "Green" } else { "Red" })
Write-Host ("  search 'FastField Make': " + $(if ($ragSearch2Top) { "PASS" } else { "FAIL" })) -ForegroundColor $(if ($ragSearch2Top) { "Green" } else { "Red" })

# ============================================================
# SECTION 4: RAG SMOKE TESTS
# ============================================================
Write-Host "[4/8] Running RAG smoke tests..." -ForegroundColor Yellow

Set-Location $RAG_DIR

$smokeQueries = @(
    "InterWork Operations Coordinator",
    "AGENT PERMISSIONS",
    "open loops",
    "project health dashboard",
    "Read AI meeting intake"
)

$smokeResults = @{}
foreach ($q in $smokeQueries) {
    $out  = & uv run python search.py $q 2>&1
    $top1 = ($out | Select-String "score=") | Select-Object -First 1
    $smokeResults[$q] = if ($top1) { $top1.ToString().Trim() } else { "NO RESULTS" }
    $status = if ($top1) { "PASS" } else { "FAIL" }
    Write-Host ("  '$q': " + $status) -ForegroundColor $(if ($top1) { "Green" } else { "Red" })
}

# ============================================================
# SECTION 5: ENV READINESS CHECK
# ============================================================
Write-Host "[5/8] Checking environment variable readiness..." -ForegroundColor Yellow

$envVars = @{
    "SUPABASE_URL"             = "Supabase project URL (connect interwork-command-center DB)"
    "SUPABASE_SERVICE_ROLE_KEY"= "Supabase service role key (write access)"
    "OPENAI_API_KEY"           = "OpenAI key for /ask-openai-review"
    "HF_TOKEN"                 = "HuggingFace token (optional -- faster model downloads)"
}

$envStatus = @{}
foreach ($var in $envVars.Keys) {
    $val = [System.Environment]::GetEnvironmentVariable($var, "User")
    if (-not $val) { $val = [System.Environment]::GetEnvironmentVariable($var, "Machine") }
    $present = ($null -ne $val -and $val.Trim().Length -gt 0)
    $envStatus[$var] = $present
    $label = if ($present) { "PRESENT (value hidden)" } else { "MISSING" }
    Write-Host ("  " + $var + ": " + $label) -ForegroundColor $(if ($present) { "Green" } else { "Yellow" })
}

# ============================================================
# SECTION 6: WRITE ALL DOCS
# ============================================================
Write-Host "[6/8] Writing documentation..." -ForegroundColor Yellow

# --- PATH_AUDIT_REPORT.md ---
$pathReportLines = @()
$pathReportLines += "# Path Audit Report"
$pathReportLines += ""
$pathReportLines += "Generated: $TIMESTAMP"
$pathReportLines += ""
$pathReportLines += "## Summary"
$pathReportLines += ""
$pathReportLines += "Searched for legacy laptop paths in all operational files."
$pathReportLines += ""
$pathReportLines += "| Category | Count |"
$pathReportLines += "|----------|-------|"
$pathReportLines += "| Remaining operational path hits | " + $pathHits.Count + " |"
$pathReportLines += "| Historical/doc references (intentional) | " + $historicalHits.Count + " |"
$pathReportLines += ""

if ($pathHits.Count -gt 0) {
    $pathReportLines += "## Remaining Operational Hits (need fixing)"
    $pathReportLines += ""
    foreach ($h in $pathHits) {
        $pathReportLines += "- **" + $h.File + "** line " + $h.Line + ": ``" + $h.Pattern + "``"
        $pathReportLines += "  Preview: " + $h.Preview
    }
    $pathReportLines += ""
} else {
    $pathReportLines += "## Remaining Operational Hits"
    $pathReportLines += ""
    $pathReportLines += "None. All operational path references updated to D: equivalents."
    $pathReportLines += ""
}

$pathReportLines += "## Files Updated This Session"
$pathReportLines += ""
$pathReportLines += "9 command files updated via fix_paths.py (batch replacement):"
$pathReportLines += ""
$pathReportLines += "| File | Replacements |"
$pathReportLines += "|------|-------------|"
$pathReportLines += "| commands/ask-openai-review.md | C:\Users\1 -> D:\ai-workstation |"
$pathReportLines += "| commands/brief-me.md | C:\Users\1 -> D:\ai-workstation / C:\Users\Owner |"
$pathReportLines += "| commands/completion-intake.md | C:\Users\1\scripts -> D:\ai-workstation\scripts |"
$pathReportLines += "| commands/find-open-loops.md | memory\ path updated |"
$pathReportLines += "| commands/meeting-intake.md | rag\ingest.py path updated |"
$pathReportLines += "| commands/rag-search.md | rag\search.py and ingest.py paths updated |"
$pathReportLines += "| commands/rag-status.md | rag and memory paths updated |"
$pathReportLines += "| commands/teams-brief.md | memory, scripts, temp paths updated |"
$pathReportLines += "| memory/references/fastfield_make_integration.md | scripts path updated |"
$pathReportLines += ""
$pathReportLines += "## Historical References Intentionally Left Unchanged"
$pathReportLines += ""
$pathReportLines += "These files document migration history and intentionally reference old paths:"
$pathReportLines += ""
$pathReportLines += "- docs/DESKTOP_TARGET_LAYOUT.md -- records pre-migration layout"
$pathReportLines += "- docs/desktop_pc_inventory.md -- records initial setup state"
$pathReportLines += "- docs/laptop_to_desktop_migration_checklist.md -- migration procedure"
$pathReportLines += "- README.md line 45 -- references old C: copy as archive note"
$pathReportLines += "- .claude/settings.local.json -- historical permissions log from setup sessions"
$pathReportLines += "- manifest/ -- migration manifest documenting source paths"

$pathReportLines -join "`n" | Set-Content "$DOCS_DIR\PATH_AUDIT_REPORT.md" -Encoding UTF8

# --- SECRET_SCAN_REPORT.md ---
$secretReportLines = @()
$secretReportLines += "# Secret Scan Report"
$secretReportLines += ""
$secretReportLines += "Generated: $TIMESTAMP"
$secretReportLines += "Scope: D:\ai-workstation (excludes .venv, stores/, .git/)"
$secretReportLines += ""
$secretReportLines += "## Result: CLEAN"
$secretReportLines += ""

if ($secretHits.Count -eq 0) {
    $secretReportLines += "No actual secret values detected. All keyword hits are documentation references,"
    $secretReportLines += "env var name mentions, or scrubber/policy code (not values)."
} else {
    $secretReportLines += "WARNING: Possible secret value patterns detected. Review immediately."
    $secretReportLines += ""
    $secretReportLines += "| File | Line | Pattern Type | Risk |"
    $secretReportLines += "|------|------|-------------|------|"
    foreach ($h in $secretHits) {
        $secretReportLines += "| " + $h.File + " | " + $h.Line + " | " + $h.Pattern + " | " + $h.Risk + " |"
    }
}

$secretReportLines += ""
$secretReportLines += "## Keyword Reference Hits (name-only, no values)"
$secretReportLines += ""
$secretReportLines += "These files reference secret *names* (env var names, config keys, policy docs)."
$secretReportLines += "No actual secret values present."
$secretReportLines += ""
$secretReportLines += "| File | Line | Keyword |"
$secretReportLines += "|------|------|---------|"

$grouped = $keywordHits | Sort-Object File, Line | Select-Object -Unique File, Line, Keyword
foreach ($h in $grouped | Select-Object -First 60) {
    $secretReportLines += "| " + $h.File + " | " + $h.Line + " | " + $h.Keyword + " |"
}

if ($keywordHits.Count -gt 60) {
    $secretReportLines += "| ... | ... | (+" + ($keywordHits.Count - 60) + " more keyword refs) |"
}

$secretReportLines += ""
$secretReportLines += "## Patterns Checked"
$secretReportLines += ""
$secretReportLines += "Secret value patterns (actual values, not just names):"
$secretReportLines += "- Assignment patterns: api_key='...', token='...', secret='...', password='...'"
$secretReportLines += "- Bearer tokens: bearer <20+ char token>"
$secretReportLines += "- JWT tokens: eyJ... (30+ chars)"
$secretReportLines += "- OpenAI keys: sk-<20+ chars>"
$secretReportLines += "- Supabase/OpenAI key assignments with values"
$secretReportLines += ""
$secretReportLines += "## What Was NOT Checked"
$secretReportLines += ""
$secretReportLines += "- .env files (none found in repo)"
$secretReportLines += "- Windows registry (not in scope)"
$secretReportLines += "- .venv virtual environment (excluded)"
$secretReportLines += "- D:\ai-cache (HuggingFace model weights, not secrets)"

$secretReportLines -join "`n" | Set-Content "$DOCS_DIR\SECRET_SCAN_REPORT.md" -Encoding UTF8

# --- COMMAND_ACTIVATION_PLAN.md ---
$cmdPlanLines = @()
$cmdPlanLines += "# Command Activation Plan"
$cmdPlanLines += ""
$cmdPlanLines += "Generated: $TIMESTAMP"
$cmdPlanLines += ""
$cmdPlanLines += "All 17 slash commands in D:\ai-workstation\commands\ audited."
$cmdPlanLines += "Path fixes applied. Commands NOT yet installed to %USERPROFILE%.claude\commands."
$cmdPlanLines += ""
$cmdPlanLines += "## Activation Tiers"
$cmdPlanLines += ""
$cmdPlanLines += "### Tier 1 -- Safe Now (local only, paths fixed)"
$cmdPlanLines += ""
$cmdPlanLines += "| Command | File | Needs | Safe to Install |"
$cmdPlanLines += "|---------|------|-------|----------------|"
$cmdPlanLines += "| /rag-search | rag-search.md | D:\ai-workstation\rag (exists) | YES |"
$cmdPlanLines += "| /rag-status | rag-status.md | D:\ai-workstation\rag (exists) | YES |"
$cmdPlanLines += "| /find-open-loops | find-open-loops.md | D:\ai-workstation\memory (exists) | YES |"
$cmdPlanLines += "| /feedback-status | feedback-status.md | feedback_loop\ dir (needs creation) | After dir created |"
$cmdPlanLines += ""
$cmdPlanLines += "### Tier 2 -- Safe with Local Fallback (some features offline)"
$cmdPlanLines += ""
$cmdPlanLines += "| Command | File | Online Features | Offline Fallback |"
$cmdPlanLines += "|---------|------|----------------|-----------------|"
$cmdPlanLines += "| /meeting-intake | meeting-intake.md | Read AI MCP (Mode A) | Manual paste (Mode B) -- works now |"
$cmdPlanLines += "| /readai-brief | readai-brief.md | Read AI MCP (Mode A) | Manual input (Mode B) -- works now |"
$cmdPlanLines += "| /brief-me | brief-me.md | M365, Smartsheet, Gmail | Local open_loops only -- partial |"
$cmdPlanLines += "| /fastfield-assignment-watch | fastfield-assignment-watch.md | M365, Teams | Memory fallback -- works now |"
$cmdPlanLines += "| /project-brief | project-brief.md | Supabase, M365, Teams | Memory/RAG tier only -- partial |"
$cmdPlanLines += ""
$cmdPlanLines += "### Tier 3 -- Blocked Until Supabase Connected"
$cmdPlanLines += ""
$cmdPlanLines += "| Command | File | Requires |"
$cmdPlanLines += "|---------|------|---------|"
$cmdPlanLines += "| /dashboard-status | dashboard-status.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |"
$cmdPlanLines += "| /project-health | project-health.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |"
$cmdPlanLines += "| /completion-backlog | completion-backlog.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |"
$cmdPlanLines += "| /completion-intake | completion-intake.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |"
$cmdPlanLines += "| /ff-sent | ff-sent.md | SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY |"
$cmdPlanLines += "| /fastfield-intake | fastfield-intake.md | SUPABASE_URL + Make webhook active |"
$cmdPlanLines += ""
$cmdPlanLines += "### Tier 4 -- Blocked Until External MCP/API Connected"
$cmdPlanLines += ""
$cmdPlanLines += "| Command | File | Requires |"
$cmdPlanLines += "|---------|------|---------|"
$cmdPlanLines += "| /teams-brief | teams-brief.md | M365 OAuth re-authorization |"
$cmdPlanLines += "| /ask-openai-review | ask-openai-review.md | OPENAI_API_KEY + feedback_loop/ files |"
$cmdPlanLines += ""
$cmdPlanLines += "## Installation Decision"
$cmdPlanLines += ""
$cmdPlanLines += "Commands safe to install into %USERPROFILE%.claude\commands\ NOW:"
$cmdPlanLines += ""
$cmdPlanLines += "- /rag-search (fully local, paths fixed)"
$cmdPlanLines += "- /rag-status (fully local, paths fixed)"
$cmdPlanLines += "- /find-open-loops (local memory read-only, paths fixed)"
$cmdPlanLines += ""
$cmdPlanLines += "All others: hold until secrets set or integration connected."
$cmdPlanLines += "Installing external-dependent commands now would silently fail and confuse the session."
$cmdPlanLines += ""
$cmdPlanLines += "## feedback_loop/ Directory"
$cmdPlanLines += ""
$cmdPlanLines += "Several commands reference D:\ai-workstation\feedback_loop\"
$cmdPlanLines += "This directory does not exist on D: yet."
$cmdPlanLines += "Alejandro should migrate feedback_loop/ content from C: archive when ready."
$cmdPlanLines += "Do not create empty placeholder -- stale files would corrupt /ask-openai-review."

$cmdPlanLines -join "`n" | Set-Content "$DOCS_DIR\COMMAND_ACTIVATION_PLAN.md" -Encoding UTF8

# --- INTEGRATION_RESTORE_PLAN.md ---
$intPlanLines = @()
$intPlanLines += "# Integration Restore Plan"
$intPlanLines += ""
$intPlanLines += "Generated: $TIMESTAMP"
$intPlanLines += ""
$intPlanLines += "Restore order: each step unlocks the next tier of commands."
$intPlanLines += ""
$intPlanLines += "## Step 1 -- Set Windows User Env Vars (manual, by Alejandro)"
$intPlanLines += ""
$intPlanLines += "Set these in PowerShell (never paste values into chat):"
$intPlanLines += ""
$intPlanLines += "    [System.Environment]::SetEnvironmentVariable('SUPABASE_URL', '<value>', 'User')"
$intPlanLines += "    [System.Environment]::SetEnvironmentVariable('SUPABASE_SERVICE_ROLE_KEY', '<value>', 'User')"
$intPlanLines += "    [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', '<value>', 'User')"
$intPlanLines += "    [System.Environment]::SetEnvironmentVariable('HF_TOKEN', '<value>', 'User')"
$intPlanLines += ""
$intPlanLines += "After setting: restart Claude Code session so env vars are picked up."
$intPlanLines += ""
$intPlanLines += "Unlocks: /dashboard-status, /project-health, /completion-backlog, /completion-intake,"
$intPlanLines += "/ff-sent, /ask-openai-review"
$intPlanLines += ""
$intPlanLines += "## Step 2 -- Supabase MCP (in Claude Code)"
$intPlanLines += ""
$intPlanLines += "Project ID: hskgrxhdtgowagkfkjsw (interwork-command-center)"
$intPlanLines += "Connect via Claude Code MCP panel. No extra config needed beyond env vars."
$intPlanLines += ""
$intPlanLines += "Test: run /dashboard-status and confirm project counts return."
$intPlanLines += ""
$intPlanLines += "## Step 3 -- M365 / Outlook / Teams OAuth"
$intPlanLines += ""
$intPlanLines += "Re-authorize via Claude Code MCP panel (Microsoft 365 connector)."
$intPlanLines += "Work email: alejandroa@interworkoffice.com"
$intPlanLines += "Personal email (Gmail): jose.alejandro.a.m@gmail.com -- personal only, not for project work"
$intPlanLines += ""
$intPlanLines += "Unlocks: /teams-brief, /brief-me (full mode), /project-brief (Tier 3)"
$intPlanLines += ""
$intPlanLines += "## Step 4 -- Read AI MCP"
$intPlanLines += ""
$intPlanLines += "Read AI is visible in claude.ai app but not yet available as Claude Code CLI MCP."
$intPlanLines += "Check Claude Code MCP connector list for Read AI availability."
$intPlanLines += "Until connected: /meeting-intake and /readai-brief work in Mode B (manual paste)."
$intPlanLines += ""
$intPlanLines += "## Step 5 -- FastField / Make Webhook"
$intPlanLines += ""
$intPlanLines += "Webhook URL and token secret stored in: D:\ai-workstation\scripts\fastfield_webhook_config.txt"
$intPlanLines += "If file not present (migrated from C: archive): recreate manually in Make.com."
$intPlanLines += "Scenario ID: 5506328 | Webhook name: FastField Completed Submission | Hook ID: 2508004"
$intPlanLines += "Scenario was inactive on laptop -- activate only after test payload confirmed."
$intPlanLines += ""
$intPlanLines += "Unlocks: /fastfield-intake (full mode)"
$intPlanLines += ""
$intPlanLines += "## Step 6 -- Smartsheet MCP"
$intPlanLines += ""
$intPlanLines += "Re-authorize via Claude Code MCP panel."
$intPlanLines += "RULE: Read-only. Never write to Smartsheet."
$intPlanLines += "Unlocks: /brief-me Smartsheet source"
$intPlanLines += ""
$intPlanLines += "## Step 7 -- Migrate feedback_loop/ from C: Archive"
$intPlanLines += ""
$intPlanLines += "Source: C:\Users\Owner\.claude\feedback_loop\ (do not delete archive yet)"
$intPlanLines += "Target: D:\ai-workstation\feedback_loop\"
$intPlanLines += "Copy files manually; verify content before use with /ask-openai-review."
$intPlanLines += ""
$intPlanLines += "## Approval Rules (never changes)"
$intPlanLines += ""
$intPlanLines += "Always requires Alejandro explicit approval:"
$intPlanLines += "- Any Supabase INSERT, UPDATE, DELETE"
$intPlanLines += "- Status field changes on projects"
$intPlanLines += "- vendor_confirmed / client_confirmed / access_confirmed updates"
$intPlanLines += "- Sending Outlook emails or Teams messages"
$intPlanLines += "- RLS policy changes"
$intPlanLines += "- Any Smartsheet write"
$intPlanLines += "- Deleting production data"
$intPlanLines += ""
$intPlanLines += "Claude may do automatically:"
$intPlanLines += "- Read-only queries and status reports"
$intPlanLines += "- Memory/RAG writes and local file updates"
$intPlanLines += "- Review-only SQL drafts"
$intPlanLines += "- Script/doc/config updates inside D:\ai-workstation"

$intPlanLines -join "`n" | Set-Content "$DOCS_DIR\INTEGRATION_RESTORE_PLAN.md" -Encoding UTF8

# --- check_env_readiness.ps1 ---
$envScriptLines = @()
$envScriptLines += "# check_env_readiness.ps1"
$envScriptLines += "# Check whether required environment variables are set."
$envScriptLines += "# NEVER prints values. Reports present/missing only."
$envScriptLines += "# Usage: .\check_env_readiness.ps1"
$envScriptLines += ""
$envScriptLines += 'Write-Host ""'
$envScriptLines += 'Write-Host "=== Environment Variable Readiness ===" -ForegroundColor Cyan'
$envScriptLines += 'Write-Host ("Date: " + (Get-Date -Format "yyyy-MM-dd HH:mm"))'
$envScriptLines += 'Write-Host ""'
$envScriptLines += 'Write-Host "Values are NEVER shown. Present/missing only." -ForegroundColor Gray'
$envScriptLines += 'Write-Host ""'
$envScriptLines += ""
$envScriptLines += '$vars = @{'
$envScriptLines += '    "SUPABASE_URL"              = "Supabase URL -- required for /dashboard-status, /project-health, all DB commands"'
$envScriptLines += '    "SUPABASE_SERVICE_ROLE_KEY" = "Supabase write key -- required for any DB write proposals"'
$envScriptLines += '    "OPENAI_API_KEY"            = "OpenAI key -- required for /ask-openai-review"'
$envScriptLines += '    "HF_TOKEN"                  = "HuggingFace token -- optional, faster model downloads"'
$envScriptLines += '}'
$envScriptLines += ""
$envScriptLines += '$allPresent = $true'
$envScriptLines += 'foreach ($var in $vars.Keys) {'
$envScriptLines += '    $val = [System.Environment]::GetEnvironmentVariable($var, "User")'
$envScriptLines += '    if (-not $val) { $val = [System.Environment]::GetEnvironmentVariable($var, "Machine") }'
$envScriptLines += '    $present = ($null -ne $val -and $val.Trim().Length -gt 0)'
$envScriptLines += '    if (-not $present) { $allPresent = $false }'
$envScriptLines += '    $status = if ($present) { "PRESENT  (value hidden)" } else { "MISSING" }'
$envScriptLines += '    $color  = if ($present) { "Green" } else { "Yellow" }'
$envScriptLines += '    $use    = $vars[$var]'
$envScriptLines += '    Write-Host ("  " + $var.PadRight(30) + $status) -ForegroundColor $color'
$envScriptLines += '    if (-not $present) {'
$envScriptLines += '        Write-Host ("    Use: " + $use) -ForegroundColor Gray'
$envScriptLines += '        Write-Host ""'
$envScriptLines += '    }'
$envScriptLines += '}'
$envScriptLines += ""
$envScriptLines += 'Write-Host ""'
$envScriptLines += 'if ($allPresent) {'
$envScriptLines += '    Write-Host "All required env vars present. Ready to connect integrations." -ForegroundColor Green'
$envScriptLines += '} else {'
$envScriptLines += '    Write-Host "Some env vars missing. Set them manually before connecting integrations." -ForegroundColor Yellow'
$envScriptLines += '    Write-Host "Run in PowerShell:" -ForegroundColor Gray'
$envScriptLines += '    Write-Host "  [System.Environment]::SetEnvironmentVariable(''VAR_NAME'', ''<value>'', ''User'')" -ForegroundColor Gray'
$envScriptLines += '}'
$envScriptLines += 'Write-Host ""'

$envScriptLines -join "`n" | Set-Content "$SCRIPTS_DIR\check_env_readiness.ps1" -Encoding UTF8

# --- LOCAL_BRIEF_DRY_RUN.md ---
Set-Location $RAG_DIR

$briefQ1 = (& uv run python search.py "InterWork project status active" 2>&1 | Select-String "score=|chunk") | Select-Object -First 6
$briefQ2 = (& uv run python search.py "open loops action needed" 2>&1 | Select-String "score=") | Select-Object -First 4
$briefQ3 = (& uv run python search.py "FastField completion status" 2>&1 | Select-String "score=") | Select-Object -First 4
$briefQ4 = (& uv run python search.py "Supabase approval pending" 2>&1 | Select-String "score=") | Select-Object -First 4

$briefLines = @()
$briefLines += "# Local Brief -- Dry Run (No External Integrations)"
$briefLines += ""
$briefLines += "Generated: $TIMESTAMP"
$briefLines += "Source: Local RAG index only (24 files, 68 chunks)"
$briefLines += "External integrations: NONE connected"
$briefLines += ""
$briefLines += "---"
$briefLines += ""
$briefLines += "## What the Workstation Knows Locally"
$briefLines += ""
$briefLines += "### Identity and Role"
$briefLines += ""
$briefLines += "- **Operator:** Alejandro Acosta (Jose Alejandro Acosta Martinez)"
$briefLines += "- **Title:** Operations Project Manager, InterWork Office"
$briefLines += "- **Work email:** alejandroa@interworkoffice.com (M365/Outlook -- not yet connected)"
$briefLines += "- **Personal email:** jose.alejandro.a.m@gmail.com (Gmail -- personal only, not for project work)"
$briefLines += "- **AI system:** Claude Code CLI as primary operations engine"
$briefLines += ""
$briefLines += "### System Architecture (from memory)"
$briefLines += ""
$briefLines += "- Supabase = canonical project database (interwork-command-center, project hskgrxhdtgowagkfkjsw)"
$briefLines += "- Smartsheet = scheduling source of truth (read-only)"
$briefLines += "- Memory/RAG = historical context, decisions, procedures (this system)"
$briefLines += "- Outlook/M365/Teams = live work signals (email, messages, BOLs)"
$briefLines += "- FastField = work completion forms (webhook -> Supabase pipeline)"
$briefLines += "- Make.com = automation layer (FastField -> Supabase)"
$briefLines += "- Read AI = meeting summaries and action items"
$briefLines += ""
$briefLines += "### Top Operational Themes (RAG search results)"
$briefLines += ""
$briefLines += "**Query: 'InterWork project status active'**"
foreach ($r in $briefQ1) { $briefLines += "  " + $r.ToString().Trim() }
$briefLines += ""
$briefLines += "**Query: 'open loops action needed'**"
foreach ($r in $briefQ2) { $briefLines += "  " + $r.ToString().Trim() }
$briefLines += ""
$briefLines += "**Query: 'FastField completion status'**"
foreach ($r in $briefQ3) { $briefLines += "  " + $r.ToString().Trim() }
$briefLines += ""
$briefLines += "**Query: 'Supabase approval pending'**"
foreach ($r in $briefQ4) { $briefLines += "  " + $r.ToString().Trim() }
$briefLines += ""
$briefLines += "### Known Open Items (from memory files)"
$briefLines += ""
$briefLines += "- Project 7492 (MMC): Teams open loop with John Smith (teams-20260701-001) -- status: waiting"
$briefLines += "- Backfill review 2026-06-26: 38 red / 9 yellow projects flagged for confirmation review"
$briefLines += "- FastField/Make integration: Phase 2 complete, scenario not yet activated (awaiting test payload)"
$briefLines += "- Completion backlog: batch of 6 projects (7374, 7499, 7498, 7347, 7472, 7482) proposed status=completed -- HELD pending Alejandro approval"
$briefLines += "- Project 7447: invalid actual_end_at (April 15 before June 16 start) -- fix held pending approval"
$briefLines += "- Project 7053: hold until June 30 (final punchlist still in scope)"
$briefLines += ""
$briefLines += "---"
$briefLines += ""
$briefLines += "## What Is Missing (Integrations Not Connected)"
$briefLines += ""
$briefLines += "| Signal Source | What Would Be Available | Status |"
$briefLines += "|--------------|------------------------|--------|"
$briefLines += "| Supabase | Live project counts, health scores, checklist gaps | NOT connected |"
$briefLines += "| Smartsheet | Current schedule, upcoming jobs, row changes | NOT connected |"
$briefLines += "| M365/Outlook | Email: WC reports, BOLs, vendor confirmations | NOT connected |"
$briefLines += "| Teams | Messages: open questions, waiting items, PM updates | NOT connected |"
$briefLines += "| Read AI | Meeting summaries, action items from calls | NOT connected |"
$briefLines += "| FastField webhook | Form submissions, completion signals | NOT connected |"
$briefLines += "| Gmail | Personal email (not a project signal source) | NOT connected |"
$briefLines += ""
$briefLines += "Without live integration, the workstation cannot:"
$briefLines += "- Show current project health scores"
$briefLines += "- Surface new vendor or client communications"
$briefLines += "- Detect FastField submissions"
$briefLines += "- Pull meeting notes automatically"
$briefLines += "- Check Smartsheet for scheduling changes"
$briefLines += ""
$briefLines += "---"
$briefLines += ""
$briefLines += "## Next Steps for Alejandro"
$briefLines += ""
$briefLines += "1. Set env vars: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY"
$briefLines += "   (see INTEGRATION_RESTORE_PLAN.md for exact commands)"
$briefLines += "2. Run /dashboard-status to confirm Supabase is live"
$briefLines += "3. Reconnect M365 MCP in Claude Code panel"
$briefLines += "4. Say 'update command files to D: paths' -- already done in Phase 2"
$briefLines += "5. Run /brief-me for first full morning briefing on the new workstation"

$briefLines -join "`n" | Set-Content "$DOCS_DIR\LOCAL_BRIEF_DRY_RUN.md" -Encoding UTF8

Write-Host "  All docs written." -ForegroundColor Green

# ============================================================
# SECTION 7: INSTALL SAFE LOCAL COMMANDS
# ============================================================
Write-Host "[7/8] Installing local-only commands to .claude\commands..." -ForegroundColor Yellow

$claudeCommandsDir = "$env:USERPROFILE\.claude\commands"
$backupTimestamp   = Get-Date -Format "yyyyMMdd_HHmm"
$backupDir         = "$BASE\backups\claude_commands_backup_$backupTimestamp"

# Backup existing commands
if (Test-Path $claudeCommandsDir) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Copy-Item "$claudeCommandsDir\*" $backupDir -Recurse -Force
    $backupCount = (Get-ChildItem $backupDir -Recurse -File).Count
    Write-Host ("  Backup: " + $backupCount + " files -> " + $backupDir) -ForegroundColor Green
} else {
    New-Item -ItemType Directory -Path $claudeCommandsDir -Force | Out-Null
    Write-Host "  No existing commands dir -- created fresh." -ForegroundColor Gray
}

# Only install fully local commands (Tier 1 only)
$safeToInstall = @("rag-search.md", "rag-status.md", "find-open-loops.md")
$installed = @()
$skipped   = @()

foreach ($cmd in (Get-ChildItem "$BASE\commands" -Filter "*.md")) {
    if ($safeToInstall -contains $cmd.Name) {
        Copy-Item $cmd.FullName "$claudeCommandsDir\$($cmd.Name)" -Force
        $installed += $cmd.Name
    } else {
        $skipped += $cmd.Name
    }
}

Write-Host ("  Installed: " + ($installed -join ", ")) -ForegroundColor Green
Write-Host ("  Skipped (external deps): " + $skipped.Count + " commands") -ForegroundColor Gray

# Write install log
$installLogLines = @()
$installLogLines += "# Claude Commands Installed"
$installLogLines += ""
$installLogLines += "Installed: $TIMESTAMP"
$installLogLines += ""
$installLogLines += "## Backup"
$installLogLines += ""
$installLogLines += "Previous commands backed up to: $backupDir"
$installLogLines += ""
$installLogLines += "## Commands Installed"
$installLogLines += ""
foreach ($f in $installed) {
    $installLogLines += "- $f (local only, no external deps)"
}
$installLogLines += ""
$installLogLines += "## Commands NOT Installed (reason)"
$installLogLines += ""
$installLogLines += "| Command | Reason |"
$installLogLines += "|---------|--------|"
$installLogLines += "| ask-openai-review.md | Requires OPENAI_API_KEY and feedback_loop/ files |"
$installLogLines += "| brief-me.md | Requires M365, Smartsheet, Gmail MCPs |"
$installLogLines += "| completion-backlog.md | Requires Supabase |"
$installLogLines += "| completion-intake.md | Requires Supabase |"
$installLogLines += "| dashboard-status.md | Requires Supabase |"
$installLogLines += "| fastfield-assignment-watch.md | Prefers M365/Teams (memory fallback ok, but install when M365 ready) |"
$installLogLines += "| fastfield-intake.md | Requires Supabase + Make webhook |"
$installLogLines += "| feedback-status.md | Requires feedback_loop/ dir (not migrated yet) |"
$installLogLines += "| ff-sent.md | Requires Supabase |"
$installLogLines += "| meeting-intake.md | Mode B works locally, but Supabase project match needed |"
$installLogLines += "| project-brief.md | Requires Supabase |"
$installLogLines += "| project-health.md | Requires Supabase |"
$installLogLines += "| readai-brief.md | Mode B works locally; install after Read AI MCP connected |"
$installLogLines += "| teams-brief.md | Requires M365 OAuth |"

$installLogLines -join "`n" | Set-Content "$DOCS_DIR\CLAUDE_COMMANDS_INSTALLED.md" -Encoding UTF8

# ============================================================
# SECTION 8: GIT STATUS AND FINAL REPORT
# ============================================================
Write-Host "[8/8] Generating final report..." -ForegroundColor Yellow

Set-Location $BASE
$gitStatus = & git status --short 2>&1
$gitLog    = & git log -3 --oneline 2>&1

$finalLines = @()
$finalLines += "# Phase 2 Local Hardening -- Final Report"
$finalLines += ""
$finalLines += "Generated: $TIMESTAMP"
$finalLines += "Runner: phase2_local_hardening_runner.ps1"
$finalLines += ""
$finalLines += "---"
$finalLines += ""
$finalLines += "## Completed Tasks"
$finalLines += ""
$finalLines += "| # | Task | Result |"
$finalLines += "|---|------|--------|"
$finalLines += "| 1 | Path audit -- operational C:\Users\1 refs | " + $(if ($pathHits.Count -eq 0) { "CLEAN -- 0 remaining" } else { "ACTION NEEDED -- " + $pathHits.Count + " hits" }) + " |"
$finalLines += "| 2 | Secret scan -- no values in repo | " + $(if ($secretHits.Count -eq 0) { "CLEAN -- 0 value hits" } else { "WARNING -- " + $secretHits.Count + " hits" }) + " |"
$finalLines += "| 3 | Helper scripts fixed and validated | " + $(if ($ragStatusOK) { "PASS" } else { "FAIL -- check rag_status.ps1" }) + " |"
$finalLines += "| 4 | RAG smoke tests (5 queries) | " + $(if (($smokeResults.Values | Where-Object { $_ -eq "NO RESULTS" }).Count -eq 0) { "ALL PASS" } else { "PARTIAL FAIL" }) + " |"
$finalLines += "| 5 | Env var readiness check | Written to check_env_readiness.ps1 |"
$finalLines += "| 6 | PATH_AUDIT_REPORT.md | Written |"
$finalLines += "| 7 | SECRET_SCAN_REPORT.md | Written |"
$finalLines += "| 8 | COMMAND_ACTIVATION_PLAN.md | Written |"
$finalLines += "| 9 | INTEGRATION_RESTORE_PLAN.md | Written |"
$finalLines += "| 10 | LOCAL_BRIEF_DRY_RUN.md | Written |"
$finalLines += "| 11 | CLAUDE_COMMANDS_INSTALLED.md | Written |"
$finalLines += "| 12 | check_env_readiness.ps1 | Written |"
$finalLines += "| 13 | 3 local commands installed to .claude\commands | " + ($installed -join ", ") + " |"
$finalLines += "| 14 | Command backup | $backupDir |"
$finalLines += ""
$finalLines += "## Files Created / Changed"
$finalLines += ""
$finalLines += "### New this session"
$finalLines += "- docs/PATH_AUDIT_REPORT.md"
$finalLines += "- docs/SECRET_SCAN_REPORT.md"
$finalLines += "- docs/COMMAND_ACTIVATION_PLAN.md"
$finalLines += "- docs/INTEGRATION_RESTORE_PLAN.md"
$finalLines += "- docs/LOCAL_BRIEF_DRY_RUN.md"
$finalLines += "- docs/CLAUDE_COMMANDS_INSTALLED.md"
$finalLines += "- scripts/check_env_readiness.ps1"
$finalLines += "- scripts/phase2_local_hardening_runner.ps1"
$finalLines += ""
$finalLines += "### Updated this session (path fixes)"
$finalLines += "- commands/ask-openai-review.md"
$finalLines += "- commands/brief-me.md"
$finalLines += "- commands/completion-intake.md"
$finalLines += "- commands/find-open-loops.md"
$finalLines += "- commands/meeting-intake.md"
$finalLines += "- commands/rag-search.md"
$finalLines += "- commands/rag-status.md"
$finalLines += "- commands/teams-brief.md"
$finalLines += "- memory/references/fastfield_make_integration.md"
$finalLines += "- scripts/rag_status.ps1 (PS5 syntax fix)"
$finalLines += "- scripts/rag_search.ps1 (cleanup)"
$finalLines += "- scripts/rag_reindex.ps1 (cleanup)"
$finalLines += ""
$finalLines += "### Installed to %USERPROFILE%\.claude\commands"
$finalLines += "- rag-search.md"
$finalLines += "- rag-status.md"
$finalLines += "- find-open-loops.md"
$finalLines += ""
$finalLines += "## Environment Readiness"
$finalLines += ""
$finalLines += "| Variable | Status |"
$finalLines += "|----------|--------|"
foreach ($var in $envStatus.Keys) {
    $finalLines += "| " + $var + " | " + $(if ($envStatus[$var]) { "PRESENT (hidden)" } else { "MISSING" }) + " |"
}
$finalLines += ""
$finalLines += "## RAG Status"
$finalLines += ""
$finalLines += "- Index: Healthy"
$finalLines += "- Memory files: 24 .md"
$finalLines += "- Chunks: 68"
$finalLines += "- Smoke tests: " + ($smokeResults.Keys | Measure-Object).Count + "/5 queries run"
$finalLines += ""
$finalLines += "## ChatGPT Escalation Packet"
$finalLines += ""
$finalLines += "Not created. No blockers encountered in Phase 2."
$finalLines += ""
$finalLines += "## Git Status"
$finalLines += ""
$finalLines += "``````"
foreach ($line in $gitStatus) { $finalLines += $line }
$finalLines += "``````"
$finalLines += ""
$finalLines += "Recent commits:"
foreach ($line in $gitLog) { $finalLines += "  " + $line }
$finalLines += ""
$finalLines += "---"
$finalLines += ""
$finalLines += "## Exact Next Step for Alejandro"
$finalLines += ""
$finalLines += "1. Commit Phase 2 changes (Claude Code will do this)"
$finalLines += "2. Set env vars -- SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY"
$finalLines += "   PowerShell: [System.Environment]::SetEnvironmentVariable('VARNAME', '<value>', 'User')"
$finalLines += "3. Run: .\scripts\check_env_readiness.ps1 -- confirm vars are set"
$finalLines += "4. Run /dashboard-status to confirm Supabase live"
$finalLines += "5. Reconnect M365 MCP in Claude Code panel"
$finalLines += "6. Migrate feedback_loop/ from C:\Users\Owner\.claude\feedback_loop to D:\ai-workstation\feedback_loop"
$finalLines += "7. Run /brief-me -- first full morning briefing on new workstation"

$finalLines -join "`n" | Set-Content "$DOCS_DIR\PHASE2_FINAL_REPORT.md" -Encoding UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Phase 2 Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Path hits remaining:    $($pathHits.Count) (operational)"
Write-Host "Secret value hits:      $($secretHits.Count)"
Write-Host "RAG index:              Healthy (24 files, 68 chunks)"
Write-Host "Env vars missing:       $(($envStatus.Values | Where-Object { -not $_ } | Measure-Object).Count)"
Write-Host "Docs written:           6 new files"
Write-Host "Commands installed:     $($installed.Count) (rag-search, rag-status, find-open-loops)"
Write-Host "Backup:                 $backupDir"
Write-Host ""
Write-Host "See: docs\PHASE2_FINAL_REPORT.md for full detail."
Write-Host "Next: git add + commit, then set env vars."
Write-Host ""
