from customtkinter import *
from datetime import datetime
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from data_structures.schedule_ds import *

class ScheduleUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame

    def schedule_ui(self):
        self.clear_tab_frame()

        # Add Title
        CTkLabel(
            self.tab_frame,
            text="Schedule Overview",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=20)

        # Search Bar and Buttons
        search_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Search by Pet Name...",
            font=FONT_SMALL,
            width=350,
            height=40
        )
        search_entry.place(x=200, y=90)

        CTkButton(
            self.tab_frame,
            text="Search",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=lambda: self.search_schedule(search_entry.get()),
            width=150,
            height=40
        ).place(x=570, y=90)

        CTkButton(
            self.tab_frame,
            text="Clear",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#ffbfca",
            hover_color="#ff8b9e",
            command=self.load_schedule,
            width=150,
            height=40
        ).place(x=730, y=90)

        # Main Content Area
        self.schedule_overview_frame = CTkFrame(
            self.tab_frame,
            corner_radius=10,
            width=900,
            height=600,
            fg_color=COLOR_MAIN_BG
        )
        self.schedule_overview_frame.place(x=200, y=150)

        headers = ["Schedule", "Pet Name", "Activity"]
        for i, header in enumerate(headers):
            CTkLabel(
                self.schedule_overview_frame,
                text=header,
                width=180,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=5, pady=15, sticky="w")

        self.load_schedule()

    def load_schedule(self):
        """Load all schedule data and display it."""
        all_activities = []

        # Load pending activities
        for line in load_file_lines(PENDING_ACTIVITIES_FILE):
            try:
                activity, pet_name, date = line.strip().split(",")[:3]
                all_activities.append({"activity": activity, "pet_name": pet_name, "date": date})
            except ValueError:
                print(f"Skipping malformed entry in schedule: {line.strip()}")

        # Insert all activities into a binary tree
        self.schedule_tree = BinaryTree()
        for activity in all_activities:
            self.schedule_tree.insert(activity)

        self.display_activities(self.schedule_tree.inorder_traversal())

    def display_activities(self, activities):
        """Display the given activities in the UI."""
        # Clear current frame
        for widget in self.schedule_overview_frame.winfo_children():
            widget.destroy()

        headers = ["Schedule", "Pet Name", "Activity"]
        for i, header in enumerate(headers):
            CTkLabel(
                self.schedule_overview_frame,
                text=header,
                width=180,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=5, pady=15, sticky="w")

        # Display sorted activities
        for i, activity in enumerate(activities, start=1):
            CTkLabel(
                self.schedule_overview_frame,
                text=activity["date"],
                width=150,
                anchor="w",
                font=FONT_MEDIUM,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=i, column=0, padx=10, pady=10, sticky="w")

            CTkLabel(
                self.schedule_overview_frame,
                text=activity["pet_name"],
                width=150,
                anchor="w",
                font=FONT_MEDIUM,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=i, column=1, padx=10, pady=10, sticky="w")

            CTkLabel(
                self.schedule_overview_frame,
                text=activity["activity"],
                width=150,
                anchor="w",
                font=FONT_MEDIUM,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=i, column=2, padx=10, pady=10, sticky="w")

    def remove_completed_activity(self, completed_activity):
        """Remove an activity from the schedule when marked as done."""
        try:
            # Load approved appointments
            approved_activities = load_file_lines(APPROVED_APPOINTMENTS_FILE)

            # Remove the completed activity
            updated_activities = [
                line for line in approved_activities
                if not line.startswith(f"{completed_activity['activity']},{completed_activity['pet_name']},{completed_activity['date']}")
            ]
            write_to_file(APPROVED_APPOINTMENTS_FILE, updated_activities)

            # Reload the schedule to reflect the removal
            self.load_schedule()
        except Exception as e:
            print(f"Error removing completed activity: {e}")

    def search_schedule(self, query):
        """Search for a specific pet name in the schedule."""
        if not query.strip():
            self.load_schedule()  # Load all schedules if the query is empty
            return

        results = self.schedule_tree.search(query)
        if results:
            self.display_activities(results)
        else:
            # Display 'No results found' if no matches
            for widget in self.schedule_overview_frame.winfo_children():
                widget.destroy()

            CTkLabel(
                self.schedule_overview_frame,
                text="No results found.",
                font=FONT_MEDIUM,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=1, column=0, columnspan=3, pady=20)

        