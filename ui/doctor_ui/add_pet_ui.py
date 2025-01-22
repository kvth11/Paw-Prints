from customtkinter import *
from tkcalendar import Calendar
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.main_ui import *

class AddPetUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame
        self.species_var = StringVar()  # Declare species_var as an instance attribute

    def add_pet_ui(self):
        self.clear_tab_frame()

        CTkLabel(
            self.tab_frame,
            text="Pet Profile Setup",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=40)

        CTkLabel(
            self.tab_frame,
            text="Name:",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=120)
        name_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Enter Name",
            font=FONT_MEDIUM,
            width=500,
            height=40
        )
        name_entry.place(x=200, y=160)

        CTkLabel(
            self.tab_frame,
            text="Owner Name:",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=240)
        owner_name_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Enter Owner Name",
            font=FONT_MEDIUM,
            width=500,
            height=40
        )
        owner_name_entry.place(x=200, y=280)

        CTkLabel(
            self.tab_frame,
            text="Age (Years):",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=360)
        years_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Years",
            font=FONT_MEDIUM,
            width=239,
            height=40
        )
        years_entry.place(x=200, y=400)

        CTkLabel(
            self.tab_frame,
            text="Age (Months):",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=460, y=360)
        months_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Months",
            font=FONT_MEDIUM,
            width=239,
            height=40
        )
        months_entry.place(x=460, y=400)

        CTkLabel(
            self.tab_frame,
            text="Species:",
            font=FONT_MEDIUM,
            text_color=COLOR_TEXT_PRIMARY,
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=480)

        self.species_var.set(DEFAULT_SPECIES_OPTIONS[0])  # Set default species
        CTkOptionMenu(
            self.tab_frame,
            variable=self.species_var,
            values=DEFAULT_SPECIES_OPTIONS,
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_MEDIUM,
            fg_color="#bfecff",
            button_color="#bfecff",
            button_hover_color=COLOR_BUTTON_HOVER,
            height=40
        ).place(x=200, y=520)

        CTkButton(
            self.tab_frame,
            text="Add Pet",
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color=COLOR_BUTTON_HOVER,
            command=lambda: self.add_pet(
                name_entry.get(),
                years_entry.get(),
                months_entry.get(),
                self.species_var.get(),
                owner_name_entry.get()
            ),
            width=500,
            height=50
        ).place(x=200, y=600)

    def add_pet(self, name, years, months, species, owner_name):
        try:
            if not (name and years and months and species and owner_name):
                create_notification(self.master, "❌ Please fill out all fields.", COLOR_ERROR)
                return

            try:
                years = int(years)
                months = int(months)
            except ValueError:
                create_notification(self.master, "❌ Invalid input. Age must be a number.", COLOR_ERROR)
                return

            age = f"{years} years, {months} months"
            write_to_file(PET_PROFILES_FILE, f"{name}\t{age}\t{species}\t{owner_name}\n")

            create_notification(self.master, f"✅ Pet '{name}' added successfully!", COLOR_SUCCESS)

            # Clear text fields
            for widget in self.tab_frame.winfo_children():
                if isinstance(widget, CTkEntry):
                    widget.delete(0, "end")

            # Reset species dropdown
            self.species_var.set(DEFAULT_SPECIES_OPTIONS[0])

        except Exception as e:
            create_notification(self.master, f"❌ Error: {e}", COLOR_ERROR)