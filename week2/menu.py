from my_todolists.entities import TodoList, Task
from my_todolists.front import Printers
from my_todolists.user_inputs import UserMainInput, UserTaskInput


def user_interface() -> None:
    """Main menu."""

    Printers().print_welcome()

    Printers().print_menu()

    CREATE_NEW_LIST = 1
    ADD_NEW_TASK = 2
    LIST_OPTIONS = 3
    OBTAIN_OPTIONS = 4
    MODIFY_TASK = 5
    DELETE_TASK = 6
    SEARCH_OPTIONS = 7
    EXIT = 8

    ask = True
    while ask:
        try:
            choice = UserMainInput().choice_main_menu()
            if choice == CREATE_NEW_LIST:
                TodoList().create_list()
                Printers().print_list_created()
                Printers().print_print_saved_lists()
                Printers().print_menu()
            elif choice == ADD_NEW_TASK:
                title, description, tags = UserTaskInput().new_task_params()
                id_task = TodoList().add_task_to_list(title, description, tags)
                Printers().print_task_created()
                Printers().tasks_printer(id_task, title, description, tags)
                Printers().print_menu()
            elif choice == LIST_OPTIONS:
                list_submenu()
            elif choice == OBTAIN_OPTIONS:
                obtain_submenu()
            elif choice == MODIFY_TASK:
                Printers().print_saved_lists()
                list_choice = UserMainInput().choice_list_to_show()
                try:
                    show_list(list_choice)
                except TypeError:
                    Printers().print_invalid_id()
                    break
                task_mod_choice = UserMainInput().choice_task_to_show()
                try:
                    modify_task(task_mod_choice, list_choice)
                except TypeError:
                    Printers().print_invalid_id()
                Printers().print_menu()
            elif choice == DELETE_TASK:
                Printers().print_saved_lists()
                list_choice = UserMainInput().choice_list_to_show()
                try:
                    show_list(list_choice)
                except TypeError:
                    Printers().print_invalid_id()
                    break
                task_del_choice = UserMainInput().choice_task_to_show()
                if not Task().delete_task(list_choice, task_del_choice):
                    Printers().print_invalid_id()
                Printers().print_deleted_task(task_del_choice)
                Printers().print_menu()
            elif choice == SEARCH_OPTIONS:
                search_submenu()
            elif choice == EXIT:
                ask = False
        except ValueError:
            Printers().print_error_choice()
            Printers().print_menu()


def list_submenu() -> None:
    """User choice from List:"""

    LIST_CURRENT_TASKS = 1
    LIST_TASK_ON_LIST = 2
    LIST_ALL_TODO_LISTS = 3

    Printers().print_list_submenu()

    choice_list_submenu = UserMainInput().choice_main_menu()

    if choice_list_submenu == LIST_CURRENT_TASKS:
        for id_task, title, description, tag in TodoList().current_tasks():
            Printers().print_task(
                id_task, title, description, tag
            )
        Printers().print_menu()
    elif choice_list_submenu == LIST_TASK_ON_LIST:
        Printers().print_saved_lists()
        list_choice = UserMainInput().choice_list_to_show()
        for id_task, title, description, tag in TodoList().tasks_on_list(
            list_choice
        ):
            Printers().print_task(
                id_task, title, description, tag
            )
        Printers().print_menu()
    elif choice_list_submenu == LIST_ALL_TODO_LISTS:
        for id_list, task, title, description, tags in TodoList(
        ).show_all_lists():
            Printers().print_list(id_list)
            Printers().print_task(task, title, description, tags)
        Printers().print_menu()
    else:
        Printers().print_error_choice()
        Printers().print_menu()


def obtain_submenu() -> None:
    """User choice from Obtain:"""

    Printers().print_obtain_submenu()

    OBTAIN_TASK_BY_ID = 1
    OBTAIN_LIST_BY_ID = 2

    choice_obtain_submenu = UserMainInput().choice_main_menu()

    if choice_obtain_submenu == OBTAIN_TASK_BY_ID:
        id_task_choice = UserMainInput().choice_task_to_show()
        for id_list, task, title, description, tags in Task(
        ).search_task_id(id_task_choice):
            Printers().print_list(id_list)
            Printers().print_task(task, title, description, tags)
        Printers().print_menu()
    elif choice_obtain_submenu == OBTAIN_LIST_BY_ID:
        Printers().print_saved_lists()
        id_list_choice = UserMainInput().choice_list_to_show()
        for task, title, description, tags in TodoList(
        ).search_list_id(id_list_choice):
            Printers().print_task(task, title, description, tags)
        Printers().print_menu()
    else:
        Printers().print_error_choice()
        Printers().print_menu()


def show_list(list_choice):
    for id_task, title, description, tag in TodoList(
    ).tasks_on_list(list_choice):
        Printers().print_task(
            id_task, title, description, tag
        )
    return list_choice


def modify_task(task_mod_choice, list_mod_choice):
    id_task, title, description, tags = Task().modify_task(
        list_mod_choice, task_mod_choice,
    )
    Printers().print_modified_task(id_task)
    Printers().print_task(id_task, title, description, tags)


def search_submenu() -> None:
    """User choice from Search:"""

    Printers().print_search_submenu()

    SEARCH_TASK_BY_TITLE = 1
    SEARCH_TASK_BY_DESCRIPTION = 2

    choice_search_submenu = UserMainInput().choice_main_menu()

    if choice_search_submenu == SEARCH_TASK_BY_TITLE:
        task_title_search = UserMainInput().choice_task_title()
        for id_list, task, title, description, tags in Task(
        ).search_task(1, task_title_search):
            Printers().print_list(id_list)
            Printers().print_task(task, title, description, tags)
        else:
            Printers().print_no_search_result()
        Printers().print_menu()
    elif choice_search_submenu == SEARCH_TASK_BY_DESCRIPTION:
        task_desc_search = UserMainInput().choice_task_description()
        for id_list, task, title, description, tags in Task(
        ).search_task(2, task_desc_search):
            Printers().print_list(id_list)
            Printers().print_task(task, title, description, tags)
        else:
            Printers().print_no_search_result()
        Printers().print_menu()
    else:
        Printers().print_error_choice()
        Printers().print_menu()
