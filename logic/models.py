class PetNode:
    """Node representing a single pet."""

    def __init__(self, name, years, months, species, owner_name):
        self.name = name
        self.years = years
        self.months = months
        self.species = species
        self.owner_name = owner_name
        self.next = None

class PetList:
    #Linked list to manage pet profiles.

    def __init__(self):
        self.head = None

    def add_pet(self, name, years, months, species, owner_name):
        #Add a new pet to the list.#
        new_pet = PetNode(name, years, months, species, owner_name)
        if not self.head:
            self.head = new_pet
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_pet

    def display_pets(self):
        #Return a list of all pets in the system.
        pets = []
        current = self.head
        while current:
            pets.append(
                f"{current.name}\t{current.years}y {current.months}m\t{current.species}\t{current.owner_name}"
            )
            current = current.next
        return pets

class ActivityQueue:
    #Queue for managing scheduled activities.

    def __init__(self):
        self.queue = []

    def add_activity(self, activity, pet_name, date):
        #Add an activity to the queue.
        self.queue.append({"activity": activity, "pet_name": pet_name, "date": date, "completed": False})

    def complete_activity(self, activity):
        #Mark an activity as completed.
        for act in self.queue:
            if act == activity:
                act["completed"] = True

    def get_pending_activities(self):
        #Return all pending activities.
        return [act for act in self.queue if not act["completed"]]

    def delete_activity(self, activity):
        #Delete an activity from the queue.
        if activity in self.queue:
            self.queue.remove(activity)

class ActivityStack:
    #Stack for managing completed activities.

    def __init__(self):
        self.stack = []

    def complete_activity(self, activity):
        #Add a completed activity to the stack.
        self.stack.append(activity)

    def view_history(self):
        #Return the history of completed activities.
        return self.stack