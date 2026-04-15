$ErrorActionPreference = "Stop"

$InstallRoot = Join-Path $env:LOCALAPPDATA "DailyDriver\ScreenshotManager"
$DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Screenshot Manager.lnk"
$StartMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Daily Driver\Screenshot Manager.lnk"

Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $InstallRoot
Remove-Item -Force -ErrorAction SilentlyContinue $DesktopShortcut
Remove-Item -Force -ErrorAction SilentlyContinue $StartMenuShortcut

Write-Host "Screenshot Manager uninstalled."
