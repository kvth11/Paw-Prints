from PIL import Image, UnidentifiedImageError
from customtkinter import CTkImage, CTkToplevel, CTkLabel

def load_image(path, size=None):
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return CTkImage(dark_image=img, size=size)
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
    except UnidentifiedImageError:
        print(f"Invalid image file at {path}")
    return None


def show_notification(master, message, color, duration=3000):
    """Display a notification popup."""
    notification = CTkToplevel(master)
    notification.overrideredirect(True)
    notification.configure(fg_color=color)

    master_x = master.winfo_x()
    master_y = master.winfo_y()
    master_width = master.winfo_width()

    notification_width = 450
    notification_height = 50
    notification_x = master_x + master_width - notification_width - 20
    notification_y = master_y + 20

    notification.geometry(f"{notification_width}x{notification_height}+{notification_x}+{notification_y}")

    CTkLabel(
        notification, 
        text=message, 
        font=("Poppins", 16), 
        text_color="white", 
        fg_color=color,
        corner_radius=10,
    ).pack(fill="both", expand=True, padx=10, pady=10)

    notification.after(duration, notification.destroy)