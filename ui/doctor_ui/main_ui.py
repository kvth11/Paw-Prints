from customtkinter import *
from PIL import Image
import os
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.add_pet_ui import AddPetUI
from ui.doctor_ui.activity_manager_ui import ActivityManagerUI
from ui.doctor_ui.pet_profiles_ui import PetProfilesUI
from ui.doctor_ui.schedule_ui import ScheduleUI
from ui.doctor_ui.archive_ui import ArchiveUI
from ui.doctor_ui.appointment_ui import AppointmentUI

class DoctorUI:
    def __init__(self, master):
        self.master = master
        self.master.title(WINDOW_TITLE)
        self.master.geometry(WINDOW_GEOMETRY)

        # Create the main content area
        self.tab_frame = CTkFrame(self.master, fg_color=COLOR_MAIN_BG)
        self.tab_frame.place(relx=0.099, rely=0, relwidth=1, relheight=1)

        # Initialize sub-UI components with the necessary references
        self.add_pet_ui = AddPetUI(self.master, self.tab_frame, self.clear_tab_frame)
        self.activity_manager_ui = ActivityManagerUI(self.master, self.tab_frame, self.clear_tab_frame)
        self.pet_profiles_ui = PetProfilesUI(self.master, self.tab_frame, self.clear_tab_frame)
        self.schedule_ui = ScheduleUI(self.master, self.tab_frame, self.clear_tab_frame)
        self.archive_ui = ArchiveUI(self.master, self.tab_frame, self.clear_tab_frame)
        self.appointment_ui = AppointmentUI(self.master, self.tab_frame, self.clear_tab_frame)

        # Create UI components
        self.doctor_ui()

    def doctor_ui(self):
        # Default 'tab_bg_label' to 'None'
        self.tab_bg_label = None

        current_dir = os.path.dirname(__file__)
        BG_IMAGE_PATH = os.path.join(current_dir, "images", "bg3.png")
        LOGO_IMAGE_PATH = os.path.join(current_dir, "images", "logo2.png")

        # Add Background Image
        if file_exists(BG_IMAGE_PATH):
            tab_bg_img = CTkImage(dark_image=Image.open(BG_IMAGE_PATH), size=(1150, 900))
            self.tab_bg_label = CTkLabel(self.tab_frame, image=tab_bg_img, text="")
            self.tab_bg_label.image = tab_bg_img
            self.tab_bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Navigation Frame
        self.nav_frame = CTkFrame(self.master, width=250, fg_color=COLOR_NAV_BG)
        self.nav_frame.place(x=0, y=0, relheight=1)

        # Add Logo to Navigation Panel
        if file_exists(LOGO_IMAGE_PATH):
            logo_img = CTkImage(dark_image=Image.open(LOGO_IMAGE_PATH), size=(200, 200))
            self.logo_label = CTkLabel(self.nav_frame, image=logo_img, text="")
            self.logo_label.image = logo_img
            self.logo_label.pack(pady=20)

        # Navigation Buttons
        nav_buttons = [
            ("Pet Profile Setup", self.add_pet_ui.add_pet_ui),
            ("Activity Manager", self.activity_manager_ui.activity_manager_ui),
            ("Pet Profiles", self.pet_profiles_ui.pet_profiles_ui),
            ("Schedule Overview", self.schedule_ui.schedule_ui),
            ("Activity Archive", self.archive_ui.archive_ui),
            ("Appointment Requests", self.appointment_ui.appointment_ui),
        ]
        self.nav_buttons = []
        self.last_clicked_button = None

        for text, command in nav_buttons:
            btn = CTkButton(
                self.nav_frame,
                text=text,
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_NAV_BG,
                hover_color=COLOR_BUTTON_HOVER,
                command=lambda cmd=command, btn_text=text: self.navigate(cmd, btn_text),
            )
            btn.pack(fill="x", pady=10, padx=20, ipady=10)
            self.nav_buttons.append(btn)

        # Log Out Button
        self.logout_button = CTkButton(
            self.nav_frame,
            text="Log Out",
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_PRIMARY,
            fg_color=COLOR_BUTTON_LOGOUT,
            hover_color=COLOR_BUTTON_HOVER_LOGOUT,
            command=self.logout,
        )
        self.logout_button.pack(side="bottom", fill="x", pady=20, padx=20, ipady=10)

        # Welcome Message
        self.feedback_label = CTkLabel(
            self.tab_frame,
            text="Welcome to the Doctor Portal! 🐾",
            font=FONT_LARGE,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG,
        )
        self.feedback_label.place(relx=0.45, rely=0.45, anchor="center")

    def navigate(self, command, button_text):
        self.clear_tab_frame()

        if self.last_clicked_button:
            self.last_clicked_button.configure(fg_color=COLOR_NAV_BG)
        for btn in self.nav_buttons:
            if btn.cget("text") == button_text:
                btn.configure(fg_color=COLOR_BUTTON_HOVER)
                self.last_clicked_button = btn

        command()

    def clear_tab_frame(self):
        for widget in self.tab_frame.winfo_children():
            if widget != self.tab_bg_label:
                widget.destroy()

    def logout(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from ui.role_selection_ui.main_ui import RoleSelectionUI
        RoleSelectionUI(self.master)

    def show_notification(self, message, color, duration=3000):
        create_notification(self.master, message, color, duration)