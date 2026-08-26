@echo off
setlocal
set "BRIDGE_ROOT=%~dp0"
powershell.exe -NoProfile -Command "$c = Get-Content -LiteralPath '%BRIDGE_ROOT%config.json' -Raw | ConvertFrom-Json; & '%BRIDGE_ROOT%HoofCare.DToolsBridge.exe' --project $c.project --project-directory $c.project_directory --executable $c.executable --executable-sha256 $c.executable_sha256 --allowlist '%BRIDGE_ROOT%allowlist.json' --logs '%BRIDGE_ROOT%logs'"
exit /b %ERRORLEVEL%
