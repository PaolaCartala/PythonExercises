from mytodolists.front import Printers
from mytodolists.user_inputs import UserMainInput
from user_interface import UserInterfaceManager


def user_menu() -> None:
    """Main menu."""

    Printers().print_welcome()

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
            Printers().print_menu()
            choice = UserMainInput().choice_main_menu()
            if choice == CREATE_NEW_LIST:
                UserInterfaceManager().create_new_list()
                Printers().print_list_created()
                Printers().print_saved_lists()
            elif choice == ADD_NEW_TASK:
                Printers().print_saved_lists()
                id_task, title, description, tags = UserInterfaceManager(
                ).add_new_task()
                Printers().print_task(id_task, title, description, tags)
            elif choice == LIST_OPTIONS:
                Printers().print_list_submenu()
                UserInterfaceManager().list_submenu()
            elif choice == OBTAIN_OPTIONS:
                Printers().print_obtain_submenu()
                UserInterfaceManager().obtain_submenu()
            elif choice == MODIFY_TASK:
                Printers().print_saved_lists()
                UserInterfaceManager().modify_task()
            elif choice == DELETE_TASK:
                Printers().print_saved_lists()
                UserInterfaceManager().delete_task()
            elif choice == SEARCH_OPTIONS:
                Printers().print_search_submenu()
                UserInterfaceManager().search_submenu()
            elif choice == EXIT:
                ask = False
        except ValueError:
            Printers().print_error_choice()


if __name__ == '__main__':
    user_menu()
