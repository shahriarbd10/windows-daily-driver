$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolRoot = Resolve-Path (Join-Path $ScriptDir "..")
$ExePath = Join-Path $ToolRoot "dist\ScreenshotManager.exe"

if (-not (Test-Path $ExePath)) {
    throw "Build output not found. Run scripts/build.ps1 first."
}

$InstallRoot = Join-Path $env:LOCALAPPDATA "DailyDriver\ScreenshotManager"
$InstallExe = Join-Path $InstallRoot "ScreenshotManager.exe"
$DesktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Screenshot Manager.lnk"
$StartMenuDir = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Daily Driver"
$StartMenuShortcut = Join-Path $StartMenuDir "Screenshot Manager.lnk"

New-Item -ItemType Directory -Path $InstallRoot -Force | Out-Null
New-Item -ItemType Directory -Path $StartMenuDir -Force | Out-Null
Copy-Item -Path $ExePath -Destination $InstallExe -Force

$Shell = New-Object -ComObject WScript.Shell

$Desktop = $Shell.CreateShortcut($DesktopShortcut)
$Desktop.TargetPath = $InstallExe
$Desktop.WorkingDirectory = $InstallRoot
$Desktop.IconLocation = "$InstallExe,0"
$Desktop.Save()

$StartMenu = $Shell.CreateShortcut($StartMenuShortcut)
$StartMenu.TargetPath = $InstallExe
$StartMenu.WorkingDirectory = $InstallRoot
$StartMenu.IconLocation = "$InstallExe,0"
$StartMenu.Save()

Write-Host "Installed Screenshot Manager to: $InstallRoot"
Write-Host "Shortcuts created on Desktop and Start Menu."
