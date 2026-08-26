$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
$SourceDirectory = Join-Path $RepositoryRoot "dist\HoofCare.DToolsBridge"
$Allowlist = Join-Path $RepositoryRoot "dtools\gl100e\bridge\allowlist.json"
$InstallRoot = Join-Path $env:LOCALAPPDATA "HoofCare\DToolsBridge"
$Config = Join-Path $InstallRoot "config.json"

if (-not (Test-Path -LiteralPath $Config -PathType Leaf)) {
    throw "EXISTING_CONFIG_REQUIRED"
}
if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
    throw "BUILD_OUTPUT_REQUIRED"
}
if (-not (Test-Path -LiteralPath $Allowlist -PathType Leaf)) {
    throw "ALLOWLIST_REQUIRED"
}

Copy-Item -Path (Join-Path $SourceDirectory "*") -Destination $InstallRoot -Recurse -Force
Copy-Item -LiteralPath $Allowlist -Destination (Join-Path $InstallRoot "allowlist.json") -Force
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "Run-DToolsBridge.cmd") -Destination (Join-Path $InstallRoot "Run-DToolsBridge.cmd") -Force
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "Run-DToolsBridge-Automation.cmd") -Destination (Join-Path $InstallRoot "Run-DToolsBridge-Automation.cmd") -Force
New-Item -ItemType Directory -Path (Join-Path $InstallRoot "logs") -Force | Out-Null

Write-Output "UPGRADE_OK"
