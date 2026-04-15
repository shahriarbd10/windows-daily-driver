# Recycle Bin Cleaner

Recycle Bin Cleaner is a focused Windows desktop utility that empties Recycle Bin with explicit safety gates before deletion.

## Key Capabilities

- Reads current Recycle Bin item count and size
- Empties Recycle Bin through the Windows shell API
- Uses a multi-step destructive-action confirmation flow:
  - Caution checkbox
  - Required keyword: `CLEAR`
  - Final yes/no confirmation dialog

## Safety Design

This operation permanently deletes recycled files and cannot be undone from normal Windows recovery flows.

The app requires all confirmation steps to be satisfied before the delete action is enabled.

## Project Layout

- `src/recycle_bin_cleaner/` - App source code
- `scripts/build.ps1` - Build script for EXE packaging
- `docs/CAUTION.md` - Safety and usage caution notes
- `RecycleBinCleaner.spec` - PyInstaller spec file

## Build (Developer)

From `tools/recycle-bin-cleaner`:

```powershell
./scripts/build.ps1
```

Output:

- `dist/RecycleBinCleaner.exe`

## Requirements

- Windows 10/11
- Python 3.10+ (build-time)

## Caution

Always verify there is nothing in Recycle Bin that you may need later before confirming deletion.
