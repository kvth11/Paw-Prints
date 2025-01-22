import os

# UI Dimensions
WINDOW_TITLE = "Paw Prints"
WINDOW_GEOMETRY = "1440x900"

# Font Constants
FONT_PRIMARY = ("Poppins", 20, "bold")
FONT_HEADER = ("Poppins", 40, "bold")
FONT_BODY = ("Poppins", 14)
FONT_MEDIUM = ("Poppins", 18)
FONT_SMALL = ("Poppins", 12)

# Color Scheme Constants
MAIN_BG_COLOR = "#fdf6f0"
NAV_BAR_COLOR = "#bfecff"
BUTTON_DOCTOR_COLOR = "#bfecff"
BUTTON_PATIENT_COLOR = "#ffe9b9"
HOVER_DOCTOR_COLOR = "#9ad7f1"
HOVER_PATIENT_COLOR = "#f3d799"
BG_COLOR = "#fdf6f0"
TEXT_COLOR = "#667075"
ERROR_COLOR = "#f0a0a0"
SUCCESS_COLOR = "#a0da7d"
BUTTON_HOVER_COLOR = "#e8f5fd"
BUTTON_TEXT_COLOR = "#ffffff"

# Image Paths
CURRENT_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")
BG_IMAGE_PATH = os.path.join(IMAGE_DIR, "bg.png")
LOGO_IMAGE_PATH = os.path.join(IMAGE_DIR, "logo.png")