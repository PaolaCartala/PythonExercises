import logging

from mytodolists.handlers import TodoListHandler, TaskHandler
from mytodolists.data_access import OldListsManager
from mytodolists.front import Printers
from mytodolists.user_inputs import UserMainInput, UserListInput, UserTaskInput


logger = logging.getLogger(__name__)
FORMAT = "\n%(levelname)s: %(message)s\n"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class UserInterfaceManager:

    @staticmethod
    def create_new_list():
        title = UserListInput.new_list_params()
        logging.debug('Title recorded')
        TodoListHandler.create_list(title)
        logging.debug('New list created')

    @staticmethod
    def add_new_task():
        if OldListsManager.count_old_lists() != 0:
            id_list = UserMainInput.choice_list_to_show()
            search = TodoListHandler.search_list_id(id_list)
            while not search and search != {}:
                logging.error('! Please insert a valid ID (number)')
                id_list = UserMainInput.choice_list_to_show()
                search = TodoListHandler.search_list_id(id_list)
        elif OldListsManager.count_old_lists() == 0:
            logging.info('No lists available, creating..')
            title = UserListInput.new_list_params()
            id_list = TodoListHandler.create_list(title)[0]
        logging.debug('List available')
        task_title, task_description, tags = UserTaskInput(
        ).new_task_params()
        logging.debug('Parameters inserted')
        id_task, title, description, tags = TodoListHandler.add_task_to_list(
            id_list, task_title, task_description, tags
        )
        logging.info('Task created')
        return id_task, title, description, tags

    @staticmethod
    def list_submenu() -> None:
        """User choice from List:"""

        LIST_CURRENT_TASKS = 1
        LIST_TASK_ON_LIST = 2
        LIST_ALL_TODO_LISTS = 3

        choice_list_submenu = UserMainInput.choice_main_menu()

        if choice_list_submenu == LIST_CURRENT_TASKS:
            logging.debug('Printing current tasks')
            for id_task, title, description, tag in TodoListHandler(
            ).current_tasks():
                Printers.print_task(
                    id_task, title, description, tag
                )
        elif choice_list_submenu == LIST_TASK_ON_LIST:
            Printers.print_saved_lists()
            list_choice = UserMainInput.choice_list_to_show()
            logging.debug('Printing tasks on list')
            for id_task, title, description, tag in TodoListHandler(
            ).current_tasks(
                list_choice
            ):
                Printers.print_task(
                    id_task, title, description, tag
                )
        elif choice_list_submenu == LIST_ALL_TODO_LISTS:
            logging.debug('Printing all list')
            for id_list, task, title, description, tags in TodoListHandler(
            ).show_all_lists():
                logging.info(f'List # {id_list}')
                Printers.print_task(task, title, description, tags)
        else:
            logging.error('! Please insert a valid ID (number)')

    @staticmethod
    def obtain_submenu() -> None:
        """User choice from Obtain:"""

        OBTAIN_TASK_BY_ID = 1
        OBTAIN_LIST_BY_ID = 2

        choice_obtain_submenu = UserMainInput.choice_main_menu()

        if choice_obtain_submenu == OBTAIN_TASK_BY_ID:
            id_task_choice = UserMainInput.choice_task_to_show()
            for id_list, task, title, description, tags in TaskHandler(
            ).search_task_id(id_task_choice):
                logging.info(f'List # {id_list}')
                Printers.print_task(task, title, description, tags)
        elif choice_obtain_submenu == OBTAIN_LIST_BY_ID:
            Printers.print_saved_lists()
            id_list_choice = UserMainInput.choice_list_to_show()
            if not TodoListHandler.search_list_id(id_list_choice):
                logging.error('! Please select a choice from the list')
            for task, title, description, tags in TodoListHandler(
            ).current_tasks(id_list_choice):
                Printers.print_task(task, title, description, tags)
        else:
            logging.error('! Please insert a valid ID (number)')

    @classmethod
    def show_list(cls, list_choice):
        for id_task, title, description, tag in list(TodoListHandler(
        ).current_tasks(list_choice)):
            Printers.print_task(
                id_task, title, description, tag
            )
        return list_choice

    @classmethod
    def modify_task(cls):
        list_choice = UserMainInput.choice_list_to_show()
        cls.show_list(list_choice)
        task_mod_choice = UserMainInput.choice_task_to_show()
        try:
            title, description, tags = UserTaskInput(
            ).new_task_params()
            id_task, title, description, tags = TaskHandler().modify_task(
                list_choice, task_mod_choice, title, description, tags
            )
            logging.info(f'Task # {id_task} successfully modified!')
            Printers.print_task(id_task, title, description, tags)
        except TypeError:
            logging.error('! Please insert a valid ID (number)')
            return False

    @classmethod
    def delete_task(cls):
        list_choice = UserMainInput.choice_list_to_show()
        cls.show_list(list_choice)
        task_del_choice = UserMainInput.choice_task_to_show()
        if not TaskHandler().delete_task(list_choice, task_del_choice):
            logging.error('! Please insert a valid ID (number)')
            return False
        logging.info(f'Task # {task_del_choice} succesfuly deleted!')

    @staticmethod
    def search_submenu() -> None:
        """User choice from Search:"""

        SEARCH_TASK_BY_TITLE = 1
        SEARCH_TASK_BY_DESCRIPTION = 2

        choice_search_submenu = UserMainInput.choice_main_menu()

        if choice_search_submenu == SEARCH_TASK_BY_TITLE:
            task_title_search = UserMainInput.choice_task_title()
            try:
                search = list(TaskHandler.search_task(1, task_title_search))
                for id_list, task, title, description, tags in search:
                    logging.info(f'List # {id_list}')
                    Printers.print_task(task, title, description, tags)
            except TypeError:
                logging.error('Search result\nNo results')
        elif choice_search_submenu == SEARCH_TASK_BY_DESCRIPTION:
            task_desc_search = UserMainInput.choice_task_description()
            try:
                search = list(TaskHandler(
                ).search_task(2, task_desc_search))
                for id_list, task, title, description, tags in search:
                    logging.info(f'List # {id_list}')
                    Printers.print_task(task, title, description, tags)
            except TypeError:
                logging.error('Search result\nNo results')
        else:
            logging.error('! Please insert a valid ID (number)')
