class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if not self.root:
            self.root = Node(data)
        else:
            self._insert(self.root, data)

    def _insert(self, current, data):
        if data["date"] < current.data["date"]:
            if current.left:
                self._insert(current.left, data)
            else:
                current.left = Node(data)
        else:
            if current.right:
                self._insert(current.right, data)
            else:
                current.right = Node(data)
    
    def search(self, query):
        """Search for all nodes matching the query."""
        result = []
        self._search(self.root, query.lower(), result)
        return result

    def _search(self, current, query, result):
        if current:
            # Check if any field matches the query
            if query in current.data["activity"].lower() or query in current.data["pet_name"].lower() or query in current.data["date"].lower():
                result.append(current.data)
            self._search(current.left, query, result)
            self._search(current.right, query, result)


    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, current, result):
        if current:
            self._inorder_traversal(current.left, result)
            result.append(current.data)
            self._inorder_traversal(current.right, result)

    def search(self, query):
        """Search for all nodes matching the query."""
        result = []
        self._search(self.root, query.lower(), result)
        return result

    def _search(self, current, query, result):
        if current:
            # Add node to results if any field matches the query
            if query in current.data["activity"].lower() or query in current.data["pet_name"].lower() or query in current.data["date"].lower():
                result.append(current.data)
            self._search(current.left, query, result)
            self._search(current.right, query, result)

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