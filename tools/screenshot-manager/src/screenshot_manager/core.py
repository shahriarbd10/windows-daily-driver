from __future__ import annotations

import shutil
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


@dataclass
class ManagerConfig:
    source_dir: Path
    destination_dir: Path
    poll_seconds: float = 2.0
    organize_by_date: bool = True
    rename_files: bool = True


class ScreenshotManager:
    def __init__(
        self,
        config: ManagerConfig,
        logger: Callable[[str], None],
        index_db: Optional[Path] = None,
    ) -> None:
        self.config = config
        self.logger = logger
        self.index_db = index_db
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._seen: set[Path] = set()

        self.config.source_dir.mkdir(parents=True, exist_ok=True)
        self.config.destination_dir.mkdir(parents=True, exist_ok=True)

        if self.index_db:
            self._init_db()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            self.logger("Manager already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.logger("Screenshot manager started.")

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3)
        self.logger("Screenshot manager stopped.")

    def _run(self) -> None:
        self.logger(f"Watching: {self.config.source_dir}")
        while not self._stop_event.is_set():
            try:
                self._scan_once()
            except Exception as exc:
                self.logger(f"Error: {exc}")
            self._stop_event.wait(self.config.poll_seconds)

    def _scan_once(self) -> None:
        for item in self.config.source_dir.iterdir():
            if not item.is_file() or item.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if item in self._seen:
                continue

            # Skip files still being written to disk.
            if not self._is_stable(item):
                continue

            self._process(item)
            self._seen.add(item)

    def _is_stable(self, file_path: Path) -> bool:
        first_size = file_path.stat().st_size
        time.sleep(0.15)
        second_size = file_path.stat().st_size
        return first_size == second_size

    def _process(self, source_file: Path) -> None:
        timestamp = datetime.now()
        target_dir = self.config.destination_dir

        if self.config.organize_by_date:
            target_dir = target_dir / timestamp.strftime("%Y-%m-%d")
            target_dir.mkdir(parents=True, exist_ok=True)

        if self.config.rename_files:
            base_name = f"shot_{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}"
            target_file = self._next_available_name(target_dir, base_name, source_file.suffix.lower())
        else:
            target_file = self._next_available_name(target_dir, source_file.stem, source_file.suffix.lower())

        shutil.move(str(source_file), str(target_file))
        self.logger(f"Moved: {source_file.name} -> {target_file}")

        if self.index_db:
            self._index_file(target_file)

    def _next_available_name(self, folder: Path, base: str, extension: str) -> Path:
        candidate = folder / f"{base}{extension}"
        counter = 1
        while candidate.exists():
            candidate = folder / f"{base}_{counter}{extension}"
            counter += 1
        return candidate

    def _init_db(self) -> None:
        assert self.index_db is not None
        with sqlite3.connect(self.index_db) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS screenshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _index_file(self, file_path: Path) -> None:
        assert self.index_db is not None
        with sqlite3.connect(self.index_db) as conn:
            conn.execute(
                "INSERT INTO screenshots (file_path, created_at) VALUES (?, ?)",
                (str(file_path), datetime.now().isoformat(timespec="seconds")),
            )
            conn.commit()
