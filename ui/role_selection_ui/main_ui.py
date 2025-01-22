from customtkinter import *
from PIL import Image, UnidentifiedImageError
from ui.role_selection_ui.utils.constants import *
from ui.role_selection_ui.utils.utils import *
from ui.role_ui.main_ui import RoleUI

class RoleSelectionUI:
    def __init__(self, master):
        self.master = master
        self.master.title(WINDOW_TITLE)
        self.master.geometry(WINDOW_GEOMETRY)

        self.create_role_selection_ui()

    def create_role_selection_ui(self):
        # Create a frame for the background image
        self.bg_frame = CTkFrame(self.master, fg_color="#fdf6f0")
        self.bg_frame.place(relwidth=1, relheight=1)

        # Load and display background image
        bg_img = load_image(BG_IMAGE_PATH, size=(1440, 900))
        if bg_img:
            CTkLabel(self.bg_frame, image=bg_img, text="").place(x=0, y=0, relwidth=1, relheight=1)

        # Main content frame
        self.content_frame = CTkFrame(self.master, fg_color=MAIN_BG_COLOR)
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Load and display logo
        logo_img = load_image(LOGO_IMAGE_PATH, size=(350, 350))
        if logo_img:
            CTkLabel(self.content_frame, image=logo_img, text="").pack(pady=(0, 70))

        # Title
        CTkLabel(
            self.content_frame,
            text="Choose Your Role",
            font=FONT_HEADER,
            text_color=TEXT_COLOR,
        ).pack(pady=(0, 50))

        # Role Buttons Frame
        role_buttons_frame = CTkFrame(self.content_frame, fg_color="transparent")
        role_buttons_frame.pack(pady=20)

        # Doctor Role Button
        CTkButton(
            role_buttons_frame,
            text="Doctor",
            command=lambda: self.open_role_page("Doctor"),
            font=FONT_PRIMARY,
            fg_color=BUTTON_DOCTOR_COLOR,
            text_color=TEXT_COLOR,
            hover_color=HOVER_DOCTOR_COLOR,
            corner_radius=10,
            width=250,
            height=60,
        ).grid(row=0, column=0, padx=20)

        # Patient Role Button
        CTkButton(
            role_buttons_frame,
            text="Patient",
            command=lambda: self.open_role_page("Patient"),
            font=FONT_PRIMARY,
            fg_color=BUTTON_PATIENT_COLOR,
            text_color=TEXT_COLOR,
            hover_color=HOVER_PATIENT_COLOR,
            corner_radius=10,
            width=250,
            height=60,
        ).grid(row=0, column=1, padx=20)

    def open_role_page(self, role):
        """Opens the appropriate Role UI."""
        for widget in self.master.winfo_children():
            widget.destroy()

        RoleUI(self.master, role)

    def on_close(self):
        if hasattr(self, 'after_id'):
            self.master.after_cancel(self.after_id)
        self.master.destroy()

if __name__ == "__main__":
    root = CTk()
    app = RoleSelectionUI(root)
    root.mainloop()