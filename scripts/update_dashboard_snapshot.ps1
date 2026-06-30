# update_dashboard_snapshot.ps1
# Reads dashboard data from Supabase (read-only) and writes a markdown snapshot to
# memory/dashboard/CURRENT_DASHBOARD_STATUS.md
#
# SAFE GUARDS:
#   - Never writes to Supabase
#   - Never prints env var values
#   - Never writes secrets to any file
#   - Outputs markdown only to memory/dashboard/CURRENT_DASHBOARD_STATUS.md
#
# USAGE:
#   .\scripts\update_dashboard_snapshot.ps1
#   .\scripts\update_dashboard_snapshot.ps1 -ManualFallback

param(
    [switch]$ManualFallback
)

$OutputFile = "memory\dashboard\CURRENT_DASHBOARD_STATUS.md"
$Timestamp  = (Get-Date -Format "yyyy-MM-dd HH:mm")
$DateOnly   = (Get-Date -Format "yyyy-MM-dd")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Write-Safe {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Abort {
    param([string]$Reason)
    Write-Safe "[ABORT] $Reason" "Red"
    exit 1
}

# ---------------------------------------------------------------------------
# Env var check — presence only, never print values
# ---------------------------------------------------------------------------

$HasSupabaseUrl  = (-not [string]::IsNullOrEmpty($env:SUPABASE_URL))
$HasSupabaseKey  = (-not [string]::IsNullOrEmpty($env:SUPABASE_SERVICE_ROLE_KEY)) -or
                   (-not [string]::IsNullOrEmpty($env:SUPABASE_ANON_KEY))

$LiveMode = $HasSupabaseUrl -and $HasSupabaseKey -and (-not $ManualFallback)

if ($ManualFallback) {
    Write-Safe "[INFO] Manual fallback mode requested. Skipping Supabase." "Yellow"
} elseif (-not $HasSupabaseUrl) {
    Write-Safe "[WARN] SUPABASE_URL not set. Switching to manual fallback mode." "Yellow"
    $LiveMode = $false
} elseif (-not $HasSupabaseKey) {
    Write-Safe "[WARN] No Supabase key env var found (SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY). Switching to manual fallback." "Yellow"
    $LiveMode = $false
}

# ---------------------------------------------------------------------------
# Live Supabase read
# ---------------------------------------------------------------------------

if ($LiveMode) {
    Write-Safe "[INFO] Supabase env vars present. Attempting live read..." "Cyan"

    $Key = if ($env:SUPABASE_SERVICE_ROLE_KEY) { $env:SUPABASE_SERVICE_ROLE_KEY }
           else { $env:SUPABASE_ANON_KEY }

    $BaseUrl = $env:SUPABASE_URL.TrimEnd("/")
    $Headers = @{
        "apikey"        = $Key
        "Authorization" = "Bearer $Key"
        "Content-Type"  = "application/json"
    }

    function Invoke-SupabaseQuery {
        param([string]$Endpoint, [string]$Label)
        try {
            $Response = Invoke-RestMethod -Uri "$BaseUrl/rest/v1/$Endpoint" `
                -Headers $Headers -Method GET -ErrorAction Stop
            return $Response
        } catch {
            Write-Safe "[WARN] Supabase query failed for ${Label}: $($_.Exception.Message)" "Yellow"
            return $null
        }
    }

    # Count queries — use select=count with Prefer: count=exact header
    $CountHeaders = $Headers.Clone()
    $CountHeaders["Prefer"] = "count=exact"

    function Get-Count {
        param([string]$Table, [string]$Filter = "")
        $Url = "$BaseUrl/rest/v1/${Table}?select=project_number${Filter}"
        try {
            $Resp = Invoke-WebRequest -Uri $Url -Headers $CountHeaders -Method HEAD -ErrorAction Stop
            $Range = $Resp.Headers["Content-Range"]
            if ($Range -match "/(\d+)$") { return [int]$Matches[1] }
            return "?"
        } catch {
            return "?"
        }
    }

    $TodayFilter    = "&execution_date=eq.$DateOnly"
    $TomorrowDate   = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")
    $TomorrowFilter = "&execution_date=eq.$TomorrowDate"

    # Calculate start/end of current ISO week (Mon–Sun)
    $DayOfWeek      = [int](Get-Date).DayOfWeek
    $DaysToMon      = if ($DayOfWeek -eq 0) { -6 } else { 1 - $DayOfWeek }
    $WeekStart      = (Get-Date).AddDays($DaysToMon).ToString("yyyy-MM-dd")
    $WeekEnd        = (Get-Date).AddDays($DaysToMon + 6).ToString("yyyy-MM-dd")
    $WeekFilter     = "&execution_date=gte.$WeekStart&execution_date=lte.$WeekEnd"

    Write-Safe "[INFO] Querying counts..." "Cyan"

    $CountAll      = Get-Count "projects" "&status=in.(Scheduled,In Progress,Pending Approval,On Hold)"
    $CountToday    = Get-Count "projects" "$TodayFilter&status=in.(Scheduled,In Progress)"
    $CountTomorrow = Get-Count "projects" "$TomorrowFilter&status=in.(Scheduled)"
    $CountWeek     = Get-Count "projects" "$WeekFilter&status=in.(Scheduled,In Progress)"
    $CountAtRisk   = Get-Count "projects" "&readiness=eq.At Risk&status=in.(Scheduled,In Progress)"
    $CountAlerts   = $CountAtRisk  # Expand this if alert logic becomes more precise

    # Row-level queries
    $TodayRows    = Invoke-SupabaseQuery "projects?select=project_number,client,location,type,execution_date,start_time,execution_owner,status,readiness&execution_date=eq.$DateOnly&status=in.(Scheduled,In%20Progress)&order=project_number.asc" "today rows"
    $AtRiskRows   = Invoke-SupabaseQuery "projects?select=project_number,client,location,type,execution_date,execution_owner,status,readiness&readiness=eq.At Risk&status=in.(Scheduled,In%20Progress)&order=execution_date.asc&limit=50" "at-risk rows"
    $MissingPMRows = Invoke-SupabaseQuery "projects?select=project_number,client,location,execution_date,status&execution_owner=is.null&status=in.(Scheduled,In%20Progress)&order=execution_date.asc&limit=50" "missing PM rows"

    $SourceNote = "Live Supabase read (read-only, no writes)"

    Write-Safe "[OK] Live read complete." "Green"
}

# ---------------------------------------------------------------------------
# Manual fallback: prompt for current counts
# ---------------------------------------------------------------------------

if (-not $LiveMode) {
    Write-Safe ""
    Write-Safe "=== Manual Fallback Mode ===" "Yellow"
    Write-Safe "Enter the current values from the dashboard. Press Enter to accept defaults (blank = unknown)."
    Write-Safe ""

    function Prompt-Count {
        param([string]$Label, [string]$Default = "?")
        $Input = Read-Host "  $Label [$Default]"
        if ([string]::IsNullOrWhiteSpace($Input)) { return $Default }
        return $Input
    }

    $CountAll      = Prompt-Count "All (total active)" "?"
    $CountAlerts   = Prompt-Count "Alerts" "?"
    $CountAtRisk   = Prompt-Count "At Risk" "?"
    $CountToday    = Prompt-Count "Today" "?"
    $CountTomorrow = Prompt-Count "Tomorrow" "?"
    $CountWeek     = Prompt-Count "This Week" "?"

    $TodayRows     = $null
    $AtRiskRows    = $null
    $MissingPMRows = $null

    $SourceNote = "Manual fallback — values entered by operator. Needs live Supabase refresh."

    Write-Safe ""
    Write-Safe "[INFO] Using manually entered counts." "Yellow"
}

# ---------------------------------------------------------------------------
# Row formatters
# ---------------------------------------------------------------------------

function Format-TodayTable {
    param($Rows)
    if (-not $Rows -or $Rows.Count -eq 0) {
        return "_No row-level data captured — run live refresh._"
    }
    $Lines = @("| Project # | Client | Location | Type | Date | Time | Execution Owner | Status | Readiness |",
               "|---|---|---|---|---|---|---|---|---|")
    foreach ($r in $Rows) {
        $Lines += "| $($r.project_number) | $($r.client) | $($r.location) | $($r.type) | $($r.execution_date) | $($r.start_time) | $($r.execution_owner) | $($r.status) | $($r.readiness) |"
    }
    return $Lines -join "`n"
}

function Format-SimpleTable {
    param($Rows, [string]$EmptyMsg)
    if (-not $Rows -or $Rows.Count -eq 0) {
        return "_${EmptyMsg}_"
    }
    $Lines = @("| Project # | Client | Location | Type | Date | Execution Owner | Status | Readiness |",
               "|---|---|---|---|---|---|---|---|")
    foreach ($r in $Rows) {
        $Lines += "| $($r.project_number) | $($r.client) | $($r.location) | $($r.type) | $($r.execution_date) | $($r.execution_owner) | $($r.status) | $($r.readiness) |"
    }
    return $Lines -join "`n"
}

function Format-MissingPMTable {
    param($Rows)
    if (-not $Rows -or $Rows.Count -eq 0) {
        return "_No missing-PM rows captured — run live refresh._"
    }
    $Lines = @("| Project # | Client | Location | Date | Status |",
               "|---|---|---|---|---|")
    foreach ($r in $Rows) {
        $Lines += "| $($r.project_number) | $($r.client) | $($r.location) | $($r.execution_date) | $($r.status) |"
    }
    return $Lines -join "`n"
}

# ---------------------------------------------------------------------------
# Build markdown output
# ---------------------------------------------------------------------------

$TodayTable    = Format-TodayTable $TodayRows
$AtRiskTable   = Format-SimpleTable $AtRiskRows "No at-risk row data captured — run live refresh."
$MissingPMTable = Format-MissingPMTable $MissingPMRows

$Markdown = @"
# Current Dashboard Status
_AI-readable snapshot of the InterWork Operations Dashboard_

---

## Snapshot Metadata

| Field | Value |
|---|---|
| **Last Updated** | $Timestamp |
| **Data Source** | $SourceNote |
| **Snapshot Method** | $(if ($LiveMode) { "Automated — Supabase REST API (read-only)" } else { "Manual fallback" }) |
| **Needs Refresh** | $(if ($LiveMode) { "No — generated from live data" } else { "Yes — run ``scripts/update_dashboard_snapshot.ps1`` with Supabase env vars" }) |
| **Snapshot Age Warning** | If today's date is more than 1 day after Last Updated, treat counts as stale |

---

## Summary Counts

| Filter | Count |
|---|---|
| **All (active)** | $CountAll |
| **Alerts** | $CountAlerts |
| **At Risk** | $CountAtRisk |
| **Today** | $CountToday |
| **Tomorrow** | $CountTomorrow |
| **This Week** | $CountWeek |

---

## Today's Projects ($DateOnly)

$TodayTable

---

## At-Risk Projects

$AtRiskTable

---

## Missing PM Projects

$MissingPMTable

---

## Stale Scheduled Projects

_Not captured in this snapshot run. Requires a targeted Supabase query for past-dated Scheduled projects._
_Run live refresh to populate._

---

## Data Source Notes

- Source: $SourceNote
- Snapshot generated: $Timestamp
- For row-level tomorrow detail, run live refresh.
- This file is committed to GitHub and read by Claude Chat.
- Do not add secrets, tokens, or raw email content to this file.

---

## How to Refresh

``````powershell
# From repo root:
.\scripts\update_dashboard_snapshot.ps1
``````

Requires: ``SUPABASE_URL`` and ``SUPABASE_SERVICE_ROLE_KEY`` (or ``SUPABASE_ANON_KEY``) set in environment.
If env vars are missing, the script will enter manual fallback mode.
"@

# ---------------------------------------------------------------------------
# Write output file
# ---------------------------------------------------------------------------

$OutputPath = Join-Path (Get-Location) $OutputFile

try {
    $Markdown | Out-File -FilePath $OutputPath -Encoding utf8 -Force
    Write-Safe ""
    Write-Safe "[OK] Snapshot written to: $OutputFile" "Green"
    Write-Safe "[OK] Source: $SourceNote" "Green"
    Write-Safe ""
    Write-Safe "Next steps:" "Cyan"
    Write-Safe "  git add memory/dashboard/CURRENT_DASHBOARD_STATUS.md"
    Write-Safe "  git commit -m 'Refresh dashboard snapshot'"
    Write-Safe "  git push"
} catch {
    Abort "Failed to write output file: $($_.Exception.Message)"
}
