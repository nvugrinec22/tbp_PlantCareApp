import tkinter as tk
from db import add_growth_measurement
from utils import (
    center_window,
    BG_MAIN,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)


def open_add_growth_window(plant_id, on_saved):
    window = tk.Toplevel()
    window.title("Izmjeri biljku")
    window.configure(bg=BG_MAIN)

    WIDTH = 320
    HEIGHT = 230

    window.resizable(False, False)
    window.transient(window.master)
    window.grab_set()
    window.focus_set()

    center_window(window, window.master, WIDTH, HEIGHT)

    tk.Label(
        window,
        text="🌱 Izmjeri biljku",
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(15, 10))

    tk.Label(
        window,
        text="Visina biljke (cm)",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    height_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    height_entry.pack(fill="x", padx=30, pady=(0, 15))

    error_label = tk.Label(
        window,
        text="",
        bg=BG_MAIN,
        fg="#b00020",
        font=("Segoe UI", 9)
    )
    error_label.pack(pady=(0, 10))

    def save_growth():
        error_label.config(text="")  

        value = height_entry.get().strip()

        if not value:
            error_label.config(text="Unesi visinu biljke")
            height_entry.focus_set()
            return

        try:
            height = float(value)
        except ValueError:
            error_label.config(text="Visina mora biti broj (npr. 12.5)")
            height_entry.focus_set()
            return

        if height <= 0:
            error_label.config(text="Visina mora biti veća od 0")
            height_entry.focus_set()
            return

        error = add_growth_measurement(plant_id, height)

        if error:
            error_label.config(text="Neispravna vrijednost visine")
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
        command=save_growth
    ).pack(pady=(5, 15))
