def show_menu() -> None:
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


def available_lists(all_lists: list) -> None:
    """Print the saved lists."""
    print('\nAvailable lists:')
    for lists in all_lists:
        for list_id in lists.keys():
            print(f"# {list_id}")
    print('------------------------\n')


def printers(task_id: str, title: str, description: str) -> None:
    """Print a task."""
    print(f'Task: # {task_id}')
    print(f'Title: {title}')
    print(f'Description: {description}')
    print('------------------------\n')


def printer_lists(list_id: str) -> None:
    """Print a list."""
    print("\nSearch result")
    print('------------------------')
    print(f'List # {list_id}')
    print('------------------------')
