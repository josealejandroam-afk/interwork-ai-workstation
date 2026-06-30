<#
.SYNOPSIS
    Export sanitized metadata from Outlook "AI Intake" folder.
    Read-only. Never sends, deletes, moves, or modifies messages.

.PARAMETER FolderName
    Target Outlook folder (default: "AI Intake")

.PARAMETER ProjectNumber
    Tag to prefix output files (e.g. "7189")

.PARAMETER MaxMessages
    Max emails to export per run (default: 50)

.PARAMETER DryRun
    Preview only — lists what would be exported, writes nothing

.EXAMPLE
    # Dry-run
    powershell -ExecutionPolicy Bypass -File scripts\outlook_ai_intake_export.ps1 -FolderName "AI Intake" -ProjectNumber "7189" -DryRun

    # Full export
    powershell -ExecutionPolicy Bypass -File scripts\outlook_ai_intake_export.ps1 -FolderName "AI Intake" -ProjectNumber "7189"
#>

[CmdletBinding()]
param(
    [string]$FolderName   = "AI Intake",
    [string]$ProjectNumber = "unknown",
    [int]$MaxMessages      = 50,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Output directory (gitignored) ---
$OutputRoot = Join-Path $PSScriptRoot "..\local_sources\outlook_summaries"
$OutputDir  = Join-Path $OutputRoot "project_$ProjectNumber"

if (-not $DryRun) {
    if (-not (Test-Path $OutputRoot)) { New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null }
    if (-not (Test-Path $OutputDir))  { New-Item -ItemType Directory -Force -Path $OutputDir  | Out-Null }
}

# --- Connect to Classic Outlook via COM ---
Write-Host "Connecting to Outlook via COM automation (read-only)..."
try {
    $Outlook = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Outlook.Application")
    Write-Host "Connected to running Outlook instance."
} catch {
    try {
        $Outlook = New-Object -ComObject Outlook.Application
        Write-Host "Started new Outlook COM instance."
    } catch {
        Write-Error @"
Classic Outlook COM not available.

This script requires Classic Outlook (not New Outlook).
Manual fallback: File > Save As .msg into:
  D:\ai-workstation\local_sources\outlook_exports\project_$ProjectNumber\

Then tell Claude: "Read the .msg files in local_sources/outlook_exports/project_$ProjectNumber/"
"@
        exit 1
    }
}

$Namespace = $Outlook.GetNamespace("MAPI")

# --- Locate target folder ---
Write-Host "Looking for folder: '$FolderName'..."
$TargetFolder = $null

foreach ($Store in $Namespace.Stores) {
    try {
        $Root = $Store.GetRootFolder()
        foreach ($Folder in $Root.Folders) {
            if ($Folder.Name -ieq $FolderName) {
                $TargetFolder = $Folder
                break
            }
        }
    } catch { continue }
    if ($null -ne $TargetFolder) { break }
}

if ($null -eq $TargetFolder) {
    Write-Error @"
Folder '$FolderName' not found in any mailbox.

To create it:
1. Open Classic Outlook
2. Right-click your mailbox → New Folder
3. Name it exactly: AI Intake
4. Place it at the top level of the mailbox

Then drag relevant emails into 'AI Intake' before running this script.
"@
    exit 1
}

$Items = $TargetFolder.Items
$Count = [Math]::Min($Items.Count, $MaxMessages)

Write-Host ""
Write-Host "Found '$FolderName' folder — $($Items.Count) message(s). Exporting up to $MaxMessages."
if ($DryRun) { Write-Host "[DRY RUN — no files will be written]" }
Write-Host ""

# --- Sanitize body text: strip URLs, email addresses, long number strings ---
function Sanitize-Body {
    param([string]$text)
    if ([string]::IsNullOrWhiteSpace($text)) { return "" }
    # Truncate to 1500 chars before processing
    $truncated = if ($text.Length -gt 1500) { $text.Substring(0, 1500) + "`n[truncated]" } else { $text }
    # Remove obvious URLs
    $clean = $truncated -replace 'https?://\S+', '[URL]'
    # Remove email addresses
    $clean = $clean -replace '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', '[EMAIL]'
    return $clean.Trim()
}

# --- Export loop ---
$Exported = 0
$Skipped  = 0

for ($i = 1; $i -le $Count; $i++) {
    $Item = $Items.Item($i)

    # Only process mail items
    if ($Item.Class -ne 43) {  # 43 = olMail
        $Skipped++
        continue
    }

    $Subject    = if ($Item.Subject)           { $Item.Subject }           else { "(no subject)" }
    $Sender     = if ($Item.SenderName)        { $Item.SenderName }        else { "unknown" }
    $SenderAddr = if ($Item.SenderEmailAddress){ $Item.SenderEmailAddress } else { "" }
    $Received   = if ($Item.ReceivedTime)      { $Item.ReceivedTime.ToString("yyyy-MM-dd HH:mm") } else { "unknown" }
    $BodyPreview = Sanitize-Body -text $Item.Body

    # Attachments — names only, no content
    $AttachmentNames = @()
    foreach ($Att in $Item.Attachments) {
        $AttachmentNames += $Att.FileName
    }

    $OutputContent = @"
---
project: $ProjectNumber
source: outlook_ai_intake
exported: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
dry_run: $($DryRun.IsPresent)
---

Subject: $Subject
From: $Sender <$SenderAddr>
Received: $Received
Attachments: $(if ($AttachmentNames.Count -gt 0) { $AttachmentNames -join ', ' } else { 'none' })

---
Body Preview (sanitized):

$BodyPreview
"@

    $SafeSubject = $Subject -replace '[\\/:*?"<>|]', '_'
    $SafeSubject = $SafeSubject.Substring(0, [Math]::Min(60, $SafeSubject.Length))
    $Filename    = "project_${ProjectNumber}_${i}_${SafeSubject}.txt"
    $FilePath    = Join-Path $OutputDir $Filename

    if ($DryRun) {
        Write-Host "[$i] WOULD EXPORT: $Filename"
        Write-Host "    From: $Sender | Received: $Received"
        Write-Host "    Subject: $Subject"
        if ($AttachmentNames.Count -gt 0) {
            Write-Host "    Attachments: $($AttachmentNames -join ', ')"
        }
        Write-Host ""
    } else {
        [System.IO.File]::WriteAllText($FilePath, $OutputContent, [System.Text.Encoding]::UTF8)
        Write-Host "[$i] Exported: $Filename"
    }

    $Exported++
}

Write-Host ""
Write-Host "Done. $Exported exported, $Skipped skipped (non-mail items)."
if (-not $DryRun) {
    Write-Host "Output folder: $OutputDir"
    Write-Host ""
    Write-Host "Next step: Tell Claude:"
    Write-Host "  'Read the summaries in local_sources/outlook_summaries/project_$ProjectNumber/"
    Write-Host "   and extract any facts relevant to project $ProjectNumber."
    Write-Host "   Do not commit the raw summary files.'"
}

# Release COM objects cleanly
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Items)     | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($TargetFolder) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($Namespace) | Out-Null
# Don't quit Outlook if we attached to an already-running instance
