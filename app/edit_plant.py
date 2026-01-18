import tkinter as tk
from db import update_plant, get_plant_info
from utils import (
    center_window,
    BG_MAIN,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)


def open_edit_plant_window(plant_id, refresh_callback):
    window = tk.Toplevel()
    window.title("Uredi biljku")
    window.configure(bg=BG_MAIN)

    WIDTH = 360
    HEIGHT = 260

    window.resizable(False, False)
    window.transient(window.master)
    window.grab_set()
    window.focus_set()

    center_window(window, window.master, WIDTH, HEIGHT)

    tk.Label(
        window,
        text="✏️ Uredi biljku",
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(15, 10))

    info = get_plant_info(plant_id)

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
    name_entry.pack(fill="x", padx=30, pady=(0, 12))
    name_entry.insert(0, info["name"])

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
    species_entry.pack(fill="x", padx=30, pady=(0, 20))
    species_entry.insert(0, info["species"] or "")

    error_label = tk.Label(
        window,
        text="",
        fg="#b00020",
        bg=BG_MAIN,
        font=("Segoe UI", 9)
    )
    error_label.pack(pady=(0, 10))

    def save():
        name = name_entry.get().strip()
        species = species_entry.get().strip()

        error_label.config(text="")

        if not name:
            error_label.config(text="Naziv biljke je obavezan")
            name_entry.focus_set()
            return

        update_plant(plant_id, name, species)
        refresh_callback()
        window.destroy()

    tk.Button(
        window,
        text="💾 Spremi promjene",
        bg=GREEN_MAIN,
        fg="white",
        activebackground=GREEN_DARK,
        relief="flat",
        font=("Segoe UI", 11, "bold"),
        padx=20,
        pady=6,
        command=save
    ).pack(pady=(5, 20))
