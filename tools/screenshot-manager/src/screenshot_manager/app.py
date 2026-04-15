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
        self.geometry("920x620")
        self.minsize(860, 560)
        self.configure(bg="#f4f6f8")

        self.source_var = tk.StringVar(value=str(default_source()))
        self.destination_var = tk.StringVar(value=str(default_destination()))
        self.organize_var = tk.BooleanVar(value=True)
        self.rename_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Ready")

        self.manager: ScreenshotManager | None = None
        self.start_button: ttk.Button | None = None
        self.stop_button: ttk.Button | None = None
        self.log_box: tk.Text | None = None

        self._configure_styles()
        self._build_ui()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Root.TFrame", background="#f4f6f8")
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#ffffff", foreground="#16222e", font=("Segoe UI Semibold", 14))
        style.configure("Hint.TLabel", background="#ffffff", foreground="#5c6875", font=("Segoe UI", 9))
        style.configure("Section.TLabel", background="#ffffff", foreground="#2b3d50", font=("Segoe UI Semibold", 10))
        style.configure("Primary.TButton", font=("Segoe UI Semibold", 10), padding=(12, 7))
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        style.configure("TCheckbutton", background="#ffffff", font=("Segoe UI", 10))

    def _build_ui(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=18)
        root.pack(fill=tk.BOTH, expand=True)

        card = ttk.Frame(root, style="Card.TFrame", padding=16)
        card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(card, text="Screenshot Manager", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            card,
            text="Automatically organize and rename screenshots with a clean, predictable workflow.",
            style="Hint.TLabel",
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 14))

        ttk.Label(card, text="Screenshot Folder", style="Section.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Entry(card, textvariable=self.source_var).grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 10))
        ttk.Button(card, text="Browse", command=self._pick_source).grid(row=3, column=2, sticky="e")

        ttk.Label(card, text="Destination Folder", style="Section.TLabel").grid(row=4, column=0, sticky="w", pady=(12, 0))
        ttk.Entry(card, textvariable=self.destination_var).grid(row=5, column=0, columnspan=2, sticky="ew", padx=(0, 10))
        ttk.Button(card, text="Browse", command=self._pick_destination).grid(row=5, column=2, sticky="e")

        ttk.Checkbutton(card, text="Organize screenshots by date folder", variable=self.organize_var).grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(14, 0)
        )
        ttk.Checkbutton(card, text="Rename screenshots to timestamp format", variable=self.rename_var).grid(
            row=7, column=0, columnspan=3, sticky="w", pady=(2, 0)
        )

        button_row = ttk.Frame(card, style="Card.TFrame")
        button_row.grid(row=8, column=0, columnspan=3, sticky="w", pady=(14, 10))

        self.start_button = ttk.Button(button_row, text="Start Monitoring", style="Primary.TButton", command=self.start_manager)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = ttk.Button(button_row, text="Stop", command=self.stop_manager, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(8, 0))

        ttk.Button(button_row, text="Clear Log", command=self._clear_log).pack(side=tk.LEFT, padx=(8, 0))

        ttk.Label(card, text="Activity Log", style="Section.TLabel").grid(row=9, column=0, sticky="w", pady=(6, 4))
        self.log_box = tk.Text(
            card,
            height=14,
            state=tk.DISABLED,
            bd=1,
            relief=tk.SOLID,
            bg="#f8fafb",
            fg="#15202b",
            insertbackground="#15202b",
            font=("Consolas", 10),
            padx=8,
            pady=8,
        )
        self.log_box.grid(row=10, column=0, columnspan=3, sticky="nsew")

        status_bar = ttk.Label(root, textvariable=self.status_var, anchor="w", style="Hint.TLabel")
        status_bar.pack(fill=tk.X, pady=(8, 0))

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)
        card.rowconfigure(10, weight=1)

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
        self.after(0, self._append_log, text)

    def _append_log(self, text: str) -> None:
        if not self.log_box:
            return
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def _clear_log(self) -> None:
        if not self.log_box:
            return
        self.log_box.config(state=tk.NORMAL)
        self.log_box.delete("1.0", tk.END)
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
        self.status_var.set("Monitoring started")
        if self.start_button:
            self.start_button.config(state=tk.DISABLED)
        if self.stop_button:
            self.stop_button.config(state=tk.NORMAL)

    def stop_manager(self) -> None:
        if self.manager:
            self.manager.stop()
            self.manager = None
        self.status_var.set("Stopped")
        if self.start_button:
            self.start_button.config(state=tk.NORMAL)
        if self.stop_button:
            self.stop_button.config(state=tk.DISABLED)

    def _on_close(self) -> None:
        if self.manager:
            self.manager.stop()
        self.destroy()


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
