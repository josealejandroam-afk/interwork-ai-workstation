<#
.SYNOPSIS
    Read-only Microsoft Graph test via the official Microsoft.Graph PowerShell module.
    Device code flow. Never sends, modifies, deletes, archives, flags, or moves anything.

.PARAMETER DryRun
    Preview results only. No files written to disk.

.PARAMETER ProjectQuery
    Search query for project email search (default: "7510")

.PARAMETER CalendarDays
    Calendar window in days ahead (default: 14)

.PARAMETER MaxMessages
    Max inbox messages to read (default: 5)

.EXAMPLE
    # Dry-run (no files written)
    powershell -ExecutionPolicy Bypass -File scripts\graph_powershell_readonly_test.ps1 -DryRun

    # Full read with project search
    powershell -ExecutionPolicy Bypass -File scripts\graph_powershell_readonly_test.ps1 -ProjectQuery "7510" -MaxMessages 5
#>

[CmdletBinding()]
param(
    [switch]$DryRun,
    [string]$ProjectQuery  = "7510",
    [int]$CalendarDays     = 14,
    [int]$MaxMessages      = 5
)

$ErrorActionPreference = "Stop"

$TargetAccount  = "alejandroa@interworkoffice.com"
$RequiredScopes = @("User.Read", "Mail.Read", "Calendars.Read")
$RepoRoot       = Split-Path -Parent $PSScriptRoot
$MailDir        = Join-Path $RepoRoot "local_sources\graph_mail"
$CalDir         = Join-Path $RepoRoot "local_sources\graph_calendar"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
function Write-Section([string]$title) {
    Write-Host ""
    Write-Host "=== $title ===" -ForegroundColor Cyan
}

function Sanitize-Preview {
    param([string]$text, [int]$maxLen = 255)
    if (-not $text) { return "" }
    $clean = $text -replace 'https?://\S+', '[URL]'
    if ($clean.Length -gt $maxLen) { return $clean.Substring(0, $maxLen) + "..." }
    return $clean.Trim()
}

function Safe-Substring([string]$s, [int]$len) {
    if (-not $s) { return "" }
    if ($s.Length -le $len) { return $s }
    return $s.Substring(0, $len)
}

# ---------------------------------------------------------------------------
# 1. Check for Microsoft.Graph.Authentication module
# ---------------------------------------------------------------------------
Write-Section "Module Check"
$authMod = Get-Module Microsoft.Graph.Authentication -ListAvailable |
           Sort-Object Version -Descending |
           Select-Object -First 1

if (-not $authMod) {
    Write-Host "MISSING: Microsoft.Graph.Authentication is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "To install (run as yourself, Scope CurrentUser - no admin required):"
    Write-Host ""
    Write-Host "  # Full meta-module (includes all submodules):"
    Write-Host "  Install-Module Microsoft.Graph -Scope CurrentUser -Repository PSGallery -Force"
    Write-Host ""
    Write-Host "  # Or minimal install (auth + mail + calendar only):"
    Write-Host "  Install-Module Microsoft.Graph.Authentication -Scope CurrentUser -Repository PSGallery"
    Write-Host ""
    Write-Host "After install, re-run this script."
    exit 1
}

Write-Host "Found: $($authMod.Name) v$($authMod.Version) at $($authMod.ModuleBase)" -ForegroundColor Green

