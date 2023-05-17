from logic import (
    new_list, add_task, current_tasks,
    tasks_on_list, show_all_lists,
    search_task_id, search_list_id, modify_task,
    delete_task, search_task_title, search_task_desc
)
from front import show_menu, printers


def app() -> None:
    """Main app."""

    print("\nWelcome to your To-Do Lists!\n--------------------------\n")

    show_menu()

    ask = True
    while ask:
        try:
            choice = int(input("Please select a choice: \n"))
            if choice == 1:
                global id_list, todo_list
                id_list, todo_list = new_list()
                print("\nToDo list created!\n")
                show_menu()
            elif choice == 2:
                title = input("\nPlease introduce a title for this task:\n")
                description = input(
                    "\nPlease introduce a description for this task:\n")
                id_task = add_task(id_list, todo_list, title, description)
                print("\nTask created!\n------------------------\n")
                printers(id_task, title, description)
                show_menu()
            elif choice == 3:
                print("\n1) List current tasks")
                print("2) List tasks on a list")
                print("3) List all To-Do lists")
                choice_3 = int(input("\nPlease select a choice: \n"))
                choice_list(choice_3)
            elif choice == 4:
                print("\n1) Obtain a specific task by id")
                print("2) Obtain a specific list by id")
                choice_4 = int(input("\nPlease select a choice: \n"))
                choice_obtain(choice_4)
            elif choice == 5:
                show_all_lists()
                task_modify_choice = input(
                    "Please choose the task to modify:\n")
                try:
                    id_task, title, description = modify_task(
                        task_modify_choice
                    )
                    print("\nTask succesfuly modified!\n")
                    printers(id_task, title, description)
                except TypeError:
                    print("\n! Please insert a valid task ID (number)\n")
                show_menu()
            elif choice == 6:
                show_all_lists()
                task_del_choice = input(
                    "\nPlease choose the task to delete:\n")
                if delete_task(task_del_choice):
                    print(f"\nTask #{task_del_choice} succesfuly deleted!")
                    print("---------------------------\n")
                else:
                    print("\n! Please insert a valid task ID (number)\n")
                show_menu()
            elif choice == 7:
                print("\n1) Search for a task by its title")
                print("2) Search for a task by its content")
                choice_7 = int(input("\nPlease select a choice: \n"))
                choice_search(choice_7)
            elif choice == 8:
                ask = False
            else:
                print("\n! Please, insert a number from the menu\n")
                show_menu()
        except ValueError:
            print("\n! Please, insert a number from the menu\n")
            show_menu()


def choice_list(choice_3: str) -> None:
    """User choice from List:

    Args:
        choice_3 (str): user's choice
    """
    if choice_3 == 1:
        print("\nCurrent tasks")
        print('------------------------\n')
        for task_id, title, description in current_tasks(id_list, todo_list):
            printers(task_id, title, description)
        show_menu()
    elif choice_3 == 2:
        list_choice = input("Please choose the list to show:\n")
        for task_id, title, description in tasks_on_list(list_choice):
            printers(task_id, title, description)
        show_menu()
    elif choice_3 == 3:
        for task_id, title, description in show_all_lists():
            printers(task_id, title, description)
        show_menu()
    else:
        print("\n! Please select a choice from the list\n")
        show_menu()


def choice_obtain(choice_4: str) -> None:
    """User choice from Obtain:

    Args:
        choice_4 (str): user's choice
    """
    if choice_4 == 1:
        id_task_choice = input(
            "\nPlease choose the task id to show:\n")
        try:
            print("\nSearch result\n------------------------")
            task_id, title, description = search_task_id(id_task_choice)
            printers(task_id, title, description)
        except TypeError:
            print("\n! Please insert a task ID (number)\n")
        show_menu()
    elif choice_4 == 2:
        id_list_choice = input("Please choose the list id to show:\n")
        for task_id, title, description in search_list_id(id_list_choice):
            printers(task_id, title, description)
        show_menu()
    else:
        print("\n! Please select a choice from the list")
        show_menu()


def choice_search(choice_7: str) -> None:
    """User choice from Search:

    Args:
        choice_7 (str): user's choice
    """
    if choice_7 == 1:
        task_title_search = input(
            "Insert the title that you want to search:\n")
        try:
            task_id, title, description = search_task_title(task_title_search)
            printers(task_id, title, description)
        except TypeError:
            print("\nSearch result")
            print('------------------------')
            print("No results\n")
        show_menu()
    elif choice_7 == 2:
        task_desc_search = input(
            "Insert the description that you want to search:\n")
        try:
            task_id, title, description = search_task_desc(task_desc_search)
            printers(task_id, title, description)
        except TypeError:
            print("\nSearch result")
            print('------------------------')
            print("No results\n")
        show_menu()
    else:
        print("\n! Please select a choice from the list")
        show_menu()


if __name__ == '__main__':
    app()
