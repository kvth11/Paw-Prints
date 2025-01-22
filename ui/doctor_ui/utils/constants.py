import os

# UI Dimensions
WINDOW_TITLE = "Doctor Portal"
WINDOW_GEOMETRY = "1440x900"

# Fonts
FONT_PRIMARY = ("Poppins", 16, "bold")
FONT_LARGE = ("Poppins", 36, "bold")
FONT_MEDIUM = ("Poppins", 18)
FONT_SMALL = ("Poppins", 14)

# Colors
COLOR_NAV_BG = "#bfecff"
COLOR_MAIN_BG = "#fdf6f0"
COLOR_TEXT_PRIMARY = "#667075"
COLOR_BUTTON_HOVER = "#ffe9b9"
COLOR_BUTTON_LOGOUT = "#fcb2b2"
COLOR_BUTTON_HOVER_LOGOUT = "#ec8b8b"
COLOR_SUCCESS = "#a0da7d"
COLOR_ERROR = "#f0a0a0"

# Paths
CURRENT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")
BG_IMAGE_PATH = os.path.join(IMAGE_DIR, "bg3.png")
LOGO_IMAGE_PATH = os.path.join(IMAGE_DIR, "logo2.png")


# File Paths
DATABASE_FOLDER = "database"
CREDENTIALS_FILE = os.path.join(DATABASE_FOLDER, "credentials.txt")
PENDING_ACTIVITIES_FILE = os.path.join(DATABASE_FOLDER, "pending_activities.txt")
APPROVED_APPOINTMENTS_FILE = os.path.join(DATABASE_FOLDER, "approved_appointments.txt")
ACTIVITY_ARCHIVE_FILE = os.path.join(DATABASE_FOLDER, "activity_archive.txt")
PET_PROFILES_FILE = os.path.join(DATABASE_FOLDER, "pet_profiles.txt")
APPOINTMENT_REQUESTS_FILE = os.path.join(DATABASE_FOLDER, "appointment_requests.txt")
DECLINED_APPOINTMENTS_FILE = os.path.join(DATABASE_FOLDER, "declined_appointments.txt")


# Default Values
DEFAULT_SPECIES_OPTIONS = ["Dog", "Cat", "Bird", "Rabbit", "Hamster"]
DEFAULT_TIME_OPTIONS = [
    "06:00 AM", "07:00 AM", "08:00 AM", "09:00 AM", "10:00 AM",
    "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM",
    "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM", "08:00 PM"
]