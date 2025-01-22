from customtkinter import *
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.main_ui import *

class AppointmentUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame
    
    def appointment_ui(self):
        self.clear_tab_frame()

        self.tab_frame.update_idletasks()
        self.tab_frame.configure(fg_color=COLOR_MAIN_BG)
        tab_width = self.tab_frame.winfo_width()
        tab_height = self.tab_frame.winfo_height()

        frame_width = 1100
        frame_height = 700
        frame_x = 200
        frame_y = (tab_height - frame_height) // 2 + 20

        CTkLabel(
            self.tab_frame,
            text="Appointment Requests",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=frame_x, y=frame_y - 80 + 20)

        self.appointment_requests_frame = CTkFrame(
            self.tab_frame,
            corner_radius=10,
            width=frame_width,
            height=frame_height,
            fg_color=COLOR_MAIN_BG
        )
        self.appointment_requests_frame.place(x=frame_x, y=frame_y)

        headers = ["Pet Details", "Activity", "Date & Time", "Actions", ""]
        for i, header in enumerate(headers):
            CTkLabel(
                self.appointment_requests_frame,
                text=header,
                width=150,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=3, pady=15, sticky="w")

        CTkFrame(
            self.appointment_requests_frame,
            height=3,
        ).grid(row=1, column=0, columnspan=len(headers), sticky="we", padx=5)

        requests = load_file_lines(APPOINTMENT_REQUESTS_FILE)

        if not requests:
            CTkLabel(
                self.appointment_requests_frame,
                text="No pending requests!",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=2, column=0, columnspan=len(headers), pady=20)
        else:
            for i, request in enumerate(requests, start=2):
                try:
                    pet_details, activity, schedule_datetime = request.strip().split(",")[:3]

                    CTkLabel(
                        self.appointment_requests_frame,
                        text=pet_details,
                        width=150,
                        anchor="w",
                        font=FONT_MEDIUM,
                        text_color=COLOR_TEXT_PRIMARY,
                        fg_color=COLOR_MAIN_BG
                    ).grid(row=i, column=0, padx=15, pady=10, sticky="w")

                    CTkLabel(
                        self.appointment_requests_frame,
                        text=activity,
                        width=150,
                        anchor="w",
                        font=FONT_MEDIUM,
                        text_color=COLOR_TEXT_PRIMARY,
                        fg_color=COLOR_MAIN_BG
                    ).grid(row=i, column=1, padx=15, pady=10, sticky="w")

                    CTkLabel(
                        self.appointment_requests_frame,
                        text=schedule_datetime,
                        width=150,
                        anchor="w",
                        font=FONT_MEDIUM,
                        text_color=COLOR_TEXT_PRIMARY,
                        fg_color=COLOR_MAIN_BG
                    ).grid(row=i, column=2, padx=15, pady=10, sticky="w")

                    CTkButton(
                        self.appointment_requests_frame,
                        text="Approve",
                        font=FONT_MEDIUM,
                        text_color="white",
                        fg_color=COLOR_SUCCESS,
                        hover_color="#88c070",
                        command=lambda req=request: self.approve_request(req),
                    ).grid(row=i, column=3, padx=10)

                    CTkButton(
                        self.appointment_requests_frame,
                        text="Decline",
                        font=FONT_MEDIUM,
                        text_color="white",
                        fg_color=COLOR_ERROR,
                        hover_color="#d08080",
                        command=lambda req=request: self.decline_request(req),
                    ).grid(row=i, column=4, padx=10)

                except ValueError:
                    print(f"Skipping malformed request: {request.strip()}")  # Log the issue

    def approve_request(self, request):
        try:
            # Load all requests
            requests = load_file_lines(APPOINTMENT_REQUESTS_FILE)

            if request in requests:
                # Remove the approved request from pending requests
                requests.remove(request)

                # Write the updated pending requests back to the file
                write_to_file(APPOINTMENT_REQUESTS_FILE, "\n".join(requests) + "\n", mode="w")

                # Append the approved request to approved appointments
                write_to_file(APPROVED_APPOINTMENTS_FILE, request.strip() + "\n", mode="a")

                # Safely unpack the request string
                try:
                    # Unpack the fields from the request (adjust the indices if needed)
                    pet_name, owner_name, age, species, activity, schedule_datetime = request.strip().split(",")

                    # Correctly format the entry for pending activities
                    formatted_entry = f"{activity},{pet_name},{schedule_datetime}\n"

                    # Add to pending activities for the doctor
                    write_to_file(PENDING_ACTIVITIES_FILE, formatted_entry, mode="a")

                    # Notify success
                    create_notification(
                        self.master,
                        "✅ Appointment approved and added to pending activities.",
                        COLOR_SUCCESS,
                    )
                except ValueError:
                    create_notification(self.master, "❌ Invalid appointment request format.", COLOR_ERROR)

            # Refresh the appointment UI
            self.appointment_ui()
        except Exception as e:
            create_notification(self.master, f"❌ Error approving appointment: {e}", COLOR_ERROR)

    def decline_request(self, request):
        try:
            # Load all pending requests
            requests = load_file_lines(APPOINTMENT_REQUESTS_FILE)

            # Ensure the request exists in the list
            if request in requests:
                # Remove the declined request
                requests.remove(request)

                # Write the updated requests back to the appointment requests file
                write_to_file(APPOINTMENT_REQUESTS_FILE, "\n".join(requests) + "\n", mode="w")

                # Append the declined request to the declined appointments file
                write_to_file(DECLINED_APPOINTMENTS_FILE, request.strip() + "\n", mode="a")

                # Notify the user
                create_notification(self.master, "❌ Appointment declined.", COLOR_ERROR)
            else:
                create_notification(self.master, "❌ Error: Request not found.", COLOR_ERROR)

            # Refresh the appointment UI
            self.appointment_ui()
        except Exception as e:
            # Notify about the exception
            create_notification(self.master, f"❌ Error declining appointment: {e}", COLOR_ERROR)

    def write_to_file(filepath, content, mode="w"):
        """Write content to a file, creating directories if necessary."""
        try:
            directory = os.path.dirname(filepath)
            if not os.path.exists(directory):
                os.makedirs(directory)  # Create the directory if it doesn't exist
            with open(filepath, mode) as file:
                if isinstance(content, list):
                    file.writelines(content)
                else:
                    file.write(content)
        except Exception as e:
            raise IOError(f"Could not write to file {filepath}: {e}")