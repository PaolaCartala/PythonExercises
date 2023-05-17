import os


class Printers:

    def print_welcome(self):
        print("\nWelcome to your To-Do Lists!\n----------------------------\n")

    def print_menu(self) -> None:
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

    def print_list_created(self):
        print("\nTo-Do list created!\n")

    def print_task_created(self):
        print("\nTask created!\n------------------------\n")

    def print_modified_task(self, id_task: str):
        print(f"\nTask # {id_task} successfully modified!\n")

    def print_deleted_task(self, task):
        print(f"\nTask #{task} succesfuly deleted!")
        print("---------------------------\n")

    def print_saved_lists(self) -> None:
        """Print the saved lists."""
        print('\nAvailable lists:')
        folder = sorted(os.listdir('lists/'))
        for file in folder:
            print(f"# {file[:-5]}")
        print('------------------------\n')

    def print_task(
        self, id_task: str, title: str, description: str, tags: list
    ) -> None:
        """Print a task."""
        print(f'\nTask: # {id_task}')
        print(f'Title: {title}')
        print(f'Description: {description}')
        print('Tags:')
        for tag in tags:
            print(f'{tag:>10}')
        print('------------------------')

    def print_no_tasks(self):
        print("\nThe list is empty\n")

    def print_no_search_result(self) -> None:
        """Print 'no results'."""
        print("\nSearch result\n------------------------\n")
        print("No results\n")

    def print_list(self, list_id: str) -> None:
        """Print a list."""
        print("\nSearch result")
        print('------------------------')
        print(f'List # {list_id}')
        print('------------------------')

    def print_list_submenu(self) -> None:
        """Submenu List:"""
        print("\n1) List current tasks")
        print("2) List tasks on a list")
        print("3) List all To-Do lists")

    def print_obtain_submenu(self) -> None:
        """Subenu Obtain:"""
        print("\n1) Obtain a specific task by id")
        print("2) Obtain a specific list by id")

    def print_search_submenu(self) -> None:
        """Subenu Search:"""
        print("\n1) Search for a task by its title")
        print("2) Search for a task by its content")

    def print_error_choice(self):
        print("\n! Please select a choice from the list\n")

    def print_invalid_id(self):
        print("\n! Please insert a valid ID (number)\n")
