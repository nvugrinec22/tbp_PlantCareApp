import tkinter as tk
from db import login_user, register_user
from utils import BG_MAIN, BG_CARD, GREEN_MAIN, GREEN_DARK, TEXT_MAIN, TEXT_MUTED


class AuthFrame(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, bg=BG_MAIN)
        self.on_login_success = on_login_success
        self.mode = "login"  

        self.build_ui()
        self.update_mode()

  
    def build_ui(self):
  
        self.title = tk.Label(
            self,
            font=("Segoe UI", 20, "bold"),
            bg=BG_MAIN,
            fg=TEXT_MAIN
        )
        self.title.pack(pady=(30, 20))

        self.card = tk.Frame(
            self,
            bg=BG_CARD,
            padx=25,
            pady=20,
            highlightbackground="#ddd",
            highlightthickness=1
        )
        self.card.pack()

        tk.Label(
            self.card,
            text="Korisničko ime",
            bg=BG_CARD,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        self.username = tk.Entry(self.card, width=30)
        self.username.pack(pady=(0, 10))

        tk.Label(
            self.card,
            text="Lozinka",
            bg=BG_CARD,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        self.password = tk.Entry(self.card, show="*", width=30)
        self.password.pack(pady=(0, 10))

        self.confirm_label = tk.Label(
            self.card,
            text="Ponovi lozinku",
            bg=BG_CARD,
            fg=TEXT_MUTED
        )
        self.confirm_entry = tk.Entry(self.card, show="*", width=30)

        self.error_label = tk.Label(
            self.card,
            text="",
            fg="#b00020",
            bg=BG_CARD,
            font=("Segoe UI", 9)
        )
        self.error_label.pack(pady=(5, 5))

        self.primary_btn = tk.Button(
            self.card,
            bg=GREEN_MAIN,
            fg="white",
            activebackground=GREEN_DARK,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=6
        )

        self.switch_btn = tk.Button(
            self,
            bg=BG_MAIN,
            fg=GREEN_DARK,
            relief=tk.FLAT,
            cursor="hand2",
            font=("Segoe UI", 9)
        )
        self.switch_btn.pack(pady=15)

    def update_mode(self):
        self.primary_btn.pack_forget()
        self.confirm_label.pack_forget()
        self.confirm_entry.pack_forget()
        self.error_label.pack_forget()
        self.error_label.config(text="")

        if self.mode == "login":
            self.title.config(text="🔐 Prijava")

            self.error_label.pack(pady=(5, 5))

            self.primary_btn.config(
                text="Prijavi se",
                command=self.login
            )
            self.primary_btn.pack(fill="x", pady=(10, 5))

            self.switch_btn.config(
                text="Nemaš račun? Registriraj se",
                command=self.switch_to_register
            )

        else:
            self.title.config(text="🆕 Registracija")

            self.confirm_label.pack(anchor="w")
            self.confirm_entry.pack(pady=(0, 10))

            self.error_label.pack(pady=(5, 5))

            self.primary_btn.config(
                text="Kreiraj račun",
                command=self.register
            )
            self.primary_btn.pack(fill="x", pady=(10, 5))

            self.switch_btn.config(
                text="Već imaš račun? Prijavi se",
                command=self.switch_to_login
            )


    def switch_to_register(self):
        self.mode = "register"
        self.clear_fields()
        self.update_mode()

    def switch_to_login(self):
        self.mode = "login"
        self.clear_fields()
        self.update_mode()

    def clear_fields(self):
        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)
        self.error_label.config(text="")

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        self.error_label.config(text="")

        if not username or not password:
            self.error_label.config(text="Sva polja su obavezna")
            return

        user_id = login_user(username, password)
        if user_id:
            self.on_login_success(user_id)
        else:
            self.error_label.config(text="Neispravno korisničko ime ili lozinka")

    def register(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm_entry.get().strip()

        self.error_label.config(text="")

        if not username or not password or not confirm:
            self.error_label.config(text="Sva polja su obavezna")
            return

        if len(password) < 6:
            self.error_label.config(text="Lozinka mora imati barem 6 znakova")
            return

        if password != confirm:
            self.error_label.config(text="Lozinke se ne podudaraju")
            return

        user_id = register_user(username, password)
        if user_id:
            self.on_login_success(user_id)
        else:
            self.error_label.config(text="Korisničko ime već postoji")
