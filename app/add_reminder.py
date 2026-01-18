import tkinter as tk
from datetime import date
from db import add_reminder_rule
from utils import (
    center_window,
    BG_MAIN,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)


def open_add_reminder_window(plant_id, on_saved):
    window = tk.Toplevel()
    window.title("Dodaj podsjetnik")
    window.configure(bg=BG_MAIN)

    WIDTH = 340
    HEIGHT = 300

    window.resizable(False, False)
    window.transient(window.master)
    window.grab_set()
    window.focus_set()

    center_window(window, window.master, WIDTH, HEIGHT)

    tk.Label(
        window,
        text="⏰ Dodaj podsjetnik",
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(15, 10))

    tk.Label(
        window,
        text="Naziv podsjetnika",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    title_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    title_entry.pack(fill="x", padx=30, pady=(0, 15))
    title_entry.focus_set()

    tk.Label(
        window,
        text="Interval (u danima)",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    interval_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    interval_entry.pack(fill="x", padx=30, pady=(0, 20))

    error_label = tk.Label(
        window,
        text="",
        bg=BG_MAIN,
        fg="#b00020",
        font=("Segoe UI", 9)
    )
    error_label.pack(pady=(0, 10))

    def save():
        error_label.config(text="")

        title = title_entry.get().strip()
        interval_text = interval_entry.get().strip()

        if not title:
            error_label.config(text="Naziv podsjetnika je obavezan")
            title_entry.focus_set()
            return

        if not interval_text:
            error_label.config(text="Unesi interval u danima")
            interval_entry.focus_set()
            return

        try:
            interval = int(interval_text)
        except ValueError:
            error_label.config(text="Interval mora biti cijeli broj")
            interval_entry.focus_set()
            return

        if interval <= 0:
            error_label.config(text="Interval mora biti veći od 0")
            interval_entry.focus_set()
            return

        error = add_reminder_rule(
            plant_id,
            title,
            interval,
            date.today()
        )

        if error:
            error_label.config(text=error)
            return

        window.destroy()
        on_saved()


    tk.Button(
        window,
        text="Spremi",
        bg=GREEN_MAIN,
        fg="white",
        activebackground=GREEN_DARK,
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=6,
        command=save
    ).pack(pady=(0, 20))
