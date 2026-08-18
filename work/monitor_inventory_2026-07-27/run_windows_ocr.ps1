param(
    [Parameter(Mandatory = $true)][string]$ImageDirectory,
    [Parameter(Mandatory = $true)][string]$OutputJson
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Storage.FileAccessMode, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]

$asTaskMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() |
    Where-Object {
        $_.Name -eq 'AsTask' -and
        $_.IsGenericMethod -and
        $_.GetParameters().Count -eq 1
    } |
    Select-Object -First 1

function Await-Result {
    param(
        [Parameter(Mandatory = $true)]$AsyncOperation,
        [Parameter(Mandatory = $true)][Type]$ResultType
    )

    $task = $script:asTaskMethod.MakeGenericMethod($ResultType).Invoke($null, @($AsyncOperation))
    $task.GetAwaiter().GetResult()
}

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$files = Get-ChildItem -LiteralPath $ImageDirectory -File |
    Where-Object { $_.Extension -match '^\.(jpg|jpeg|png|heic)$' } |
    Sort-Object Name

$records = foreach ($image in $files) {
    $stream = $null
    $bitmap = $null
    try {
        $file = Await-Result ([Windows.Storage.StorageFile]::GetFileFromPathAsync($image.FullName)) ([Windows.Storage.StorageFile])
        $stream = Await-Result ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await-Result ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await-Result ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $result = Await-Result ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        [pscustomobject]@{
            file_name = $image.Name
            full_path = $image.FullName
            ocr_text = $result.Text
            error = $null
        }
    }
    catch {
        [pscustomobject]@{
            file_name = $image.Name
            full_path = $image.FullName
            ocr_text = $null
            error = $_.Exception.Message
        }
    }
    finally {
        if ($null -ne $bitmap) { $bitmap.Dispose() }
        if ($null -ne $stream) { $stream.Dispose() }
    }
}

$records | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath $OutputJson -Encoding UTF8
Write-Output "Processed $($records.Count) images"
