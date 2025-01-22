from customtkinter import *
from ui.role_ui.utils.utils import *
from ui.role_ui.utils.constants import *
from ui.doctor_ui.main_ui import DoctorUI
from ui.patient_ui.main_ui import PatientUI


class RoleUI:
    def __init__(self, master, role):
        self.master = master
        self.role = role
        self.master.title(f"{role} Portal")
        self.master.geometry("1440x900")  # Adjusted window size
        self.is_login_mode = True  # Start in login mode
        self.create_role_ui()

    def create_role_ui(self):
        # Load and display background image
        self.bg_img = load_image(BG_IMAGE_PATH, size=(1440, 900))  # Store as an instance variable
        if self.bg_img:
            bg_label = CTkLabel(self.master, image=self.bg_img, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main frame for login/signup details
        self.main_frame = CTkFrame(
            self.master,
            fg_color="white",
            bg_color=MAIN_BG_COLOR,
            corner_radius=40,
            width=700,
            height=850,
        )
        self.main_frame.place(relx=0.6, rely=0.5, anchor="center")

        # Title
        title = CTkLabel(
            self.main_frame,
            text=f"{self.role} Portal",
            font=FONT_HEADER,
            text_color=TEXT_COLOR,
        )
        title.pack(pady=40)

        # Username entry
        CTkLabel(
            self.main_frame,
            text="Username:",
            font=FONT_PRIMARY,
            text_color=TEXT_COLOR,
        ).pack(anchor="w", padx=50, pady=10)

        self.username_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter your username",
            font=FONT_MEDIUM,
            height=50,
        )
        self.username_entry.pack(fill="x", padx=50, pady=10)

        # Password entry
        CTkLabel(
            self.main_frame,
            text="Password:",
            font=FONT_PRIMARY,
            text_color=TEXT_COLOR,
        ).pack(anchor="w", padx=50, pady=10)

        self.password_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter your password",
            font=FONT_MEDIUM,
            height=50,
            show="●",
        )
        self.password_entry.pack(fill="x", padx=50, pady=10)

        # Action Button (Login/Sign-Up)
        self.action_button = CTkButton(
            self.main_frame,
            text="Login",
            command=self.handle_action,
            font=FONT_PRIMARY,
            fg_color=BUTTON_DOCTOR_COLOR,
            text_color=TEXT_COLOR,
            hover_color=HOVER_DOCTOR_COLOR,
            corner_radius=15,
            height=55,
        )
        self.action_button.pack(pady=30, padx=50, fill="x")

        # Toggle Button (Switch Login/Sign-Up)
        self.toggle_button = CTkButton(
            self.main_frame,
            text="Switch to Sign Up",
            command=self.toggle_mode,
            font=FONT_PRIMARY,
            fg_color=BUTTON_PATIENT_COLOR,
            text_color=TEXT_COLOR,
            hover_color=HOVER_PATIENT_COLOR,
            corner_radius=15,
            height=55,
        )
        self.toggle_button.pack(pady=20, padx=50, fill="x")

        # Back Button
        back_button = CTkButton(
            self.main_frame,
            text="Back to Role Selection",
            command=self.go_to_role_selection,
            font=FONT_PRIMARY,
            fg_color=MAIN_BG_COLOR,
            text_color=TEXT_COLOR,
            hover_color="#ecdaca",
            corner_radius=15,
            height=55,
        )
        back_button.pack(pady=30, padx=50, fill="x")

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.action_button.configure(text="Sign Up" if not self.is_login_mode else "Login")
        self.toggle_button.configure(text="Switch to Login" if not self.is_login_mode else "Switch to Sign Up")

    def handle_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            show_notification(self.master, "❌ Please fill out all fields.", ERROR_COLOR)
            return

        if len(username) < 8:
            show_notification(self.master, "❌ Username must be at least 8 characters long.", ERROR_COLOR)
            return

        if len(password) < 8:
            show_notification(self.master, "❌ Password must be at least 8 characters long.", ERROR_COLOR)
            return

        if self.is_login_mode:
            self.handle_login(username, password)
        else:
            self.handle_signup(username, password)

    def handle_login(self, username, password):
        """Validate and log in the user."""
        try:
            with open(CREDENTIALS_FILE, "r") as file:
                for line in file:
                    stored_role, stored_username, stored_password = line.strip().split(",")
                    if self.role == stored_role and username == stored_username and password == stored_password:
                        self.main_frame.destroy()
                        (DoctorUI if self.role == "Doctor" else PatientUI)(self.master)
                        return
            show_notification(self.master, "❌ Invalid Credentials.", ERROR_COLOR)
        except FileNotFoundError:
            show_notification(self.master, f"❌ No users found. Please sign up.", ERROR_COLOR)

    def handle_signup(self, username, password):
        """Save new user credentials."""
        try:
            # Ensure the directory for the credentials file exists
            os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)

            # Check if the username already exists
            if os.path.exists(CREDENTIALS_FILE):
                with open(CREDENTIALS_FILE, "r") as file:
                    for line in file:
                        _, stored_username, _ = line.strip().split(",")
                        if stored_username == username:
                            show_notification(
                                self.master,
                                f"❌ Username '{username}' already exists.",
                                ERROR_COLOR,
                            )
                            return

            # Append new user credentials
            with open(CREDENTIALS_FILE, "a") as file:
                file.write(f"{self.role},{username},{password}\n")

            # Notify success
            show_notification(self.master, "✅ Sign Up Successful! You can now log in.", SUCCESS_COLOR)
            self.toggle_mode()  # Switch to Login mode
        except Exception as e:
            # Notify error
            show_notification(self.master, f"❌ Error during sign-up: {e}", ERROR_COLOR)

    def go_to_role_selection(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        from ui.role_selection_ui.main_ui import RoleSelectionUI
        RoleSelectionUI(self.master)

if __name__ == "__main__":
    root = CTk()
    app = RoleUI(root, role="Doctor")
    root.mainloop()