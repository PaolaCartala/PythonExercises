from mytodolists.front import Printers
from mytodolists.user_inputs import UserMainInput
from mytodolists.custom_exceptions import (
    TableDoesntExistError, DatabaseNotConnectedError
)
from user_interface import UserInterfaceManager
from constants import MainOptions


class UserMenu:

    @staticmethod
    def menu_handler() -> None:
        """Main menu."""

        Printers.print_welcome()

        functions = {
            MainOptions.CREATE_NEW_LIST.value:
                UserInterfaceManager().create_new_list,
            MainOptions.ADD_NEW_TASK.value:
                UserInterfaceManager().add_new_task,
            MainOptions.LIST_OPTIONS.value:
                UserInterfaceManager().list_submenu,
            MainOptions.OBTAIN_OPTIONS.value:
                UserInterfaceManager().obtain_submenu,
            MainOptions.MODIFY_TASK.value: UserInterfaceManager().modify_task,
            MainOptions.DELETE_TASK.value: UserInterfaceManager().delete_task,
            MainOptions.SEARCH_OPTIONS.value:
                UserInterfaceManager().search_submenu,
            MainOptions.SORT_GROUP_TASKS.value:
                UserInterfaceManager().sortgroup_submenu
        }

        ask = True
        while ask:
            Printers.print_menu()
            choice = UserMainInput().choice_main_menu()
            if choice == MainOptions.EXIT.value:
                ask = False
                break
            try:
                functions[choice]()
            except (KeyError, ValueError):
                Printers.print_error_choice()
            except (DatabaseNotConnectedError, TableDoesntExistError):
                Printers.print_critical()
                ask = False


if __name__ == '__main__':
    UserMenu.menu_handler()
