# Daily Driver

A collection of small Windows software tools that remove everyday friction.

## Goals

- Build practical utilities for common day-to-day tasks
- Keep each tool focused, reliable, and easy to run
- Share reusable logic across tools when it makes sense
- Maintain clear docs and tests as the project grows

## Project Structure

- `tools/` - Individual utility apps or scripts (one folder per tool)
- `shared/` - Reusable modules, helpers, and common code
- `scripts/` - Project automation scripts (setup, lint, release, etc.)
- `docs/` - Architecture notes, design docs, and usage guides
- `tests/` - Cross-tool and integration tests

## How We Build Here

- Start with a problem-first tool idea
- Define a small MVP and acceptance criteria
- Implement in isolated tool folders under `tools/`
- Add tests before expanding features
- Document installation and usage in each tool folder

## Suggested First Tools

1. Clipboard history cleaner / formatter
2. Bulk file renamer with preview mode
3. Screenshot organizer by date + OCR text index
4. Startup apps health checker
5. Temporary files smart cleanup utility

## Implemented Tool

- `tools/screenshot-manager` - Windows GUI app to auto-organize and rename screenshots with install/uninstall scripts.

## Next Step

Pick the first tool, then we can scaffold it end-to-end (UI/CLI, logic, tests, and packaging).
# windows-daily-driver
