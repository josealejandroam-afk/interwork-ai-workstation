[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._ -]{0,99}$')]
    [string]$Label,

    [string]$OutputDirectory = (Join-Path $env:LOCALAPPDATA 'InterWork\LocalExecutor\credential-requests'),

    [ValidateSet('User', 'Process')]
    [string]$EnvironmentTarget = 'User',

    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$variableName = 'INTERWORK_QUEUE_SUBMIT_TOKEN'
$existing = [Environment]::GetEnvironmentVariable($variableName, $EnvironmentTarget)
if (-not $Force -and -not [string]::IsNullOrWhiteSpace($existing)) {
    throw "$variableName already exists for this Windows user. Use -Force only when intentionally rotating it."
}

$random = [Security.Cryptography.RandomNumberGenerator]::Create()
$bytes = New-Object byte[] 32
$random.GetBytes($bytes)
$body = [Convert]::ToBase64String($bytes).TrimEnd('=').Replace('+', '-').Replace('/', '_')
$token = "iwq_submit_$body"

$sha = [Security.Cryptography.SHA256]::Create()
$hash = [Convert]::ToHexString(
    $sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($token))
).ToLowerInvariant()

[Environment]::SetEnvironmentVariable($variableName, $token, $EnvironmentTarget)

$safeLabel = $Label.Replace("'", "''")
$safeFile = ($Label -replace '[^A-Za-z0-9._-]', '-').Trim('-')
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$outputPath = Join-Path $OutputDirectory "$timestamp-$safeFile.sql"

$sql = @"
-- Review and run manually in the Supabase SQL editor.
-- Contains only a SHA-256 credential hash, never the plaintext token.
insert into private.local_executor_queue_tokens (token_hash, token_role, label)
values (decode('$hash', 'hex'), 'submitter', '$safeLabel');
"@

[IO.File]::WriteAllText($outputPath, $sql, [Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Label = $Label
    CredentialRole = 'submitter'
    EnvironmentTarget = $EnvironmentTarget
    SqlRequestPath = $outputPath
    PlaintextWrittenToDisk = $false
}
