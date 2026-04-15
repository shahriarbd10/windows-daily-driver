# Screenshot Manager

Screenshot Manager is a lightweight Windows utility that watches your screenshot folder and automatically:

- Moves screenshots into a managed destination
- Organizes by date folders (optional)
- Renames files to timestamp format (optional)
- Stores an index in SQLite for future search features

## Features

- Desktop GUI (Tkinter)
- No runtime third-party dependency required for core app
- Single-file EXE build with PyInstaller
- Install/uninstall scripts for a proper Windows app-style setup

## Project Layout

- `src/screenshot_manager/` - App source code
- `scripts/build.ps1` - Builds `ScreenshotManager.exe`
- `scripts/install.ps1` - Installs app to `%LOCALAPPDATA%`
- `scripts/uninstall.ps1` - Removes app and shortcuts
- `docs/INSTALL.md` - End-to-end install guide
- `docs/USAGE.md` - User guide

## Quick Start (Developer)

1. Open PowerShell in this folder.
2. Run:

```powershell
./scripts/build.ps1
```

3. Install:

```powershell
./scripts/install.ps1
```

4. Launch from Desktop or Start Menu shortcut.

## Build Output

- `dist/ScreenshotManager.exe`

## Requirements

- Windows 10/11
- Python 3.10+ (for build only)

## Notes

- Default source folder: `%USERPROFILE%\Pictures\Screenshots`
- Default destination: `%USERPROFILE%\Pictures\ManagedScreenshots`
- If source folder does not exist, choose another folder in the app UI
