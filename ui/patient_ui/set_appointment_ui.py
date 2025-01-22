from datetime import datetime
from tkcalendar import Calendar
from customtkinter import *
from ui.patient_ui.utils.constants import *
from ui.patient_ui.utils.utils import *


class SetAppointmentUI:
    def show_set_appointment_ui(self):
        """Display the Set Appointment UI."""
        self.clear_main_frame()

        # Set background color
        self.main_frame.configure(fg_color=MAIN_BG_COLOR)

        # Title
        CTkLabel(
            self.main_frame,
            text="Set Appointment",
            font=("Poppins", 36, "bold"),
            text_color=TITLE_TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=50, y=40)

        # Left Column: Pet and Activity Details
        column_x = 50
        field_width = 303  # Increased by 3px

        # Pet Name Entry (Instance Variable)
        CTkLabel(
            self.main_frame,
            text="Pet Name:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x, y=120)
        self.pet_name_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter Pet Name",
            font=("Poppins", 16),
            width=field_width,
            height=35,
        )
        self.pet_name_entry.place(x=column_x, y=160)

        # Owner Name Entry (Instance Variable)
        CTkLabel(
            self.main_frame,
            text="Owner Name:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x, y=220)
        self.owner_name_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter Owner Name",
            font=("Poppins", 16),
            width=field_width,
            height=35,
        )
        self.owner_name_entry.place(x=column_x, y=260)

        # Age Entries: Years and Months (Instance Variables)
        CTkLabel(
            self.main_frame,
            text="Age (Years):",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x, y=320)
        self.years_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Years",
            font=("Poppins", 16),
            width=field_width // 2 - 10,
            height=35,
        )
        self.years_entry.place(x=column_x, y=360)

        CTkLabel(
            self.main_frame,
            text="Age (Months):",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x + field_width // 2 + 20, y=320)
        self.months_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Months",
            font=("Poppins", 16),
            width=field_width // 2 - 10,
            height=35,
        )
        self.months_entry.place(x=column_x + field_width // 2 + 20, y=360)

        # Species Dropdown (Instance Variable)
        CTkLabel(
            self.main_frame,
            text="Species:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x, y=420)
        self.species_var = StringVar(value="Dog")
        CTkOptionMenu(
            self.main_frame,
            variable=self.species_var,
            values=["Dog", "Cat", "Bird", "Rabbit", "Hamster"],
            text_color=TEXT_COLOR,
            font=("Poppins", 16),
            fg_color=COLOR_NAV_BG,
            button_color=COLOR_NAV_BG,
            button_hover_color="#ffe9b9",
            height=35,
        ).place(x=column_x, y=460)

        # Concern Entry (Instance Variable)
        CTkLabel(
            self.main_frame,
            text="Concern:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=column_x, y=520)
        self.activity_entry = CTkEntry(
            self.main_frame,
            placeholder_text="Enter Your Concern",
            font=("Poppins", 16),
            width=field_width,
            height=35,
        )
        self.activity_entry.place(x=column_x, y=560)

        # Right Column: Date, Time, and Submission
        right_column_x = column_x + 400

        # Calendar
        CTkLabel(
            self.main_frame,
            text="Select Date:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=right_column_x, y=120)
        self.calendar = Calendar(self.main_frame, selectmode="day")
        self.calendar.place(x=right_column_x, y=160, width=field_width, height=250)

        # Time Dropdown (Instance Variable)
        CTkLabel(
            self.main_frame,
            text="Select Time:",
            font=("Poppins", 16),
            text_color=TEXT_COLOR,
            fg_color=MAIN_BG_COLOR,
        ).place(x=right_column_x, y=440)
        self.time_var = StringVar(value="06:00 AM")
        CTkOptionMenu(
            self.main_frame,
            variable=self.time_var,
            values=[
                f"{hour:02d}:00 {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21)
            ],
            text_color=TEXT_COLOR,
            font=("Poppins", 16),
            fg_color=COLOR_NAV_BG,
            button_color=COLOR_NAV_BG,
            button_hover_color="#ffe9b9",
            height=35,
        ).place(x=right_column_x, y=480)

        # Submit Button
        CTkButton(
            self.main_frame,
            text="Submit Appointment",
            text_color=TEXT_COLOR,
            font=("Poppins", 16, "bold"),
            fg_color=COLOR_NAV_BG,
            hover_color="#ffe9b9",
            command=self.submit_appointment,
            width=field_width,
            height=50,
        ).place(x=right_column_x, y=550)

    def submit_appointment(self):
        """Submit an appointment."""
        pet_name = self.pet_name_entry.get()
        owner_name = self.owner_name_entry.get()
        years = self.years_entry.get()
        months = self.months_entry.get()
        species = self.species_var.get()
        activity = self.activity_entry.get()
        date = self.calendar.get_date()
        time = self.time_var.get()

        if not (pet_name and owner_name and years and months and species and activity and date and time):
            show_notification(self.main_frame, "❌ Please fill out all fields.", color="#f0a0a0", duration=3000)
            return

        try:
            # Format the date and time
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%m/%d/%y")
            formatted_time = datetime.strptime(time, "%I:%M %p").strftime("%I:%M %p")
            schedule_datetime = f"{formatted_date} at {formatted_time}"

            # Write appointment to file
            with open(APPOINTMENT_REQUESTS_FILE, "a") as file:
                file.write(f"{pet_name},{owner_name},{years} years {months} months,{species},{activity},{schedule_datetime}\n")

            # Show success notification
            show_notification(self.main_frame, f"✅ Appointment for {pet_name} scheduled on {schedule_datetime}.", color="#a0da7d", duration=3000)

            # Clear inputs
            self.pet_name_entry.delete(0, "end")
            self.owner_name_entry.delete(0, "end")
            self.years_entry.delete(0, "end")
            self.months_entry.delete(0, "end")
            self.activity_entry.delete(0, "end")
            self.species_var.set("Dog")
            self.time_var.set("06:00 AM")

        except Exception as e:
            show_notification(self.main_frame, f"❌ Error: {e}", color="#f0a0a0", duration=3000)