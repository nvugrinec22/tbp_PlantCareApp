import tkinter as tk
from db import add_event
from utils import (
    center_window,
    BG_MAIN,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)


EVENT_LABELS = {
    "watering": "Zalijevanje",
    "fertilizing": "Gnojidba",
    "repotting": "Presađivanje",
    "pruning": "Orezivanje",
    "other": "Ostalo"
}



def open_add_event_window(plant_id, on_saved):
    window = tk.Toplevel()
    window.title("Dodaj događaj")
    window.configure(bg=BG_MAIN)

    WIDTH = 320
    HEIGHT = 240

    window.resizable(False, False)
    window.transient(window.master)
    window.grab_set()
    window.focus_set()

    center_window(window, window.master, WIDTH, HEIGHT)

    tk.Label(
        window,
        text="🌿 Dodaj događaj",
        font=("Segoe UI", 14, "bold"),
        bg=BG_MAIN,
        fg=TEXT_MAIN
    ).pack(pady=(15, 10))

    tk.Label(
        window,
        text="Vrsta događaja",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    event_var = tk.StringVar(value="Zalijevanje")

    option = tk.OptionMenu(
        window,
        event_var,
        *EVENT_LABELS.values()
    )
    option.config(
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    option.pack(fill="x", padx=30, pady=(0, 10))

    tk.Label(
        window,
        text="Napomena",
        bg=BG_MAIN,
        fg=TEXT_MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=30)

    note_entry = tk.Entry(
        window,
        bg="white",
        fg=TEXT_MAIN,
        relief="flat",
        highlightthickness=1
    )
    note_entry.pack(fill="x", padx=30, pady=(0, 15))

    
    def save_event():
        reverse_map = {v: k for k, v in EVENT_LABELS.items()}

        event_type = reverse_map[event_var.get()]

        add_event(
            plant_id,
            event_type,
            note_entry.get()
        )
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
        command=save_event
    ).pack(pady=(5, 15))
