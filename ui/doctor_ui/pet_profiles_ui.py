from customtkinter import *
from ui.doctor_ui.utils.constants import *
from ui.doctor_ui.utils.utils import *
from ui.doctor_ui.main_ui import *
from data_structures.pet_profiles_ds import *


class PetProfilesUI:
    def __init__(self, master, tab_frame, clear_tab_frame):
        self.master = master
        self.tab_frame = tab_frame
        self.clear_tab_frame = clear_tab_frame
        self.default_pet_profiles = []  # Store the default view data

    def pet_profiles_ui(self):
        self.clear_tab_frame()

        CTkLabel(
            self.tab_frame,
            text="Pet Profiles",
            font=FONT_LARGE,
            text_color="#f1ca75",
            fg_color=COLOR_MAIN_BG
        ).place(x=200, y=20)

        # Sorting Buttons
        CTkButton(
            self.tab_frame,
            text="Sort by Pet Name",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=self.sort_by_pet_name,
            width=200,
            height=50
        ).place(x=200, y=750)

        CTkButton(
            self.tab_frame,
            text="Sort by Species",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=self.sort_by_species,
            width=200,
            height=50
        ).place(x=470, y=750)

        CTkButton(
            self.tab_frame,
            text="Sort by Owner Name",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=self.sort_by_owner_name,
            width=200,
            height=50
        ).place(x=740, y=750)

        # Search Bar and Button
        search_entry = CTkEntry(
            self.tab_frame,
            placeholder_text="Search...",
            font=FONT_SMALL,
            width=350,
            height=40
        )
        search_entry.place(x=200, y=90)

        search_criteria = StringVar(value="Name")
        CTkOptionMenu(
            self.tab_frame,
            variable=search_criteria,
            values=["Name", "Species", "Owner"],
            text_color=COLOR_TEXT_PRIMARY,
            font=FONT_SMALL,
            fg_color="#bfecff",
            button_color="#bfecff",
            button_hover_color="#ffe9b9",
            height=40
        ).place(x=580, y=90)

        CTkButton(
            self.tab_frame,
            text="Search",
            text_color="#667075",
            font=FONT_PRIMARY,
            fg_color="#bfecff",
            hover_color="#ffe9b9",
            command=lambda: self.search_pet_profiles(search_entry.get(), search_criteria.get()),
            width=200,
            height=40
        ).place(x=750, y=90)

        # Profile List Display
        self.pet_profiles_frame = CTkFrame(
            self.tab_frame, corner_radius=10, width=900, height=600, fg_color=COLOR_MAIN_BG
        )
        self.pet_profiles_frame.place(x=200, y=150)

        headers = ["Pet Name", "Age", "Species", "Owner Name"]
        for i, header in enumerate(headers):
            CTkLabel(
                self.pet_profiles_frame,
                text=header,
                width=200,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=5, pady=10, sticky="w")

        self.load_default_pet_profiles()

    def load_default_pet_profiles(self):
        """Load the default view of pet profiles."""
        self.default_pet_profiles = load_file_lines(PET_PROFILES_FILE)
        self.load_pet_profiles(self.default_pet_profiles)

    def load_pet_profiles(self, pets):
        """Load given pet profiles into the table."""
        # Clear the current display
        for widget in self.pet_profiles_frame.winfo_children():
            widget.destroy()

        # Reload headers
        headers = ["Pet Name", "Age", "Species", "Owner Name"]
        for i, header in enumerate(headers):
            CTkLabel(
                self.pet_profiles_frame,
                text=header,
                width=200,
                anchor="w",
                font=FONT_PRIMARY,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=0, column=i, padx=5, pady=10, sticky="w")

        # Add pets to the display
        for i, pet in enumerate(pets, start=1):
            details = pet.strip().split("\t")
            for j, detail in enumerate(details):
                CTkLabel(
                    self.pet_profiles_frame,
                    text=detail,
                    width=200,
                    anchor="w",
                    font=FONT_MEDIUM,
                    text_color=COLOR_TEXT_PRIMARY,
                    fg_color=COLOR_MAIN_BG
                ).grid(row=i, column=j, padx=5, pady=5, sticky="w")

    def sort_by_pet_name(self):
        """Sort the pet profiles by name."""
        sorted_pets = sorted(self.default_pet_profiles, key=lambda pet: pet.split("\t")[0])
        self.load_pet_profiles(sorted_pets)
        create_notification(self.master, "✅ Pet profiles sorted by name.", COLOR_SUCCESS)

    def sort_by_species(self):
        """Sort the pet profiles by species."""
        sorted_pets = sorted(self.default_pet_profiles, key=lambda pet: pet.split("\t")[2])
        self.load_pet_profiles(sorted_pets)
        create_notification(self.master, "✅ Pet profiles sorted by species.", COLOR_SUCCESS)

    def sort_by_owner_name(self):
        """Sort the pet profiles by owner name."""
        sorted_pets = sorted(self.default_pet_profiles, key=lambda pet: pet.split("\t")[3])
        self.load_pet_profiles(sorted_pets)
        create_notification(self.master, "✅ Pet profiles sorted by owner name.", COLOR_SUCCESS)

    def search_pet_profiles(self, query, criteria):
        """Search pet profiles using linear search."""
        column_map = {"Name": 0, "Species": 2, "Owner": 3}
        column = column_map.get(criteria)

        results = [pet for pet in self.default_pet_profiles if query.lower() in pet.split("\t")[column].lower()]
        self.load_pet_profiles(results)

        if not results:
            CTkLabel(
                self.pet_profiles_frame,
                text="No results found.",
                font=FONT_MEDIUM,
                text_color=COLOR_TEXT_PRIMARY,
                fg_color=COLOR_MAIN_BG
            ).grid(row=1, column=0, columnspan=4, pady=20)