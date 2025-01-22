from tkinter import Tk
from ui.role_selection_ui.main_ui import RoleSelectionUI

def main():
    """Initialize and run the main application."""
    root = Tk()
    RoleSelectionUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()