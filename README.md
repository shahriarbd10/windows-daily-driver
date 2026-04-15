# Windows Daily Driver

Windows Daily Driver is a personal utility software initiative focused on small, practical Windows tools that remove daily friction and save repetitive effort.

## Vision

Build a toolbox of focused Windows desktop apps that are:

- Fast to launch and simple to use
- Reliable in normal daily workflows
- Safe for non-technical users
- Installable as standalone EXE tools
- Easy to extend with shared patterns

## Product Philosophy

- Problem-first development: each tool solves one clear pain point
- Small surface area: minimal UI, minimal setup, clear actions
- Practical safety: destructive actions require explicit warning and confirmation gates
- Local-first behavior: avoid cloud dependency assumptions
- Ship-ready artifacts: each tool should build into a downloadable EXE

## Current Tools

1. `tools/screenshot-manager`
- GUI utility that monitors a screenshot folder and organizes files
- Optional date-based folder organization and timestamp renaming
- Human-readable date format (example: `15 April 2026`)
- Activity log in UI and SQLite indexing foundation for future search
- Handles OneDrive/cloud-provider availability errors gracefully

2. `tools/recycle-bin-cleaner`
- Dedicated cleanup app for safely emptying Recycle Bin
- Reads Recycle Bin stats through Windows shell APIs
- Strong caution workflow before destructive action:
  - Caution checkbox
  - Required keyword (`CLEAR`)
  - Final confirmation dialog

## Engineering Direction

- Desktop-first Windows GUI with lightweight Python stack
- Per-tool packaging with PyInstaller EXE output
- Scripted build/install flows for repeatable releases
- Shared integration pattern between tools where useful
- Safety and resilience prioritized over feature volume

## Project Structure

- `tools/` - Individual utility apps (one folder per tool)
- `shared/` - Reusable modules and helpers
- `scripts/` - Project automation scripts
- `docs/` - Architecture notes and usage docs
- `tests/` - Cross-tool and integration tests

## Strategic Next Steps

1. Release consistency
- Standardize release folders for all tools
- Publish versioned binaries and changelog notes

2. Tool ecosystem growth
- Add Bulk File Renamer
- Add Temp File Cleaner
- Add Startup App Health Checker

3. Professional polish
- Add persistent settings per tool
- Add dark/light theme toggle
- Add in-app "Open Logs" and "Open Data Folder"

4. Reliability and testing
- Add unit tests for core file operations and naming logic
- Add smoke tests for build scripts and startup behavior
