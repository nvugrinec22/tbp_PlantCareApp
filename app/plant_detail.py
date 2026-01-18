import tkinter as tk
from tkinter import messagebox, ttk
from db import (
    get_events_for_plant,
    get_reminders_for_plant,
    get_growth_for_plant,
    delete_plant,
    get_plant_info,
    toggle_reminder_done,
    get_growth_stats,
    get_profile_image,
    get_image_gallery,
    get_fastest_growth_week,
    get_weekly_growth
)
from add_event import open_add_event_window
from add_growth import open_add_growth_window
from PIL import Image, ImageTk
import os
from error_dialog import open_error_dialog
from add_reminder import open_add_reminder_window
from edit_plant import open_edit_plant_window
from utils import (
    BG_MAIN,
    BG_CARD,
    GREEN_MAIN,
    GREEN_DARK,
    TEXT_MAIN,
    TEXT_MUTED
)
from tkinter import filedialog
from db import add_plant_image

EVENT_LABELS = {
    "watering": "Zalijevanje",
    "fertilizing": "Gnojidba",
    "repotting": "Presađivanje",
    "pruning": "Orezivanje",
    "other": "Ostalo"
}


class PlantDetailFrame(tk.Frame):
    def __init__(self, parent, plant_id, plant_name, image_path, on_back, on_reload):
        self.on_reload = on_reload
        super().__init__(parent, bg=BG_MAIN)
        self.plant_id = plant_id
        self.on_back = on_back
        self.reminder_ids = []




        back_btn = tk.Button(
            self,
            text="← Natrag",
            bg=BG_MAIN,
            fg=TEXT_MUTED,
            relief="flat",
            font=("Segoe UI", 9),
            command=self.on_back
        )
        back_btn.pack(anchor="w", padx=10, pady=5)

        back_btn.bind("<Enter>", lambda e: back_btn.config(fg=GREEN_MAIN))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg=TEXT_MUTED))

        tk.Label(
            self,
            text=f"🌿 {plant_name}",
            font=("Segoe UI", 18, "bold"),
            bg=BG_MAIN,
            fg=TEXT_MAIN
        ).pack(pady=10)


        profile_wrapper = tk.Frame(self, bg=BG_MAIN)
        profile_wrapper.pack(fill="x", pady=(0, 10))

        profile = tk.Frame(
            profile_wrapper,
            bg=BG_MAIN
        )
        profile.pack(anchor="center")



        self.img_frame = tk.Frame(profile, bg=BG_MAIN)
        self.img_frame.grid(row=0, column=0, rowspan=4, padx=20)

        profile_image = get_profile_image(self.plant_id)

        if profile_image and os.path.exists(profile_image):
            img = Image.open(profile_image).resize((180, 180))
            photo = ImageTk.PhotoImage(img)

            self.profile_image_label = tk.Label(
                self.img_frame,
                image=photo,
                bg=BG_MAIN
            )
            self.profile_image_label.image = photo
            self.profile_image_label.pack()
        else:
            self.profile_image_label = tk.Label(
                self.img_frame,
                text="🌿 Nema slike",
                bg=BG_CARD,
                fg=TEXT_MUTED
            )
            self.profile_image_label.pack()




        self.growth_stats_label = tk.Label(
            profile,
            text="📈 Ukupni rast: —",
            bg=BG_MAIN,
            fg=GREEN_DARK,
            font=("Segoe UI", 10, "bold")
        )
        self.growth_stats_label.grid(row=3, column=1, sticky="w")

        self.fastest_growth_label = tk.Label(
            profile,
            text="🚀 Najbrži tjedni rast: —",
            bg=BG_MAIN,
            fg=GREEN_DARK,
            font=("Segoe UI", 10, "bold")
        )
        self.fastest_growth_label.grid(row=4, column=1, sticky="w")





        info = get_plant_info(plant_id)
        tk.Label(
            profile,
            text=f"Naziv: {info['name']}",
            bg=BG_MAIN,
            fg=TEXT_MAIN,
            font=("Segoe UI", 10)
        ).grid(row=0, column=1, sticky="w")



        tk.Label(
            profile,
            text=f"Vrsta: {info['species']}",
            bg=BG_MAIN,
            fg=TEXT_MAIN,
            font=("Segoe UI", 10)
        ).grid(row=1, column=1, sticky="w")

        tk.Label(
            profile,
            text=f"Zasađena: {info['planting_date']}",
            bg=BG_MAIN,
            fg=TEXT_MAIN,
            font=("Segoe UI", 10)
        ).grid(row=2, column=1, sticky="w")


        def confirm_delete():
            if messagebox.askyesno("Potvrda", "Obrisati biljku i sve podatke?"):
                delete_plant(plant_id)
                self.on_back()

        tk.Button(
            profile,
            text="🗑️ Obriši biljku",
            fg="#b00020",
            bg=BG_MAIN,
            relief="flat",
            font=("Segoe UI", 9),
            command=confirm_delete
        ).grid(row=5, column=1, sticky="w", pady=(5, 0))

        btns = tk.Frame(self, bg=BG_MAIN)
        btns.pack(pady=10)

        tk.Button(
            btns,
            text="➕ Dodaj događaj",
            bg=GREEN_MAIN,
            fg="white",
            activebackground=GREEN_DARK,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            command=lambda: open_add_event_window(
                self.plant_id,
                self.load_events
            )
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="📏 Izmjeri biljku",
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            font=("Segoe UI", 10),
            command=lambda: open_add_growth_window(
                self.plant_id,
                self.load_growth
            )
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="⏰ Dodaj podsjetnik",
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            font=("Segoe UI", 10),
            command=lambda: open_add_reminder_window(
                self.plant_id,
                self.load_reminders
            )
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="✏️ Uredi biljku",
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            font=("Segoe UI", 10),
            command=lambda: open_edit_plant_window(
                self.plant_id,
                self.on_reload
            )
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btns,
            text="📸 Dodaj sliku",
            bg="#ece9e2",
            fg=TEXT_MAIN,
            relief="flat",
            font=("Segoe UI", 10),
            command=self.add_image
        ).pack(side=tk.LEFT, padx=5)


     
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "TNotebook",
            background=BG_MAIN,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#ece9e2",
            padding=[10, 5],
            font=("Segoe UI", 10)
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", BG_CARD)]
        )



        events_tab = tk.Frame(notebook, bg=BG_MAIN)
        notebook.add(events_tab, text="📋 Događaji")

        events_frame = tk.Frame(events_tab, bg=BG_MAIN)
        events_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        events_scroll = tk.Scrollbar(events_frame)
        events_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.events = tk.Listbox(
            events_frame,
            yscrollcommand=events_scroll.set,
            height=10,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            selectbackground=GREEN_MAIN,
            selectforeground="white",
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 10)
        )
        self.events.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        events_scroll.config(command=self.events.yview)


        reminders_tab = tk.Frame(
            notebook,
            bg=BG_MAIN
        )
        notebook.add(reminders_tab, text="⏰ Podsjetnici")

        reminders_frame = tk.Frame(
            reminders_tab,
            bg=BG_MAIN
        )
        reminders_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        reminders_scroll = tk.Scrollbar(reminders_frame)
        reminders_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.reminders = tk.Listbox(
            reminders_frame,
            yscrollcommand=reminders_scroll.set,
            height=10,
            bg=BG_CARD,            
            fg=TEXT_MAIN,
            selectbackground=GREEN_MAIN,
            selectforeground="white",
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 10)
        )
        self.reminders.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        reminders_scroll.config(command=self.reminders.yview)

        self.reminders.bind(
            "<<ListboxSelect>>",
            lambda e: self.reminder_error_label.config(text="")
        )

        self.reminder_error_label = tk.Label(
            reminders_tab,
            text="",
            fg="#b00020",
            bg=BG_MAIN,
            font=("Segoe UI", 9)
        )
        self.reminder_error_label.pack(pady=(0, 5))


        btn_frame = tk.Frame(reminders_tab, bg= BG_MAIN)
        btn_frame.pack(fill="x", pady=5)

        tk.Button(
            btn_frame,
            text="✔️ Označi kao odrađeno / Poništi",
            bg=GREEN_MAIN,
            fg="white",
            activebackground=GREEN_DARK,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=6,
            command=self.mark_reminder
        ).pack()



        growth_tab = tk.Frame(notebook, bg=BG_MAIN)
        notebook.add(growth_tab, text="📏 Rast")

        growth_frame = tk.Frame(
            growth_tab,
            bg=BG_MAIN
        )
        growth_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        growth_scroll = tk.Scrollbar(growth_frame)
        growth_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.growth = tk.Listbox(
            growth_frame,
            yscrollcommand=growth_scroll.set,
            height=10,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            selectbackground=GREEN_MAIN,
            selectforeground="white",
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 10)
        )
        self.growth.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        growth_scroll.config(command=self.growth.yview)


        gallery_tab = tk.Frame(notebook, bg=BG_MAIN)
        notebook.add(gallery_tab, text="🖼️ Galerija")

        canvas = tk.Canvas(gallery_tab, bg=BG_MAIN, highlightthickness=0)
        scrollbar = tk.Scrollbar(gallery_tab, orient="vertical", command=canvas.yview)

        self.gallery_frame = tk.Frame(canvas, bg=BG_MAIN)

        self.gallery_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.gallery_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.gallery_canvas = canvas
        self.gallery_images = []  


        self.load_all()

 
    def load_all(self):
        self.load_events()
        self.load_reminders()
        self.load_growth()
        self.load_growth_stats()
        self.load_gallery()


    def load_events(self):
        self.events.delete(0, tk.END)

        for d, t, n in get_events_for_plant(self.plant_id):
            label = EVENT_LABELS.get(t, t) 
            text = f"{d} | {label}"
            if n:
                text += f" – {n}"
            self.events.insert(tk.END, text)


    def load_reminders(self):
        self.reminders.delete(0, tk.END)
        self.reminder_ids.clear()
        for rid, d, msg, done in get_reminders_for_plant(self.plant_id):
            self.reminders.insert(tk.END, f"{'✔️' if done else '⏳'} {d} | {msg}")
            self.reminder_ids.append(rid)

    def mark_reminder(self):
        sel = self.reminders.curselection()
        if not sel:
            self.reminder_error_label.config(
                text="Odaberi podsjetnik iz liste"
            )
            return

        reminder_id = self.reminder_ids[sel[0]]

        error = toggle_reminder_done(reminder_id)

        if error:
            open_error_dialog(
                self,
                "Ne može se označiti",
                error
            )
            return

        self.load_reminders()

    
    


    def load_growth_stats(self):
        stats = get_growth_stats(self.plant_id)
        if stats is not None:
            _, _, total = stats
            self.growth_stats_label.config(
                text=f"📈 Ukupni rast: +{total:.1f} cm"
            )
        else:
            self.growth_stats_label.config(
                text="📈 Ukupni rast: —"
            )


    def add_image(self):
        path = filedialog.askopenfilename(
            title="Odaberi sliku biljke",
            filetypes=[
                ("Slike", "*.png *.jpg *.jpeg *.gif *.webp"),
                ("Sve datoteke", "*.*")
            ]
        )
        if path:
            add_plant_image(self.plant_id, path)
            self.load_gallery()
            self.refresh_profile_image()

    def load_gallery(self):
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()

        self.gallery_images.clear()

        images = get_image_gallery(self.plant_id)

        if not images:
            tk.Label(
                self.gallery_frame,
                text="Nema dodanih slika.",
                bg=BG_MAIN,
                fg=TEXT_MUTED
            ).grid(row=0, column=0, pady=20)
            return

        COLUMNS = 3  
        row = 0
        col = 0

        for path, vr in images:
            if not os.path.exists(path):
                continue

            img = Image.open(path)
            img.thumbnail((180, 180))  
            photo = ImageTk.PhotoImage(img)

            frame = tk.Frame(
                self.gallery_frame,
                bg=BG_MAIN,
                padx=5,
                pady=5
            )
            frame.grid(row=row, column=col, padx=10, pady=10)


            lbl = tk.Label(
                frame,
                image=photo,
                bg=BG_MAIN
            )
            lbl.image = photo
            lbl.pack()

            self.gallery_images.append(photo)

            col += 1
            if col >= COLUMNS:
                col = 0
                row += 1


    def refresh_profile_image(self):
        profile_image = get_profile_image(self.plant_id)

        if profile_image and os.path.exists(profile_image):
            img = Image.open(profile_image).resize((180, 180))
            photo = ImageTk.PhotoImage(img)

            self.profile_image_label.config(image=photo, text="")
            self.profile_image_label.image = photo
        else:
            self.profile_image_label.config(
                image="",
                text="🌿 Nema slike"
            )


    def load_growth(self):
        self.growth.delete(0, tk.END)

        for d, h in get_growth_for_plant(self.plant_id):
            self.growth.insert(tk.END, f"{d} | {h:.1f} cm")

        self.load_growth_stats()
        self.load_weekly_growth()
        self.load_fastest_growth()

    def load_fastest_growth(self):
        row = get_fastest_growth_week(self.plant_id)

        if row:
            week, growth = row
            self.fastest_growth_label.config(
                text=f"🚀 Najbrži tjedni rast: Tjedan {week} (+{growth:.1f} cm)"
            )
        else:
            self.fastest_growth_label.config(
                text="🚀 Najbrži tjedni rast: —"
            )


    def load_weekly_growth(self):
        data = get_weekly_growth(self.plant_id)

        if not data:
            self.growth.insert(tk.END, "— Nema dovoljno podataka za tjedni rast —")
            return

        self.growth.insert(tk.END, "")
        self.growth.insert(tk.END, "📅 Rast po tjednima:")

        for week, growth in data:
            self.growth.insert(
                tk.END,
                f"Tjedan {week} | +{growth:.1f} cm"
            )

