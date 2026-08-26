param(
    [switch]$ValidateOnly,
    [string]$SourceDirectory,
    [string]$DToolsExecutable,
    [string]$ProjectDirectory,
    [string]$ProjectName = "HoofCare_GL100E_G1"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
if (-not $SourceDirectory) {
    $SourceDirectory = Join-Path $RepositoryRoot "dist\HoofCare.DToolsBridge"
}
$InstallRoot = Join-Path $env:LOCALAPPDATA "HoofCare\DToolsBridge"

if ($ValidateOnly) {
    if (-not (Test-Path (Join-Path $RepositoryRoot "dtools\gl100e\bridge\allowlist.json"))) {
        throw "Missing allowlist.json"
    }
    Write-Output "VALIDATION_OK"
    exit 0
}

if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
    throw "Built Bridge directory not found: $SourceDirectory"
}

Add-Type -AssemblyName System.Windows.Forms
if (-not $DToolsExecutable) {
    $ExecutableDialog = New-Object System.Windows.Forms.OpenFileDialog
    $ExecutableDialog.Title = "Wybierz plik wykonywalny Kinco DTools"
    $ExecutableDialog.Filter = "Program Windows (*.exe)|*.exe"
    $ExecutableDialog.CheckFileExists = $true
    if ($ExecutableDialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
        throw "Kinco DTools executable selection was cancelled."
    }
    $DToolsExecutable = $ExecutableDialog.FileName
}
if (-not $ProjectDirectory) {
    $ProjectDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $ProjectDialog.Description = "Wybierz WYLACZNIE folder testowego projektu HoofCare_GL100E_G1"
    $ProjectDialog.ShowNewFolderButton = $false
    if ($ProjectDialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
        throw "Synthetic project directory selection was cancelled."
    }
    $ProjectDirectory = $ProjectDialog.SelectedPath
}
if (-not (Test-Path -LiteralPath $DToolsExecutable -PathType Leaf)) {
    throw "The selected Kinco DTools executable does not exist."
}
if (-not (Test-Path -LiteralPath $ProjectDirectory -PathType Container)) {
    throw "The selected synthetic project directory does not exist."
}

$CanonicalExecutable = (Resolve-Path -LiteralPath $DToolsExecutable).Path
$CanonicalProject = (Resolve-Path -LiteralPath $ProjectDirectory).Path
$ExecutableHash = (Get-FileHash -LiteralPath $CanonicalExecutable -Algorithm SHA256).Hash.ToLowerInvariant()
$BackupRoot = $null
if (Test-Path -LiteralPath $InstallRoot) {
    $BackupRoot = "$InstallRoot.backup.$(Get-Date -Format 'yyyyMMddHHmmss')"
    Move-Item -LiteralPath $InstallRoot -Destination $BackupRoot
}

try {
    New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null
    Copy-Item -Path (Join-Path $SourceDirectory "*") -Destination $InstallRoot -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $RepositoryRoot "dtools\gl100e\bridge\allowlist.json") -Destination (Join-Path $InstallRoot "allowlist.json") -Force
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "Run-DToolsBridge.cmd") -Destination (Join-Path $InstallRoot "Run-DToolsBridge.cmd") -Force
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "Run-DToolsBridge-Automation.cmd") -Destination (Join-Path $InstallRoot "Run-DToolsBridge-Automation.cmd") -Force
    New-Item -ItemType Directory -Path (Join-Path $InstallRoot "logs") -Force | Out-Null
    @{
        project = $ProjectName
        project_directory = $CanonicalProject
        executable = $CanonicalExecutable
        executable_sha256 = $ExecutableHash
    } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $InstallRoot "config.json") -Encoding UTF8
}
catch {
    if (Test-Path -LiteralPath $InstallRoot) {
        Move-Item -LiteralPath $InstallRoot -Destination "$InstallRoot.failed.$(Get-Date -Format 'yyyyMMddHHmmss')"
    }
    if ($BackupRoot -and (Test-Path -LiteralPath $BackupRoot)) {
        Move-Item -LiteralPath $BackupRoot -Destination $InstallRoot
    }
    throw
}

Write-Output "INSTALL_OK"
Write-Output $InstallRoot
