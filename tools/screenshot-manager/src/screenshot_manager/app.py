from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .core import ManagerConfig, ScreenshotManager


def default_source() -> Path:
    pictures = Path.home() / "Pictures"
    preferred = pictures / "Screenshots"
    if preferred.exists():
        return preferred
    return pictures


def default_destination() -> Path:
    return Path.home() / "Pictures" / "ManagedScreenshots"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Daily Driver - Screenshot Manager")
        self.geometry("760x480")
        self.minsize(700, 420)

        self.source_var = tk.StringVar(value=str(default_source()))
        self.destination_var = tk.StringVar(value=str(default_destination()))
        self.organize_var = tk.BooleanVar(value=True)
        self.rename_var = tk.BooleanVar(value=True)

        self.manager: ScreenshotManager | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Screenshot Folder").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.source_var, width=72).grid(row=1, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(frame, text="Browse", command=self._pick_source).grid(row=1, column=1, sticky="e")

        ttk.Label(frame, text="Destination Folder").grid(row=2, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(frame, textvariable=self.destination_var, width=72).grid(row=3, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(frame, text="Browse", command=self._pick_destination).grid(row=3, column=1, sticky="e")

        ttk.Checkbutton(frame, text="Organize screenshots by date folder", variable=self.organize_var).grid(
            row=4, column=0, sticky="w", pady=(14, 0)
        )
        ttk.Checkbutton(frame, text="Rename screenshots to timestamp format", variable=self.rename_var).grid(
            row=5, column=0, sticky="w"
        )

        button_row = ttk.Frame(frame)
        button_row.grid(row=6, column=0, sticky="w", pady=(14, 10))
        ttk.Button(button_row, text="Start", command=self.start_manager).pack(side=tk.LEFT)
        ttk.Button(button_row, text="Stop", command=self.stop_manager).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Label(frame, text="Activity Log").grid(row=7, column=0, sticky="w", pady=(8, 4))
        self.log_box = tk.Text(frame, height=12, state=tk.DISABLED)
        self.log_box.grid(row=8, column=0, columnspan=2, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(8, weight=1)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _pick_source(self) -> None:
        selected = filedialog.askdirectory(title="Select screenshot source folder")
        if selected:
            self.source_var.set(selected)

    def _pick_destination(self) -> None:
        selected = filedialog.askdirectory(title="Select destination folder")
        if selected:
            self.destination_var.set(selected)

    def _log(self, text: str) -> None:
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def start_manager(self) -> None:
        source = Path(self.source_var.get().strip())
        destination = Path(self.destination_var.get().strip())

        if not source.exists() or not source.is_dir():
            messagebox.showerror("Invalid Source", "Source folder does not exist.")
            return

        config = ManagerConfig(
            source_dir=source,
            destination_dir=destination,
            organize_by_date=self.organize_var.get(),
            rename_files=self.rename_var.get(),
        )

        db_path = destination / "screenshot_index.db"
        self.manager = ScreenshotManager(config=config, logger=self._log, index_db=db_path)
        self.manager.start()

    def stop_manager(self) -> None:
        if self.manager:
            self.manager.stop()
            self.manager = None

    def _on_close(self) -> None:
        if self.manager:
            self.manager.stop()
        self.destroy()


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
