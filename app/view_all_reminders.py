import tkinter as tk
from tkinter import messagebox
from db import get_all_reminders, toggle_reminder_done
from utils import (
    BG_MAIN,
    BG_CARD,
    GREEN_MAIN,
    GREEN_DARK,
    BORDER,
    TEXT_MAIN,
    TEXT_MUTED
)

class AllRemindersFrame(tk.Frame):
    def __init__(self, parent, user_id, on_back, on_open_plant):
        super().__init__(parent, bg=BG_MAIN)
        self.user_id = user_id
        self.on_back = on_back
        self.on_open_plant = on_open_plant

        tk.Button(
            self,
            text="← Natrag",
            command=self.on_back,
            bg=BG_MAIN,
            fg=TEXT_MUTED,
            relief="flat",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=10, pady=5)

        tk.Label(
            self,
            text="⏰ Svi podsjetnici",
            font=("Segoe UI", 18, "bold"),
            bg=BG_MAIN,
            fg=TEXT_MAIN
        ).pack(pady=10)

        card = tk.Frame(
            self,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        list_frame = tk.Frame(card, bg=BG_CARD)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=15,
            bg="#f7f6f2",
            fg=TEXT_MAIN,
            selectbackground=GREEN_MAIN,
            selectforeground="white",
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 10)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox.yview)

        self.error_label = tk.Label(
            self,
            text="",
            fg="#b00020",
            bg=BG_MAIN,
            font=("Segoe UI", 9)
        )
        self.error_label.pack(pady=(5, 0))

        self.listbox.bind(
            "<<ListboxSelect>>",
            lambda e: self.error_label.config(text="")
        )

        self.reminder_data = []
        self.load_reminders()

        btns = tk.Frame(self, bg=BG_MAIN)
        btns.pack(pady=10)

        tk.Button(
            btns,
            text="✔️ Označi / poništi",
            bg=GREEN_MAIN,
            fg="white",
            activebackground=GREEN_DARK,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=5,
            command=self.toggle_done
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="🌿 Otvori biljku",
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            font=("Segoe UI", 10),
            padx=10,
            pady=5,
            command=self.open_plant
        ).pack(side=tk.LEFT, padx=5)

    def load_reminders(self):
        self.listbox.delete(0, tk.END)
        self.reminder_data.clear()

        for rid, plant_name, date, msg, done, plant_id in get_all_reminders(self.user_id):
            status = "✔️" if done else "⏳"
            self.listbox.insert(
                tk.END,
                f"{status} {date} | {plant_name}: {msg}"
            )
            self.reminder_data.append((rid, done, plant_id))

    def toggle_done(self):
        sel = self.listbox.curselection()
        if not sel:
            self.error_label.config(text="Odaberi podsjetnik iz liste")
            return

        rid, done, _ = self.reminder_data[sel[0]]

        error = toggle_reminder_done(rid)

        if error:
            self.error_label.config(text=error)
            return

        self.load_reminders()



    def open_plant(self):
        sel = self.listbox.curselection()
        if not sel:
            self.error_label.config(text="Odaberi podsjetnik iz liste")
            return


        _, _, plant_id = self.reminder_data[sel[0]]
        self.on_open_plant(plant_id)
