# check_env_readiness.ps1
# Check whether required environment variables are set.
# NEVER prints values. Reports present/missing only.
# Usage: .\check_env_readiness.ps1

Write-Host ""
Write-Host "=== Environment Variable Readiness ===" -ForegroundColor Cyan
Write-Host ("Date: " + (Get-Date -Format "yyyy-MM-dd HH:mm"))
Write-Host ""
Write-Host "Values are NEVER shown. Present/missing only." -ForegroundColor Gray
Write-Host ""

$vars = @{
    "SUPABASE_URL"              = "Supabase URL -- required for /dashboard-status, /project-health, all DB commands"
    "SUPABASE_SERVICE_ROLE_KEY" = "Supabase write key -- required for any DB write proposals"
    "OPENAI_API_KEY"            = "OpenAI key -- required for /ask-openai-review"
    "HF_TOKEN"                  = "HuggingFace token -- optional, faster model downloads"
}

$allPresent = $true
foreach ($var in $vars.Keys) {
    $val = [System.Environment]::GetEnvironmentVariable($var, "User")
    if (-not $val) { $val = [System.Environment]::GetEnvironmentVariable($var, "Machine") }
    $present = ($null -ne $val -and $val.Trim().Length -gt 0)
    if (-not $present) { $allPresent = $false }
    $status = if ($present) { "PRESENT  (value hidden)" } else { "MISSING" }
    $color  = if ($present) { "Green" } else { "Yellow" }
    $use    = $vars[$var]
    Write-Host ("  " + $var.PadRight(30) + $status) -ForegroundColor $color
    if (-not $present) {
        Write-Host ("    Use: " + $use) -ForegroundColor Gray
        Write-Host ""
    }
}

Write-Host ""
if ($allPresent) {
    Write-Host "All required env vars present. Ready to connect integrations." -ForegroundColor Green
} else {
    Write-Host "Some env vars missing. Set them manually before connecting integrations." -ForegroundColor Yellow
    Write-Host "Run in PowerShell:" -ForegroundColor Gray
    Write-Host "  [System.Environment]::SetEnvironmentVariable('VAR_NAME', '<value>', 'User')" -ForegroundColor Gray
}
Write-Host ""
