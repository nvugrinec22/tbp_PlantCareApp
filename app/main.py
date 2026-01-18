import tkinter as tk
from auth import AuthFrame
from gui_main import MainWindow
from utils import BG_MAIN

def clear_root():
    for widget in root.winfo_children():
        widget.destroy()

def start_app(user_id):
    clear_root()
    MainWindow(root, user_id, on_logout=show_login)

def show_login():
    clear_root()
    AuthFrame(root, on_login_success=start_app).pack(
        fill=tk.BOTH, expand=True
    )

root = tk.Tk()
root.configure(bg=BG_MAIN)
root.title("Plant Care App")
root.geometry("500x400")
root.minsize(600, 500)

show_login()
root.mainloop()


