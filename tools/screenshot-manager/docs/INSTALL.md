# Installation Guide

This guide covers building and installing Screenshot Manager on Windows.

## 1. Prerequisites

- Windows 10 or Windows 11
- Python 3.10+ available on PATH

Check Python:

```powershell
python --version
```

## 2. Build EXE

From tool root (`tools/screenshot-manager`):

```powershell
./scripts/build.ps1
```

What this script does:

- Creates `.venv` if missing
- Installs package and build dependency (`pyinstaller`)
- Produces `dist/ScreenshotManager.exe`

## 3. Install App

```powershell
./scripts/install.ps1
```

Installed location:

- `%LOCALAPPDATA%\DailyDriver\ScreenshotManager\ScreenshotManager.exe`

Shortcuts created:

- Desktop: `Screenshot Manager`
- Start Menu: `Daily Driver/Screenshot Manager`

## 4. Uninstall

```powershell
./scripts/uninstall.ps1
```

This removes:

- Installed app files under `%LOCALAPPDATA%`
- Desktop shortcut
- Start Menu shortcut

## Troubleshooting

- If PowerShell blocks scripts, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

- If build fails with missing Python, install Python and restart terminal.
