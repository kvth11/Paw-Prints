# constants.py

import os

# UI Dimensions
WINDOW_TITLE = "Patient Portal"
WINDOW_GEOMETRY = "1440x900"

# Paths
CURRENT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(CURRENT_DIR, "..", "images")
BG_IMAGE_PATH = os.path.join(IMAGE_DIR, "bg4.png")
LOGO_IMAGE_PATH = os.path.join(IMAGE_DIR, "logo2.png")

# Base directory for the project
DATABASE_FOLDER = "database"
APPOINTMENT_REQUESTS_FILE = os.path.join(DATABASE_FOLDER, "appointment_requests.txt")
APPROVED_APPOINTMENT_FILE = os.path.join(DATABASE_FOLDER, "approved_appointments.txt")

# Colors
MAIN_BG_COLOR = "#fdf6f0"
TITLE_TEXT_COLOR = "#f1ca75"
TEXT_COLOR = "#667075"
TABLE_HEADER_TEXT_COLOR = "#667075"
TABLE_ROW_TEXT_COLOR = "#667075"
NO_DATA_TEXT_COLOR = "#667075"
TABLE_BORDER_COLOR = "#cccccc"
COLOR_NAV_BG = "#bfecff"
BUTTON_HOVER_COLOR = "#ffe9b9"
BUTTON_LOGOUT_COLOR = "#fcb2b2"
BUTTON_LOGOUT_HOVER_COLOR = "#ec8b8b"
BUTTON_TEXT_COLOR = "white"

# Fonts
FONT_HEADER = ("Poppins", 40, "bold")
FONT_NAV_BUTTON = ("Poppins", 16, "bold")
FONT_TABLE_HEADER = ("Poppins", 16, "bold")
FONT_TABLE_ROW = ("Poppins", 14)
FONT_NO_DATA_MESSAGE = ("Poppins", 16, "italic")
FONT_WELCOME_MESSAGE = ("Poppins", 36, "bold")