def center_window(win, parent, width, height):
    parent.update_idletasks()

    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()
    parent_w = parent.winfo_width()
    parent_h = parent.winfo_height()

    x = parent_x + (parent_w - width) // 2
    y = parent_y + (parent_h - height) // 2

    win.geometry(f"{width}x{height}+{x}+{y}")

BG_MAIN = "#f6f5f2"     
BG_CARD = "#ffffff"    
GREEN_MAIN = "#a8c686"  
GREEN_DARK = "#6b8f71"  
BORDER = "#ddd8ce"    
TEXT_MAIN = "#2f2f2f"
TEXT_MUTED = "#6f6f6f"
ERROR_RED = "#b00020"

