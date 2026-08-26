@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\windows\dtools_bridge\Upgrade-DToolsBridge.ps1"
if errorlevel 1 (
  echo.
  echo Aktualizacja nie powiodla sie. Zamknij ChatGPT i uruchom ten plik ponownie.
  pause
  exit /b 1
)
exit /b 0
