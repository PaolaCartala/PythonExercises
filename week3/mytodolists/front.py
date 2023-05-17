import os


class Printers:

    @staticmethod
    def print_welcome() -> None:
        print("\nWelcome to your To-Do Lists!\n----------------------------\n")

    @staticmethod
    def print_menu() -> None:
        """Print the main menu."""
        print(r"          Menu")
        print('------------------------')
        print("1) Create a new empty todo list")
        print("2) Add a new task to the list")
        print("3) List:")
        print("4) Obtain:")
        print("5) Modify a specific task by id")
        print("6) Delete a specific task")
        print("7) Search:")
        print("8) Exit\n")

    @staticmethod
    def print_list_created() -> None:
        print("\nTo-Do list created!\n")

    @staticmethod
    def print_saved_lists() -> None:
        """Print the saved lists."""
        print('\nAvailable lists:')
        folder = sorted(os.listdir('lists/'))
        for file in folder:
            i = file.index('_')
            print(f"# {file[:i]} {file[i + 1:-5]}")
        print('------------------------\n')

    @staticmethod
    def print_task(
        id_task: str, title: str, description: str, tags: list
    ) -> None:
        """Print a task."""
        print(f'\nTask: # {id_task}')
        print(f'Title: {title}')
        print(f'Description: {description}')
        print('Tags:')
        for tag in tags:
            print(f'{tag:>10}')
        print('------------------------')

    @staticmethod
    def print_list_submenu() -> None:
        """Submenu List:"""
        print("\n1) List current tasks")
        print("2) List tasks on a list")
        print("3) List all To-Do lists")

    @staticmethod
    def print_obtain_submenu() -> None:
        """Subenu Obtain:"""
        print("\n1) Obtain a specific task by id")
        print("2) Obtain a specific list by id")

    @staticmethod
    def print_search_submenu() -> None:
        """Subenu Search:"""
        print("\n1) Search for a task by its title")
        print("2) Search for a task by its content")

    @staticmethod
    def print_error_choice() -> None:
        print("\n! Please select a choice from the list\n")
