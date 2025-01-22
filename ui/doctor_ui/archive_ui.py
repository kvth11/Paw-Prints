from customtkinter import *
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.main_ui import *

class ArchiveUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame
    
    def archive_ui(self):
        self.clear_tab_frame()

        self.tab_frame.update_idletasks()
        self.tab_frame.configure(fg_color=COLOR_MAIN_BG)
        tab_width = self.tab_frame.winfo_width()
        tab_height = self.tab_frame.winfo_height()

        frame_width = 900
        frame_height = 700
        frame_x = 200
        frame_y = (tab_height - frame_height) // 2 + 20

        CTkLabel(
            self.tab_frame,
            text="Activity Archive",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=frame_x, y=frame_y - 80 + 20)

        self.activity_archive_frame = CTkFrame(
            self.tab_frame,
            corner_radius=10,
            width=frame_width,
            height=frame_height,
            fg_color=COLOR_MAIN_BG
        )
        self.activity_archive_frame.place(x=frame_x, y=frame_y)

        headers = ["Activity", "Pet Name", "Schedule", "Actions"]
        for i, header in enumerate(headers):
            CTkLabel(
                self.activity_archive_frame,
                text=header,
                width=150,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=5, pady=15, sticky="w")

        completed_activities = [
            {
                "activity": line.split(",")[0],
                "pet_name": line.split(",")[1],
                "date": line.split(",")[2].strip(),
            }
            for line in load_file_lines(ACTIVITY_ARCHIVE_FILE)
        ]

        if not completed_activities:
            CTkLabel(
                self.activity_archive_frame,
                text="No completed activities found.",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=2, column=0, columnspan=len(headers), padx=3, pady=20)
        else:
            for i, activity in enumerate(completed_activities, start=2):
                CTkLabel(
                    self.activity_archive_frame,
                    text=activity["activity"],
                    width=150,
                    anchor="w",
                    font=FONT_MEDIUM,
                    text_color=COLOR_TEXT_PRIMARY,
                    fg_color=COLOR_MAIN_BG
                ).grid(row=i, column=0, padx=20, pady=10, sticky="w")

                CTkLabel(
                    self.activity_archive_frame,
                    text=activity["pet_name"],
                    width=150,
                    anchor="w",
                    font=FONT_MEDIUM,
                    text_color=COLOR_TEXT_PRIMARY,
                    fg_color=COLOR_MAIN_BG
                ).grid(row=i, column=1, padx=20, pady=10, sticky="w")

                CTkLabel(
                    self.activity_archive_frame,
                    text=activity["date"],
                    width=150,
                    anchor="w",
                    font=FONT_MEDIUM,
                    text_color=COLOR_TEXT_PRIMARY,
                    fg_color=COLOR_MAIN_BG
                ).grid(row=i, column=2, padx=10, pady=10, sticky="w")

                CTkButton(
                    self.activity_archive_frame,
                    text="Delete",
                    font=FONT_MEDIUM,
                    text_color="white",
                    fg_color=COLOR_ERROR,
                    hover_color="#d08080",
                    command=lambda act=activity: self.confirm_delete_activity(act),
                ).grid(row=i, column=3, padx=10, pady=10, sticky="w")

    def confirm_delete_activity(self, activity):
        confirm_popup = CTkToplevel(self.master)
        confirm_popup.title("Confirm Delete")

        self.master.update_idletasks()
        popup_width = 500
        popup_height = 150
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()

        x_offset = master_x + (master_width - popup_width) // 2
        y_offset = master_y + (master_height - popup_height) // 2

        confirm_popup.geometry(f"{popup_width}x{popup_height}+{x_offset}+{y_offset}")
        confirm_popup.transient(self.master)
        confirm_popup.grab_set()
        confirm_popup.configure(bg=COLOR_MAIN_BG)

        CTkLabel(
            confirm_popup,
            text="Are you sure you want to delete this activity?",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            anchor="center",
        ).pack(pady=20)

        button_frame = CTkFrame(confirm_popup, corner_radius=10, fg_color="#ebebeb")
        button_frame.pack(pady=10)

        CTkButton(
            button_frame,
            text="Yes",
            font=FONT_MEDIUM,
            text_color="white",
            fg_color=COLOR_SUCCESS,
            hover_color="#88c070",
            command=lambda: [
                self.delete_completed_activity(activity),
                confirm_popup.destroy()
            ],
        ).pack(side="left", padx=20)

        CTkButton(
            button_frame,
            text="No",
            font=FONT_MEDIUM,
            text_color="white",
            fg_color=COLOR_ERROR,
            hover_color="#d08080",
            command=confirm_popup.destroy,
        ).pack(side="right", padx=20)

    def delete_completed_activity(self, activity):
        try:
            # Load all activities from the archive file
            activities = load_file_lines(ACTIVITY_ARCHIVE_FILE)

            # Construct the exact line to delete
            activity_to_delete = f"{activity['activity']},{activity['pet_name']},{activity['date']}".strip()

            # Filter out the activity to delete
            updated_activities = [
                line for line in activities if line.strip() != activity_to_delete
            ]

            # If no lines were removed, the activity wasn't found
            if len(updated_activities) == len(activities):
                create_notification(self.master, "❌ Activity not found.", COLOR_ERROR)
                return

            # Write the updated activities back to the file
            write_to_file(ACTIVITY_ARCHIVE_FILE, "".join(updated_activities), mode="w")

            # Refresh the archive UI
            self.archive_ui()

            # Notify the user
            create_notification(self.master, "✅ Activity deleted successfully.", COLOR_SUCCESS)
        except Exception as e:
            create_notification(self.master, f"❌ Error deleting activity: {e}", COLOR_ERROR)