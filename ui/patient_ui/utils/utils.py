# utils.py

from PIL import Image
from customtkinter import CTkImage, CTkToplevel, CTkLabel
import os

def load_file_lines(filepath):
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def load_image(path, size=None):
    """Load and resize an image."""
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return CTkImage(dark_image=img, size=size)
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
    except Exception as e:
        print(f"Error loading image: {e}")
    return None

def show_notification(master, message, color, duration=3000):
    """Display a notification popup."""
    notification = CTkToplevel(master)
    notification.overrideredirect(True)
    notification.configure(fg_color=color)

    # Ensure geometry is updated
    master.update_idletasks()

    # Calculate position
    master_x = master.winfo_x()
    master_y = master.winfo_y()
    master_width = master.winfo_width()
    notification_width = 450
    notification_height = 50
    notification_x = master_x + master_width - notification_width - 20
    notification_y = master_y + 40

    # Ensure position stays within screen bounds
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    notification_x = min(notification_x, screen_width - notification_width)
    notification_y = max(notification_y, 0)

    notification.geometry(f"{notification_width}x{notification_height}+{notification_x}+{notification_y}")

    # Add notification content
    CTkLabel(
        notification,
        text=message,
        font=("Poppins", 14),
        text_color="white",
        fg_color=color,
        corner_radius=10,
    ).pack(fill="both", expand=True, padx=10, pady=10)

    # Automatically destroy the notification
    notification.after(duration, notification.destroy)

def load_appointments(file_path):
    """Load and parse appointments from a file."""
    appointments = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                details = line.strip().split(",")
                if len(details) >= 6:
                    pet_name, _, _, _, activity, schedule_datetime = details
                    appointments.append((pet_name, activity, schedule_datetime))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return appointments