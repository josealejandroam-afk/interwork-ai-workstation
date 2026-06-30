# regenerate_client_pack.ps1
# Usage: .\scripts\regenerate_client_pack.ps1 -Client marsh_mclennan
# Prints the command to give Claude Code for regenerating a client knowledge pack.
# Claude Code does the actual writing — this script just surfaces the right prompt.

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet(
        "marsh_mclennan",
        "radian",
        "bentley_systems",
        "rothman_orthopaedics",
        "all"
    )]
    [string]$Client = "all"
)

$clients = @(
    "marsh_mclennan",
    "radian",
    "bentley_systems",
    "rothman_orthopaedics"
)

if ($Client -ne "all") {
    $clients = @($Client)
}

Write-Host ""
Write-Host "=== Regenerate Client Knowledge Pack ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Give Claude Code the following prompt:" -ForegroundColor Yellow
Write-Host ""

foreach ($c in $clients) {
    Write-Host "---" -ForegroundColor DarkGray
    Write-Host "Regenerate the client knowledge pack for $c." -ForegroundColor White
    Write-Host "Read memory/clients/$c/CLIENT_CONTEXT.md and all project cards under memory/clients/$c/projects/." -ForegroundColor White
    Write-Host "Write the updated pack to claude_project_packs/${c}_knowledge_pack.md." -ForegroundColor White
    Write-Host "Commit with message: 'Regenerate $c knowledge pack'" -ForegroundColor White
    Write-Host ""
}

Write-Host "After Claude Code writes and commits the pack(s):" -ForegroundColor Yellow
Write-Host "1. Pull latest on any other machine"
Write-Host "2. Open the .md file from claude_project_packs/"
Write-Host "3. Upload it to the matching Claude Chat Project"
Write-Host ""
