import tkinter as tk
from tkinter import messagebox
from datetime import date
from db import add_plant
from utils import (
    center_window,
    BG_MAIN,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)


def open_add_plant_window(user_id, refresh_callback):
    window = tk.Toplevel()
    window.title("Dodaj biljku")
    window.configure(bg=BG_MAIN)

    WIDTH = 340
    HEIGHT = 330

    window.resizable(False, False)
    window.transient(window.master)
    window.grab_set()
    window.focus_set()

    center_window(window, window.master, WIDTH, HEIGHT)

    tk.Label(
        window,
        text="🌱 Dodaj novu biljku",
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(15, 10))

    tk.Label(
        window,
        text="Naziv biljke",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    name_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    name_entry.pack(fill="x", padx=30, pady=(0, 10))

    tk.Label(
        window,
        text="Vrsta",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    species_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    species_entry.pack(fill="x", padx=30, pady=(0, 10))

    
    def save_plant():
        name = name_entry.get().strip()
        species = species_entry.get().strip()

        if not name:
            messagebox.showerror("Greška", "Naziv biljke je obavezan")
            return

        add_plant(
            user_id,
            name,
            species,
            date.today(),
            None
        )

        refresh_callback()
        window.destroy()

    tk.Button(
        window,
        text="Spremi biljku",
        bg=GREEN_MAIN,
        fg="white",
        activebackground=GREEN_DARK,
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=6,
        command=save_plant
    ).pack(pady=(5, 20))
