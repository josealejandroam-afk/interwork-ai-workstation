# set_required_env_vars_interactive.ps1
# Interactively set required environment variables for D:\ai-workstation integrations.
#
# RULES:
#   - Run this script locally in PowerShell only. Never paste secrets into Claude chat.
#   - Values are read with Read-Host -AsSecureString and never printed.
#   - All variables are set at User scope only (not Machine).
#   - This script does NOT connect to any external service.
#
# Usage (run as yourself, not as admin):
#   powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\set_required_env_vars_interactive.ps1
#
# After running: restart Claude Code so the new env vars are picked up.
# Verify with: powershell -ExecutionPolicy Bypass -File D:\ai-workstation\scripts\check_env_readiness.ps1

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Interactive Env Var Setup -- D:\ai-workstation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "WARNING: Run this script locally only." -ForegroundColor Yellow
Write-Host "         DO NOT paste secret values into Claude chat." -ForegroundColor Yellow
Write-Host "         Values entered here are NEVER printed or logged." -ForegroundColor Yellow
Write-Host ""
Write-Host "This script sets the following User-scoped environment variables:" -ForegroundColor Gray
Write-Host "  SUPABASE_URL               -- Supabase project URL" -ForegroundColor Gray
Write-Host "  SUPABASE_SERVICE_ROLE_KEY  -- Supabase service role key (write access)" -ForegroundColor Gray
Write-Host "  OPENAI_API_KEY             -- OpenAI API key" -ForegroundColor Gray
Write-Host "  HF_TOKEN                   -- HuggingFace token (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Enter to skip any variable and leave it unchanged." -ForegroundColor Gray
Write-Host ""

function Set-EnvVarSecure {
    param(
        [string]$VarName,
        [string]$Description,
        [switch]$Optional
    )

    $existing = [System.Environment]::GetEnvironmentVariable($VarName, "User")
    $hasExisting = ($null -ne $existing -and $existing.Trim().Length -gt 0)

    if ($hasExisting) {
        Write-Host ("  " + $VarName + ": already set (value hidden)") -ForegroundColor Green
        $overwrite = Read-Host ("  Overwrite? (y/N)")
        if ($overwrite -ne "y" -and $overwrite -ne "Y") {
            Write-Host ("  Keeping existing value for " + $VarName) -ForegroundColor Gray
            return
        }
    } else {
        $optLabel = if ($Optional) { " (optional -- press Enter to skip)" } else { " (required)" }
        Write-Host ("  " + $VarName + $optLabel) -ForegroundColor $(if ($Optional) { "Gray" } else { "Yellow" })
        Write-Host ("  Purpose: " + $Description) -ForegroundColor Gray
    }

    $secure = Read-Host ("  Enter value for " + $VarName) -AsSecureString

    # Convert SecureString to plain text only to check length -- value never stored in a variable
    $bstr   = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    $length = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr).Length
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)

    if ($length -eq 0) {
        Write-Host ("  Skipped " + $VarName) -ForegroundColor Gray
        return
    }

    # Set via SecureString -> BSTR -> plain for SetEnvironmentVariable only
    $bstr2 = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    $plain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr2)
    [System.Environment]::SetEnvironmentVariable($VarName, $plain, "User")
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr2)
    $plain = $null

    Write-Host ("  Set: " + $VarName + " (" + $length + " chars, value hidden)") -ForegroundColor Green
    Write-Host ""
}

# Required variables
Set-EnvVarSecure -VarName "SUPABASE_URL" `
    -Description "Supabase project URL (e.g. https://<id>.supabase.co). Find in Supabase dashboard > Settings > API."

Set-EnvVarSecure -VarName "SUPABASE_SERVICE_ROLE_KEY" `
    -Description "Supabase service role key. Find in Supabase dashboard > Settings > API > service_role. Keep secret."

Set-EnvVarSecure -VarName "OPENAI_API_KEY" `
    -Description "OpenAI API key (sk-...). Find at platform.openai.com > API Keys."

# Optional variables
Set-EnvVarSecure -VarName "HF_TOKEN" `
    -Description "HuggingFace token. Speeds up model downloads. Find at huggingface.co > Settings > Access Tokens." `
    -Optional

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Done. Verifying readiness..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Run check_env_readiness to confirm
& powershell.exe -ExecutionPolicy Bypass -File "D:\ai-workstation\scripts\check_env_readiness.ps1"

Write-Host ""
Write-Host "NEXT STEP: Restart Claude Code so the new env vars are loaded." -ForegroundColor Yellow
Write-Host "Then run /dashboard-status to test Supabase connection." -ForegroundColor Gray
Write-Host ""
