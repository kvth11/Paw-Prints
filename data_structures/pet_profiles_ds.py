# Bubble Sort Implementation
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array

# Selection Sort Implementation
def selection_sort(array):
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
    return array

# Linked List Implementation
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def get_all_data(self):
        current = self.head
        data_list = []
        while current:
            data_list.append(current.data)
            current = current.next
        return data_list
    
    # Binary Search Implementation
def binary_search(pets, query, column):
    """Binary search implementation."""
    low, high = 0, len(pets) - 1
    query = query.lower()

    while low <= high:
        mid = (low + high) // 2
        value = pets[mid].split("\t")[column].lower()

        if value == query:
            return [pets[mid]]
        elif value < query:
            low = mid + 1
        else:
            high = mid - 1

    return []

# Sorting Implementation
def sort_pet_profiles(pets, column):
    """Sort pet profiles by a specific column."""
    return sorted(pets, key=lambda pet: pet.split("\t")[column])

# Load and Write Utilities
def load_file_lines(filepath):
    """Load lines from a file."""
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_file(filepath, lines):
    """Write lines to a file."""
    try:
        with open(filepath, "w") as file:
            file.writelines(lines)
    except Exception as e:
        raise IOError(f"Could not write to file {filepath}: {e}")
    
# Linear Search Implementation
def linear_search(pets, query, column):
    """Linear search implementation to find all matches."""
    return [pet for pet in pets if query.lower() in pet.split("\t")[column].lower()]