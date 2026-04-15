# Usage Guide

## 1. Open the App

Launch Screenshot Manager from Desktop or Start Menu.

## 2. Configure Folders

- Screenshot Folder: where screenshots are currently saved
- Destination Folder: where managed screenshots should be stored

## 3. Configure Behavior

- Organize by date folder: creates `YYYY-MM-DD` subfolders
- Rename to timestamp: format like `shot_15 April 2026_19-20-04.png`

Date folders now use format like `15 April 2026`.

## 4. Start Processing

Click `Start`.

The app will:

- Watch your source folder
- Move each new screenshot into destination
- Log actions in the activity panel

## 5. Stop Processing

Click `Stop` before closing, or just close the window.

The app stops gracefully on exit.

## Data Index

A lightweight database file is created at destination root:

- `screenshot_index.db`

Current version stores path and timestamp for each processed screenshot.
