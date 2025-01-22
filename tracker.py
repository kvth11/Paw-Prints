# tracker.py

from logic.models import PetList, ActivityQueue, ActivityStack

class PawPrints:
    """Manages the core functionality of the PawPrints application."""

    def __init__(self):
        # Initialize the PawPrints application with pet list, activity queue, and stack
        self.pets = PetList()
        self.activity_queue = ActivityQueue()
        self.activity_stack = ActivityStack()

    def add_pet(self, name, years, months, species, owner_name):
        #Add a new pet to the pet list.
        self.pets.add_pet(name, years, months, species, owner_name)

    def schedule_activity(self, activity, pet_name, date):
        #Schedule a new activity for a pet.
        self.activity_queue.add_activity(activity, pet_name, date)

    def complete_activity(self, activity):
        #Mark an activity as completed and record it in the history.
        self.activity_queue.complete_activity(activity)
        self.activity_stack.complete_activity(activity)

    def delete_activity(self, activity):
        #Delete an activity from the activity queue.
        self.activity_queue.delete_activity(activity)

    def display_pets(self):
        #Display all pets in the pet list.
        return self.pets.display_pets()

    def get_pending_activities(self):
        #Retrieve all pending activities from the activity queue.
        return self.activity_queue.get_pending_activities()

    def get_completed_activities(self):
        #Retrieve the history of completed activities.
        return self.activity_stack.view_history()