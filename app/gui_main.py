import tkinter as tk
from db import get_plants, get_plant_info
from add_plant import open_add_plant_window
from plant_detail import PlantDetailFrame
from view_all_reminders import AllRemindersFrame
from utils import (
    BG_MAIN,
    BG_CARD,
    GREEN_MAIN,
    GREEN_DARK,
    BORDER,
    TEXT_MAIN,
    TEXT_MUTED
)

class MainWindow:
    def __init__(self, root, user_id, on_logout):
        self.root = root
        self.user_id = user_id
        self.on_logout = on_logout


        self.root.title("Plant Care App")
        self.root.geometry("700x850")

        self.current_frame = None
        self.plants = []

        self.show_plant_list()

    def clear_screen(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_plant_list(self):
        self.clear_screen()

        frame = tk.Frame(self.root, bg = BG_MAIN)
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame

        tk.Button(
            frame,
            text="🚪 Odjava",
            command=self.on_logout,
            bg=BG_MAIN,
            fg=TEXT_MUTED,
            relief="flat",
            font=("Segoe UI", 9)
        ).pack(anchor="e", padx=10, pady=5)

        tk.Label(
            frame,
            text="🌱 Moje biljke",
            font=("Segoe UI", 16, "bold"),
            bg=BG_MAIN,
            fg=TEXT_MAIN
        ).pack(pady=5)


        list_frame = tk.Frame(
            frame,
            bg=BG_CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)



        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            height=15,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            selectbackground=GREEN_MAIN,
            selectforeground="white",
            highlightthickness=0,
            relief="flat",
            font=("Segoe UI", 10)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind(
            "<<ListboxSelect>>",
            lambda e: self.error_label.config(text="")
        )


        self.error_label = tk.Label(
            frame,
            text="",
            fg="#b00020",
            bg=BG_MAIN,
            font=("Segoe UI", 9)
        )
        self.error_label.pack(pady=(5, 0))


        self.plants = get_plants(self.user_id)
        for p in self.plants:
            self.listbox.insert(tk.END, p[1])

        btn_frame = tk.Frame(frame, bg=BG_MAIN)
        btn_frame.pack(pady=15)


        tk.Button(
            btn_frame,
            text="➕ Dodaj biljku",
            command=lambda: open_add_plant_window(self.user_id, self.show_plant_list),
            bg=GREEN_MAIN,
            fg="white",
            activebackground=GREEN_DARK,
            relief="flat",
            padx=12,
            pady=6,
            font=("Segoe UI", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)


        tk.Button(
            btn_frame,
            text="➡️ Otvori biljku",
            command=self.open_selected_plant,
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            padx=10,
            pady=6,
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=5)


        tk.Button(
            btn_frame,
            text="⏰ Podsjetnici",
            command=self.show_all_reminders,
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            padx=10,
            pady=6,
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=5)



    def open_selected_plant(self):
        sel = self.listbox.curselection()
        if not sel:
            self.error_label.config(text="Odaberi biljku iz liste")
            return


        plant_id, name, image_path = self.plants[sel[0]]
        self.show_plant_detail(plant_id, name, image_path)

    def show_plant_detail(self, plant_id, name, image_path):
        self.clear_screen()

        def reload_detail():
            info = get_plant_info(plant_id)
            self.show_plant_detail(
                plant_id,
                info["name"],
                info.get("image_path")
            )

        frame = PlantDetailFrame(
            self.root,
            plant_id,
            name,
            image_path,
            on_back=self.show_plant_list,
            on_reload=reload_detail
        )
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame


    def show_all_reminders(self):
        self.clear_screen()

        frame = AllRemindersFrame(
            self.root,
            user_id=self.user_id,
            on_back=self.show_plant_list,
            on_open_plant=self.open_plant_by_id
        )
        frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = frame


    def open_plant_by_id(self, plant_id):
        for pid, name, image_path in self.plants:
            if pid == plant_id:
                self.show_plant_detail(pid, name, image_path)
                break



