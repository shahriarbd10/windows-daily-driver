from __future__ import annotations

import ctypes
import tkinter as tk
from tkinter import messagebox, ttk


class SHQUERYRBINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("i64Size", ctypes.c_longlong),
        ("i64NumItems", ctypes.c_longlong),
    ]


def query_recycle_bin() -> tuple[int, int]:
    info = SHQUERYRBINFO()
    info.cbSize = ctypes.sizeof(SHQUERYRBINFO)
    result = ctypes.windll.shell32.SHQueryRecycleBinW(None, ctypes.byref(info))
    if result != 0:
        raise OSError(f"SHQueryRecycleBinW failed with code {result}")
    return int(info.i64NumItems), int(info.i64Size)


def empty_recycle_bin() -> None:
    SHERB_NOCONFIRMATION = 0x00000001
    SHERB_NOPROGRESSUI = 0x00000002
    SHERB_NOSOUND = 0x00000004

    flags = SHERB_NOCONFIRMATION | SHERB_NOPROGRESSUI | SHERB_NOSOUND
    result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
    if result != 0:
        raise OSError(f"SHEmptyRecycleBinW failed with code {result}")


def format_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{size} B"


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Daily Driver - Recycle Bin Cleaner")
        self.geometry("560x360")
        self.minsize(540, 340)
        self.configure(bg="#f4f6f8")

        self.status_var = tk.StringVar(value="Checking recycle bin...")
        self.confirm_var = tk.BooleanVar(value=False)
        self.keyword_var = tk.StringVar(value="")

        self._build_ui()
        self.refresh_stats()

    def _build_ui(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Card.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#ffffff", foreground="#1f2933", font=("Segoe UI Semibold", 14))
        style.configure("Muted.TLabel", background="#ffffff", foreground="#52606d", font=("Segoe UI", 10))
        style.configure("Danger.TButton", font=("Segoe UI Semibold", 10), padding=(12, 7))

        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)

        card = ttk.Frame(root, style="Card.TFrame", padding=16)
        card.pack(fill=tk.BOTH, expand=True)

        ttk.Label(card, text="Recycle Bin Cleaner", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Permanently deletes all items currently in Recycle Bin.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(2, 12))

        caution = (
            "CAUTION: This action cannot be undone.\n"
            "Check the box and type CLEAR to continue."
        )
        ttk.Label(card, text=caution, style="Muted.TLabel").pack(anchor="w", pady=(0, 10))

        self.stats_label = ttk.Label(card, text="", style="Muted.TLabel")
        self.stats_label.pack(anchor="w", pady=(0, 12))

        ttk.Checkbutton(
            card,
            text="I understand this will permanently delete recycle bin files.",
            variable=self.confirm_var,
            command=self._update_actions,
        ).pack(anchor="w", pady=(0, 8))

        keyword_row = ttk.Frame(card, style="Card.TFrame")
        keyword_row.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(keyword_row, text="Type CLEAR:", style="Muted.TLabel").pack(side=tk.LEFT)
        keyword_entry = ttk.Entry(keyword_row, textvariable=self.keyword_var, width=16)
        keyword_entry.pack(side=tk.LEFT, padx=(8, 0))
        keyword_entry.bind("<KeyRelease>", lambda _e: self._update_actions())

        button_row = ttk.Frame(card, style="Card.TFrame")
        button_row.pack(fill=tk.X)
        ttk.Button(button_row, text="Refresh", command=self.refresh_stats).pack(side=tk.LEFT)
        self.clear_button = ttk.Button(button_row, text="Empty Recycle Bin", command=self.clear_recycle_bin)
        self.clear_button.pack(side=tk.LEFT, padx=(8, 0))

        ttk.Separator(card).pack(fill=tk.X, pady=14)
        ttk.Label(card, textvariable=self.status_var, style="Muted.TLabel").pack(anchor="w")

        self._update_actions()

    def _update_actions(self) -> None:
        ready = self.confirm_var.get() and self.keyword_var.get().strip().upper() == "CLEAR"
        self.clear_button.config(state=tk.NORMAL if ready else tk.DISABLED)

    def refresh_stats(self) -> None:
        try:
            count, size = query_recycle_bin()
            self.stats_label.config(text=f"Current Recycle Bin: {count} item(s), {format_bytes(size)}")
            self.status_var.set("Ready")
        except Exception as exc:
            self.stats_label.config(text="Current Recycle Bin: Unknown")
            self.status_var.set(f"Error reading recycle bin: {exc}")

    def clear_recycle_bin(self) -> None:
        if not (self.confirm_var.get() and self.keyword_var.get().strip().upper() == "CLEAR"):
            messagebox.showwarning("Confirmation Required", "Please check caution box and type CLEAR.")
            return

        approved = messagebox.askyesno(
            "Final Confirmation",
            "This will permanently delete all files in Recycle Bin. Continue?",
            icon=messagebox.WARNING,
        )
        if not approved:
            self.status_var.set("Cancelled")
            return

        try:
            empty_recycle_bin()
            self.status_var.set("Recycle Bin emptied successfully.")
            self.keyword_var.set("")
            self.confirm_var.set(False)
            self._update_actions()
            self.refresh_stats()
        except Exception as exc:
            messagebox.showerror("Operation Failed", str(exc))
            self.status_var.set(f"Failed: {exc}")


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
