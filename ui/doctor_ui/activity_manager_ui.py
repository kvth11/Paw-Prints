from customtkinter import *
from tkcalendar import Calendar
from datetime import datetime
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.main_ui import *
from data_structures.activity_manager_ds import *


class ActivityManagerUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame
        self.activity_stack = Stack()

    def activity_manager_ui(self):
        self.clear_tab_frame()

        CTkLabel(
            self.tab_frame,
            text="Activity Manager",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=20)

        CTkLabel(
            self.tab_frame,
            text="Activity Description:",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=100)

        activity_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Enter Activity Description",
            font=FONT_SMALL,
            width=380,
            height=35
        )
        activity_entry.place(x=200, y=140)

        self.activity_entry_field = activity_entry

        CTkLabel(
            self.tab_frame,
            text="Assign Activity to Pet:",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=200)

        pet_names = [line.split("\t")[0] for line in load_file_lines(PET_PROFILES_FILE)]
        pet_var = StringVar(value=pet_names[0] if pet_names else "No pets available")

        CTkOptionMenu(
            self.tab_frame,
            variable=pet_var,
            values=pet_names or ["No pets available"],
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_SMALL,
            fg_color="#bfecff",
            button_color="#bfecff",
            button_hover_color="#ffe9b9",
            height=35
        ).place(x=200, y=240)

        CTkLabel(
            self.tab_frame,
            text="Select Date:",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=300)
        calendar = Calendar(self.tab_frame, selectmode="day")
        calendar.place(x=200, y=340, width=380, height=280)

        CTkLabel(
            self.tab_frame,
            text="Select Time:",
            font=FONT_SMALL,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=640)

        time_options = [f"{hour:02}:00 {'AM' if hour < 12 else 'PM'}" for hour in range(6, 21)]
        time_var = StringVar(value=time_options[0])

        CTkOptionMenu(
            self.tab_frame,
            variable=time_var,
            values=time_options,
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_SMALL,
            fg_color="#bfecff",
            button_color="#bfecff",
            button_hover_color="#ffe9b9",
            height=35
        ).place(x=200, y=680)

        CTkButton(
            self.tab_frame,
            text="Assign Activity",
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=lambda: self.assign_activity(
                activity_entry.get(), pet_var.get(), calendar.get_date(), time_var.get()
            ),
            width=380,
            height=45
        ).place(x=200, y=740)

        # Undo Button
        CTkButton(
            self.tab_frame,
            text="Undo",
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_PRIMARY,
            fg_color="#ffaeae",
            hover_color="#ff7e7e",
            command=self.undo_activity,
            width=380,
            height=45
        ).place(x=600, y=740)

        CTkLabel(
            self.tab_frame,
            text="Pending Activities:",
            font=FONT_PRIMARY,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=650, y=100)

        self.pending_activities_frame = CTkFrame(
            self.tab_frame, corner_radius=10, width=500, height=420, fg_color=COLOR_MAIN_BG
        )
        self.pending_activities_frame.place(x=650, y=140)

        self.update_activity_list()

    def write_file(self, filepath, lines):
        """Overwrite the specified file with the given lines."""
        try:
            with open(filepath, "w") as file:
                file.writelines(lines)
        except Exception as e:
            create_notification(self.master, f"❌ Error writing to file {filepath}: {e}", COLOR_ERROR)

    def load_file(self, filepath):
        """Load lines from a file and handle errors."""
        try:
            with open(filepath, "r") as file:
                return file.readlines()
        except FileNotFoundError:
            create_notification(self.master, f"❌ File not found: {filepath}", COLOR_ERROR)
            return []
        except Exception as e:
            create_notification(self.master, f"❌ Error loading file {filepath}: {e}", COLOR_ERROR)
            return []

    def assign_activity(self, activity, pet_name, date, time):
        if not activity or not pet_name or not date or not time:
            create_notification(self.master, "❌ Please fill out all fields.", COLOR_ERROR)
            return

        try:
            schedule_datetime = format_datetime(date, time)
            activity_record = f"{activity},{pet_name},{schedule_datetime}\n"
            
            # Write to the pending activities file
            write_to_file(PENDING_ACTIVITIES_FILE, activity_record, mode="a")

            # Push the activity to the stack for undo
            self.activity_stack.push(activity_record)

            create_notification(
                self.master,
                f"✅ '{activity}' scheduled for '{pet_name}' on {schedule_datetime}.",
                COLOR_SUCCESS
            )

            # Clear the input field after assigning the activity
            self.activity_entry_field.delete(0, "end")
            self.time_var.set("06:00 AM")
            
            # Update the pending activities list to reflect the new activity
            self.update_activity_list()
        except Exception as e:
            create_notification(self.master, f"❌ Unexpected Error: {e}", COLOR_ERROR)

    def undo_activity(self):
        """Undo the last assigned activity."""
        if self.activity_stack.is_empty():
            create_notification(self.master, "❌ No activity to undo.", COLOR_ERROR)
            return

        # Pop the last activity from the stack
        last_activity = self.activity_stack.pop()

        try:
            # Remove the last activity from the pending activities file
            pending_activities = load_file_lines(PENDING_ACTIVITIES_FILE)
            updated_activities = [line for line in pending_activities if line != last_activity]
            self.write_file(PENDING_ACTIVITIES_FILE, updated_activities)

            create_notification(self.master, "✅ Last activity undone.", COLOR_SUCCESS)
            self.update_activity_list()
        except Exception as e:
            create_notification(self.master, f"❌ Error undoing activity: {e}", COLOR_ERROR)

    def update_activity_list(self):
        """Update the pending activity list display."""
        # Clear existing widgets
        for widget in self.pending_activities_frame.winfo_children():
            widget.destroy()

        # Load pending activities
        pending_activities = []
        for line in self.load_file(PENDING_ACTIVITIES_FILE):
            line = line.strip()
            if not line:
                continue
            try:
                activity, pet_name, date = line.split(",")[:3]
                pending_activities.append({"activity": activity, "pet_name": pet_name, "date": date})
            except ValueError:
                print(f"Skipping malformed entry: {line}")  # Log malformed entries for debugging

        if not pending_activities:
            CTkLabel(
                self.pending_activities_frame,
                text="No pending activities!",
                font=FONT_SMALL,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).pack(pady=20)
            return

        # Display valid pending activities
        for activity in pending_activities:
            frame = CTkFrame(self.pending_activities_frame, fg_color=COLOR_MAIN_BG, corner_radius=10)
            frame.pack(fill="x", pady=5, padx=0.5)

            # Create a BooleanVar for the checkbox state
            completed_var = BooleanVar()

            checkbox = CTkCheckBox(
                frame,
                text=f"{activity['activity']} - {activity['pet_name']} on {activity['date']}",
                variable=completed_var,
                text_color=COLOR_TEXT_PRIMARY,
                font=FONT_SMALL,
                fg_color=COLOR_MAIN_BG,
                command=lambda: self.complete_activity(activity, completed_var)
            )
            checkbox.pack(side="left", padx=10)

    def complete_activity(self, activity, completed_var):
        """Mark an activity as completed, update files, and refresh the UI."""
        if not completed_var.get():  # Ignore if the checkbox is unchecked
            return

        try:
            # Construct the activity line
            activity_line = f"{activity['activity']},{activity['pet_name']},{activity['date']}\n"

            # Remove from pending activities
            pending_activities = self.load_file(PENDING_ACTIVITIES_FILE)
            updated_pending = [line for line in pending_activities if line.strip() != activity_line.strip()]
            self.write_file(PENDING_ACTIVITIES_FILE, updated_pending)

            # Add to archive
            archive_activities = self.load_file(ACTIVITY_ARCHIVE_FILE)
            archive_activities.append(activity_line)
            self.write_file(ACTIVITY_ARCHIVE_FILE, archive_activities)

            # Notify and update the UI
            create_notification(self.master, f"✅ '{activity['activity']}' marked as completed!", COLOR_SUCCESS)
            self.update_activity_list()

        except Exception as e:
            create_notification(self.master, f"❌ Error completing activity: {e}", COLOR_ERROR)