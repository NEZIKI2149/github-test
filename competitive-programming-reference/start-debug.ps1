$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
Set-Location -LiteralPath $PSScriptRoot
if (Get-Command g++ -ErrorAction SilentlyContinue) {
    python -u (Join-Path $PSScriptRoot 'debug_bridge.py')
} else {
    $bridgePath = (& wsl.exe --exec wslpath -a (Join-Path $PSScriptRoot 'debug_bridge.py')).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'WSLが必要です。' }
    & wsl.exe --exec python3 -u $bridgePath
}