try {
    Import-Module Microsoft.Graph.Authentication -RequiredVersion $authMod.Version -ErrorAction Stop
    Write-Host "Module imported."
} catch {
    Write-Host "ERROR importing module: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ---------------------------------------------------------------------------
# 2. Connect - device code flow
# ---------------------------------------------------------------------------
Write-Section "Authentication (device code flow)"
Write-Host "Scopes requested: $($RequiredScopes -join ', ')"
Write-Host ""

try {
    Connect-MgGraph -Scopes $RequiredScopes -UseDeviceCode -NoWelcome -ErrorAction Stop
} catch {
    $errMsg = $_.Exception.Message
    Write-Host ""
    Write-Host "AUTH FAILED" -ForegroundColor Red
    Write-Host $errMsg

    if ($errMsg -match "AADSTS65001") {
        Write-Host ""
        Write-Host "TENANT POLICY: Admin consent is required for this application."
        Write-Host "The Microsoft Graph PowerShell app needs to be approved in Entra admin center."
        Write-Host "Recommended escalation to VMX/IT:"
        Write-Host "  - Request approval for 'Microsoft Graph PowerShell' service principal in"
        Write-Host "    Entra ID admin center (portal.azure.com > Enterprise Applications)"
        Write-Host "  - OR request the Claude Microsoft 365 connector (see docs/drafts/m365_access_request.md)"
        Write-Host "  - OR request a registered Graph app with Mail.Read + Calendars.Read scopes"
    } elseif ($errMsg -match "AADSTS1001010") {
        Write-Host ""
        Write-Host "APP NOT IN TENANT: Microsoft Graph PowerShell service principal not found."
        Write-Host "IT needs to add it in Entra admin center."
        Write-Host "Tenant ID (for IT reference): $($errMsg -replace '.*tenant:\s*([a-f0-9-]+).*','$1')"
    } elseif ($errMsg -match "AADSTS50158") {
        Write-Host ""
        Write-Host "CONDITIONAL ACCESS POLICY blocking device code flow."
        Write-Host "Escalate to IT."
    } elseif ($errMsg -match "AADSTS50076|AADSTS50079") {
        Write-Host ""
        Write-Host "MFA REQUIRED. Complete multi-factor authentication in the browser."
    }

    exit 1
}

# ---------------------------------------------------------------------------
# 3. Verify signed-in account
# ---------------------------------------------------------------------------
Write-Section "Account Verification"
$ctx = Get-MgContext

if (-not $ctx) {
    Write-Host "ERROR: Could not retrieve Graph context after login." -ForegroundColor Red
    exit 1
}

$signedIn = $ctx.Account
Write-Host "Signed in as:    $signedIn"
Write-Host "Tenant ID:       $($ctx.TenantId)"
Write-Host "Granted scopes:  $($ctx.Scopes -join ', ')"

if ($signedIn -ne $TargetAccount) {
    Write-Host ""
    Write-Host "WRONG ACCOUNT: Expected '$TargetAccount', got '$signedIn'." -ForegroundColor Red
    Write-Host "Disconnecting."
    Disconnect-MgGraph | Out-Null
    exit 1
}

Write-Host "Account verified." -ForegroundColor Green

# ---------------------------------------------------------------------------
# 4. Inbox read (top N)
# ---------------------------------------------------------------------------
Write-Section "Inbox Read (top $MaxMessages)"

$msgUri = ("https://graph.microsoft.com/v1.0/me/messages" +
    "?`$top=$MaxMessages" +
    "&`$select=subject,from,receivedDateTime,bodyPreview,hasAttachments,webLink" +
    "&`$orderby=receivedDateTime desc")

try {
    $msgResp = Invoke-MgGraphRequest -Uri $msgUri -Method GET
} catch {
    Write-Host "ERROR reading messages: $($_.Exception.Message)" -ForegroundColor Red
    Disconnect-MgGraph | Out-Null
    exit 1
}

$messages = $msgResp.value
Write-Host "Found $($messages.Count) message(s)."

$inboxLines = [System.Collections.Generic.List[string]]::new()
foreach ($msg in $messages) {
    $subject     = if ($msg.subject)                           { $msg.subject }                      else { "(no subject)" }
    $senderName  = if ($msg.from.emailAddress.name)            { $msg.from.emailAddress.name }        else { "?" }
    $senderAddr  = if ($msg.from.emailAddress.address)         { $msg.from.emailAddress.address }     else { "?" }
    $received    = if ($msg.receivedDateTime)                  { $msg.receivedDateTime.ToString() }   else { "?" }
    $receivedShort = if ($received.Length -ge 10)              { $received.Substring(0,10) }          else { $received }
    $hasAttach   = $msg.hasAttachments
    $preview     = Sanitize-Preview $msg.bodyPreview

    Write-Host "  [$receivedShort] $subject"
    Write-Host "    From: $senderName"
    Write-Host "    Preview: $(Safe-Substring $preview 120)..."

    $inboxLines.Add("Subject: $subject")
    $inboxLines.Add("From: $senderName <$senderAddr>")
    $inboxLines.Add("Received: $received")
    $inboxLines.Add("Has Attachments: $hasAttach")
    $inboxLines.Add("")
    $inboxLines.Add("Body Preview (sanitized):")
    $inboxLines.Add($preview)
    $inboxLines.Add("")
    $inboxLines.Add("---")
    $inboxLines.Add("")
}

# ---------------------------------------------------------------------------
# 5. Project search
# ---------------------------------------------------------------------------
Write-Section "Project Search: '$ProjectQuery'"

$cleanQuery  = $ProjectQuery.Trim('"')
$encodedQ    = [Uri]::EscapeDataString("`"$cleanQuery`"")
$searchUri   = ("https://graph.microsoft.com/v1.0/me/messages" +
    "?`$search=$encodedQ" +
    "&`$top=10" +
    "&`$select=subject,from,receivedDateTime,bodyPreview,hasAttachments")

try {
    $searchResp = Invoke-MgGraphRequest -Uri $searchUri -Method GET `
        -Headers @{ "ConsistencyLevel" = "eventual" }
} catch {
    Write-Host "Search error: $($_.Exception.Message)" -ForegroundColor Yellow
    $searchResp = @{ value = @() }
}

$searchMsgs = $searchResp.value
Write-Host "Found $($searchMsgs.Count) message(s) matching '$ProjectQuery'."

$searchLines = [System.Collections.Generic.List[string]]::new()
foreach ($msg in $searchMsgs) {
    $subject    = if ($msg.subject) { $msg.subject } else { "(no subject)" }
    $senderName = if ($msg.from.emailAddress.name) { $msg.from.emailAddress.name } else { "?" }
    $senderAddr = if ($msg.from.emailAddress.address) { $msg.from.emailAddress.address } else { "?" }
    $received   = if ($msg.receivedDateTime) { $msg.receivedDateTime.ToString() } else { "?" }
    $receivedShort = if ($received.Length -ge 10) { $received.Substring(0,10) } else { $received }
    $preview    = Sanitize-Preview $msg.bodyPreview

    Write-Host "  [$receivedShort] $subject"
    Write-Host "    From: $senderName"
    Write-Host "    Preview: $(Safe-Substring $preview 120)..."

    $searchLines.Add("Subject: $subject")
    $searchLines.Add("From: $senderName <$senderAddr>")
    $searchLines.Add("Received: $received")
    $searchLines.Add("")
    $searchLines.Add("Body Preview (sanitized):")
    $searchLines.Add($preview)
    $searchLines.Add("")
    $searchLines.Add("---")
    $searchLines.Add("")
}

# ---------------------------------------------------------------------------
# 6. Calendar
# ---------------------------------------------------------------------------
Write-Section "Calendar (next $CalendarDays days)"

$startDt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$endDt   = (Get-Date).AddDays($CalendarDays).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$calUri  = ("https://graph.microsoft.com/v1.0/me/calendarview" +
    "?startdatetime=$startDt" +
    "&enddatetime=$endDt" +
    "&`$top=20" +
    "&`$select=subject,start,end,organizer,location,bodyPreview,isAllDay" +
    "&`$orderby=start/dateTime")

try {
    $calResp = Invoke-MgGraphRequest -Uri $calUri -Method GET
} catch {
    Write-Host "Calendar error: $($_.Exception.Message)" -ForegroundColor Yellow
    $calResp = @{ value = @() }
}

$events = $calResp.value
Write-Host "Found $($events.Count) event(s)."

$calLines = [System.Collections.Generic.List[string]]::new()
foreach ($ev in $events) {
    $subject   = if ($ev.subject) { $ev.subject } else { "(no subject)" }
    $startTime = if ($ev.start.dateTime -and $ev.start.dateTime.Length -ge 16) {
                     $ev.start.dateTime.Substring(0,16).Replace("T"," ")
                 } else { "?" }
    $endTime   = if ($ev.end.dateTime -and $ev.end.dateTime.Length -ge 16) {
                     $ev.end.dateTime.Substring(0,16).Replace("T"," ")
                 } else { "?" }
    $organizer = if ($ev.organizer.emailAddress.name) { $ev.organizer.emailAddress.name } else { "?" }
    $location  = if ($ev.location.displayName) { $ev.location.displayName } else { "" }
    $allDay    = $ev.isAllDay
    $preview   = Sanitize-Preview $ev.bodyPreview 150

    Write-Host "  [$startTime] $subject"
    Write-Host "    Organizer: $organizer$(if($location){" | $location"})"

    $calLines.Add("Subject: $subject")
    $calLines.Add("Start: $startTime$(if($allDay){" (all day)"})")
    $calLines.Add("End: $endTime")
    $calLines.Add("Organizer: $organizer")
    if ($location) { $calLines.Add("Location: $location") }
    if ($preview)  { $calLines.Add(""); $calLines.Add("Preview: $preview") }
    $calLines.Add("")
    $calLines.Add("---")
    $calLines.Add("")
}

# ---------------------------------------------------------------------------
# 7. Save sanitized summaries (unless DryRun)
# ---------------------------------------------------------------------------
Write-Section "Output"
$today = (Get-Date).ToString("yyyy-MM-dd")

if ($DryRun) {
    Write-Host "[DRY RUN - no files written]"
    Write-Host "Would save to:"
    Write-Host "  $MailDir\inbox_top${MaxMessages}_${today}.txt"
    Write-Host "  $MailDir\project_search_${today}.txt"
    Write-Host "  $CalDir\calendar_${CalendarDays}days_${today}.txt"
} else {
    if ($inboxLines.Count -gt 0) {
        New-Item -ItemType Directory -Force -Path $MailDir | Out-Null
        $f = Join-Path $MailDir "inbox_top${MaxMessages}_${today}.txt"
        [System.IO.File]::WriteAllLines($f, $inboxLines, [System.Text.Encoding]::UTF8)
        Write-Host "Saved inbox:    $f"
    }

    if ($searchLines.Count -gt 0) {
        $safeQ = $ProjectQuery -replace '[^\w]','_'
        $searchDir = Join-Path $MailDir "project_$safeQ"
        New-Item -ItemType Directory -Force -Path $searchDir | Out-Null
        $f = Join-Path $searchDir "search_${today}.txt"
        [System.IO.File]::WriteAllLines($f, $searchLines, [System.Text.Encoding]::UTF8)
        Write-Host "Saved search:   $f"
    }

    if ($calLines.Count -gt 0) {
        New-Item -ItemType Directory -Force -Path $CalDir | Out-Null
        $f = Join-Path $CalDir "calendar_${CalendarDays}days_${today}.txt"
        [System.IO.File]::WriteAllLines($f, $calLines, [System.Text.Encoding]::UTF8)
        Write-Host "Saved calendar: $f"
    }
}

# ---------------------------------------------------------------------------
# 8. Disconnect
# ---------------------------------------------------------------------------
Disconnect-MgGraph | Out-Null
Write-Host ""
Write-Host "Disconnected from Microsoft Graph."
Write-Host "No emails were modified, sent, deleted, moved, archived, or flagged."
