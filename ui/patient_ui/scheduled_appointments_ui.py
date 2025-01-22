from customtkinter import *
from ui.patient_ui.utils.constants import *
from ui.patient_ui.utils.utils import *


def load_appointments(filepath):
    """Load appointments from a file and return a list of tuples."""
    appointments = []
    try:
        with open(filepath, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    pet_name, activity, schedule_datetime = parts[:3]
                    appointments.append((pet_name, activity, schedule_datetime))
    except Exception as e:
        print(f"Error loading appointments: {e}")
    return appointments


class ScheduledAppointment:
    def show_scheduled_appointments_ui(self):
        """Display scheduled appointments."""
        self.clear_main_frame()

        # Ensure the parent frame dimensions are accessible
        self.main_frame.update_idletasks()
        self.main_frame.configure(fg_color=MAIN_BG_COLOR)
        main_width = self.main_frame.winfo_width()
        main_height = self.main_frame.winfo_height()

        # Define dimensions and calculate position for centering
        frame_width = 900
        frame_height = 700
        frame_x = (main_width - frame_width) // 2
        frame_y = (main_height - frame_height) // 2 + 20

        # Title
        CTkLabel(
            self.main_frame,
            text="Scheduled Appointments",
            font=FONT_HEADER,
            text_color=TITLE_TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=frame_x, y=frame_y - 80 + 20)

        # Create Scheduled Appointments Frame
        self.scheduled_appointments_frame = CTkFrame(
            self.main_frame,
            corner_radius=10,
            width=frame_width,
            height=frame_height,
            fg_color=MAIN_BG_COLOR,
        )
        self.scheduled_appointments_frame.place(x=frame_x, y=frame_y)

        # Table Headers
        headers = ["Pet Name", "Activity", "Scheduled Appointment"]
        for col, header in enumerate(headers):
            CTkLabel(
                self.scheduled_appointments_frame,
                text=header,
                width=180,  # Adjusted for consistent width
                anchor="w",
                font=FONT_TABLE_HEADER,
                text_color=TABLE_HEADER_TEXT_COLOR,
                fg_color=MAIN_BG_COLOR,
            ).grid(row=0, column=col, padx=5, pady=15, sticky="w")

        # Draw top border line below the headers
        CTkFrame(
            self.scheduled_appointments_frame,
            height=3,
            fg_color=TABLE_BORDER_COLOR,
        ).grid(row=1, column=0, columnspan=len(headers), sticky="we", padx=5)

        try:
            # Load scheduled appointments
            appointments = load_appointments(APPROVED_APPOINTMENT_FILE)

            # Display message if no appointments are found
            if not appointments:
                CTkLabel(
                    self.scheduled_appointments_frame,
                    text="No scheduled appointments found.",
                    font=FONT_NO_DATA_MESSAGE,
                    text_color=NO_DATA_TEXT_COLOR,
                    fg_color=MAIN_BG_COLOR,
                ).grid(row=2, column=0, columnspan=len(headers), pady=20)
            else:
                # Populate the table with appointment details
                for i, appointment in enumerate(appointments, start=2):
                    pet_name, activity, schedule_datetime = appointment

                    CTkLabel(
                        self.scheduled_appointments_frame,
                        text=pet_name,
                        width=150,
                        anchor="w",
                        font=FONT_TABLE_ROW,
                        text_color=TABLE_ROW_TEXT_COLOR,
                        fg_color=MAIN_BG_COLOR,
                    ).grid(row=i, column=0, padx=10, pady=10, sticky="w")

                    CTkLabel(
                        self.scheduled_appointments_frame,
                        text=activity,
                        width=150,
                        anchor="w",
                        font=FONT_TABLE_ROW,
                        text_color=TABLE_ROW_TEXT_COLOR,
                        fg_color=MAIN_BG_COLOR,
                    ).grid(row=i, column=1, padx=10, pady=10, sticky="w")

                    CTkLabel(
                        self.scheduled_appointments_frame,
                        text=schedule_datetime,
                        width=150,
                        anchor="w",
                        font=FONT_TABLE_ROW,
                        text_color=TABLE_ROW_TEXT_COLOR,
                        fg_color=MAIN_BG_COLOR,
                    ).grid(row=i, column=2, padx=10, pady=10, sticky="w")
        except FileNotFoundError:
            CTkLabel(
                self.scheduled_appointments_frame,
                text="No scheduled appointments file found.",
                font=FONT_NO_DATA_MESSAGE,
                text_color=NO_DATA_TEXT_COLOR,
                fg_color=MAIN_BG_COLOR,
            ).grid(row=2, column=0, columnspan=len(headers), pady=20)