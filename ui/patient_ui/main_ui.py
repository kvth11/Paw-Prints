from customtkinter import *
from ui.patient_ui.utils.constants import *
from ui.patient_ui.utils.utils import *
from ui.patient_ui.set_appointment_ui import SetAppointmentUI
from ui.patient_ui.scheduled_appointments_ui import ScheduledAppointment


class PatientUI(SetAppointmentUI, ScheduledAppointment):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Patient Portal")
        self.master.geometry(WINDOW_GEOMETRY)
        self.create_patient_ui()

    def create_patient_ui(self):
        # Add Background Image
        self.bg_img = load_image(BG_IMAGE_PATH, size=(1440, 900))
        if self.bg_img:
            self.bg_label = CTkLabel(self.master, image=self.bg_img, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Background image not found at {BG_IMAGE_PATH}.")

        # Navigation Frame
        self.nav_frame = CTkFrame(self.master, width=250, fg_color=COLOR_NAV_BG)
        self.nav_frame.place(x=0, y=0, relheight=1)

        # Add Logo to Navigation Panel
        self.logo_img = load_image(LOGO_IMAGE_PATH, size=(200, 200))
        if self.logo_img:
            self.logo_label = CTkLabel(self.nav_frame, image=self.logo_img, text="")
            self.logo_label.pack(pady=20)
        else:
            print(f"Logo image not found at {LOGO_IMAGE_PATH}.")

        # Navigation Buttons
        self.nav_buttons = []
        nav_buttons = [
            ("Set Appointment", self.show_set_appointment_ui),
            ("Scheduled Appointments", self.show_scheduled_appointments_ui),
        ]
        self.last_clicked_button = None

        for text, command in nav_buttons:
            btn = CTkButton(
                self.nav_frame,
                text=text,
                font=FONT_NAV_BUTTON,
                text_color=TEXT_COLOR,
                fg_color=COLOR_NAV_BG,
                hover_color=BUTTON_HOVER_COLOR,
                command=lambda cmd=command, btn_text=text: self.navigate(cmd, btn_text),
            )
            btn.pack(fill="x", pady=10, padx=20, ipady=10)
            self.nav_buttons.append(btn)

        # Log Out Button
        self.logout_button = CTkButton(
            self.nav_frame,
            text="Log Out",
            text_color=TEXT_COLOR,
            font=FONT_NAV_BUTTON,
            fg_color=BUTTON_LOGOUT_COLOR,
            hover_color=BUTTON_LOGOUT_HOVER_COLOR,
            command=self.logout,
        )
        self.logout_button.pack(side="bottom", fill="x", pady=20, padx=20, ipady=10)

        # Main Content Area
        self.main_frame = CTkFrame(self.master, fg_color="white")
        self.main_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        # Add Background Image to Main Content Area
        self.tab_bg_img = load_image(BG_IMAGE_PATH, size=(1152, 900))
        if self.tab_bg_img:
            self.tab_bg_label = CTkLabel(self.main_frame, image=self.tab_bg_img, text="")
            self.tab_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Tab background image not found at {BG_IMAGE_PATH}.")

        # Welcome Message
        CTkLabel(
            self.main_frame,
            text="Welcome to the Patient Portal! 🐾",
            font=FONT_WELCOME_MESSAGE,
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(relx=0.45, rely=0.45, anchor="center")

    def navigate(self, command, button_text):
        """Handle navigation and button highlighting."""
        self.clear_main_frame()

        # Highlight the last clicked button
        if self.last_clicked_button:
            self.last_clicked_button.configure(fg_color=COLOR_NAV_BG)
        for btn in self.nav_buttons:
            if btn.cget("text") == button_text:
                btn.configure(fg_color=BUTTON_HOVER_COLOR)
                self.last_clicked_button = btn

        # Execute the associated command
        command()

    def clear_main_frame(self):
        """Clear all widgets in the main frame."""
        for widget in self.main_frame.winfo_children():
            if widget != self.tab_bg_label:
                widget.destroy()

    def logout(self):
        """Handle logout functionality."""
        for widget in self.master.winfo_children():
            widget.destroy()
        from ui.role_selection_ui.main_ui import RoleSelectionUI
        RoleSelectionUI(self.master)