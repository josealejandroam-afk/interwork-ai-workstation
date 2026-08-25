param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9._-]+$')]
    [string]$MachineId,

    [ValidatePattern('^[A-Za-z0-9._-]+$')]
    [string]$AgentId = 'Human'
)

$repoRoot = (& git rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($repoRoot)) {
    throw 'Run this script from inside the InterWork AI Workstation repository.'
}

Push-Location $repoRoot
try {
    & git config --local core.hooksPath .githooks
    & git config --local interwork.machineId $MachineId
    & git config --local interwork.agentId $AgentId

    if ($LASTEXITCODE -ne 0) {
        throw 'Git could not save the machine signature configuration.'
    }

    Write-Host "Machine signature enabled: $AgentId@$MachineId"
    Write-Host 'New commits will include InterWork-Actor and InterWork-Machine trailers.'
    Write-Host "Use '$AgentId@$MachineId' as activity_log.actor for approved Supabase writes."
}
finally {
    Pop-Location
}

