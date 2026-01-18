import tkinter as tk
from utils import BG_MAIN, GREEN_MAIN, TEXT_MAIN, TEXT_MUTED

def open_error_dialog(parent, title, message):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.configure(bg=BG_MAIN)

    WIDTH = 380
    HEIGHT = 180

    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()
    dialog.focus_set()

    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - WIDTH) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - HEIGHT) // 2
    dialog.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

    tk.Label(
        dialog,
        text="⛔ " + title,
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(20, 10))

    tk.Label(
        dialog,
        text=message,
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10),
        wraplength=330,
        justify="center"
    ).pack(padx=20, pady=(0, 20))

    tk.Button(
        dialog,
        text="U redu",
        bg=GREEN_MAIN,
        fg="white",
        relief="flat",
        font=("Segoe UI", 10, "bold"),
        padx=20,
        pady=6,
        command=dialog.destroy
    ).pack(pady=(0, 20))
