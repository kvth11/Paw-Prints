import os
from datetime import datetime
from customtkinter import CTkToplevel, CTkLabel

def load_file_lines(filepath):
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []
    
def write_file(filepath, lines, mode="w"):
    """Write lines to the specified file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Write to the file
        with open(filepath, mode) as file:
            if isinstance(lines, list):
                file.writelines(lines)
            else:
                file.write(lines)
    except Exception as e:
        print(f"Error: Could not write to file {filepath}. Exception: {e}")
        raise IOError(f"Could not write to file {filepath}: {e}")

def write_to_file(filepath, content, mode="a"):
    try:
        with open(filepath, mode) as file:
            file.write(content)
    except Exception as e:
        raise IOError(f"Could not write to file {filepath}: {e}")

def format_datetime(date, time):
    """Formats date and time into 'MM/DD/YY at HH:MM AM/PM'."""
    return f"{date} at {time}"

def file_exists(filepath):
    return os.path.exists(filepath)

def create_notification(master, message, color, duration=3000):
    notification = CTkToplevel(master)
    notification.overrideredirect(True)
    notification.configure(fg_color=color)

    master.update_idletasks()
    master_x, master_y = master.winfo_x(), master.winfo_y()
    master_width = master.winfo_width()
    notification_width, notification_height = 450, 50
    notification_x = master_x + master_width - notification_width - 20
    notification_y = master_y + 20
    notification.geometry(f"{notification_width}x{notification_height}+{notification_x}+{notification_y}")

    CTkLabel(
        notification,
        text=message,
        font=("Poppins", 14),
        text_color="white",
        fg_color=color,
        corner_radius=10,
    ).pack(fill="both", expand=True, padx=10, pady=10)

    master.after(duration, notification.destroy)