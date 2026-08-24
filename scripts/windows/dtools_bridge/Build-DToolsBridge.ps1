$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
$BuildRoot = Join-Path $RepositoryRoot ".build\dtools-bridge"
$VirtualEnvironment = Join-Path $BuildRoot "venv"
$Requirements = Join-Path $RepositoryRoot "dtools\gl100e\bridge\requirements-windows.txt"
$Spec = Join-Path $RepositoryRoot "dtools\gl100e\bridge\HoofCare.DToolsBridge.spec"

if (Test-Path $BuildRoot) {
    Remove-Item -LiteralPath $BuildRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $BuildRoot | Out-Null

Push-Location $RepositoryRoot
try {
    & py -3.13 -m venv $VirtualEnvironment
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.13 is required. Install it with: py install 3.13"
    }
    $Python = Join-Path $VirtualEnvironment "Scripts\python.exe"
    & $Python -m pip install --disable-pip-version-check --requirement $Requirements
    $env:PYTHONPATH = "src"
    & $Python -m compileall -q src tests scripts
    & $Python -m unittest tests.test_dtools_bridge_policy `
        tests.test_dtools_bridge_session `
        tests.test_dtools_bridge_audit `
        tests.test_dtools_bridge_controller `
        tests.test_dtools_bridge_server `
        tests.test_dtools_bridge_windows `
        tests.test_dtools_bridge_package -v
    if ($LASTEXITCODE -ne 0) { throw "Bridge tests failed." }
    & $Python -m PyInstaller --noconfirm --clean $Spec
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }
    Write-Output "BUILD_OK"
    Write-Output (Join-Path $RepositoryRoot "dist\HoofCare.DToolsBridge")
}
finally {
    Pop-Location
}
