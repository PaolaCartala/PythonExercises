import logging

from mytodolists.handlers import TodoListHandler, TaskHandler
from mytodolists.custom_exceptions import (
    EmptyListError, ItemNotFoundError
)
from mytodolists.db_manager import (
    SelectQueriesHandler, SortGroupQueriesHandler
)
from mytodolists.front import Printers
from mytodolists.user_inputs import (
    UserMainInput, UserListInput, UserTaskInput, UserQueriesInput
)
from constants import (
    ListOptions, ObtainOptions, SearchOptions, SortGroupOptions
)
from mytodolists.decorators import empty_not_found


logger = logging.getLogger(__name__)
FORMAT = "\n%(message)s\n"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class UserInterfaceManager:

    @staticmethod
    def create_new_list():
        title = UserListInput.new_list_params()
        logging.debug('Title recorded')
        TodoListHandler.create_list(title)
        logging.info('New list created!')
        Printers().print_saved_lists()

    @staticmethod
    def add_new_task():
        Printers().print_saved_lists()
        all_lists = SelectQueriesHandler.query_select_all_lists()
        if not all_lists:
            UserInterfaceManager.create_new_list()
        id_list = UserMainInput.choice_list_to_show()
        try:
            search = TodoListHandler.search_list_id(id_list)
        except (IndexError, ItemNotFoundError):
            logging.error('! Item not found')
            return False
        logging.debug('List available')
        task_title, task_description, tags = UserTaskInput(
        ).new_task_params()
        logging.debug('Parameters inserted')
        id_task, title, description, tags = TodoListHandler.add_task_to_list(
            search, task_title, task_description, tags
        )
        logging.info('Task created')
        Printers().print_task(id_task, title, description, tags)

    @staticmethod
    def list_submenu() -> None:
        """User choice from List:"""

        @empty_not_found
        def list_current():
            for list_id, id_task, title, desc, tag in TodoListHandler(
            ).current_tasks():
                logging.debug('Printing current tasks')
                logging.info(f'List # {list_id}')
                Printers.print_task(
                    id_task, title, desc, tag
                )

        @empty_not_found
        def list_tasks_on_lists():
            Printers.print_saved_lists()
            list_choice = UserMainInput.choice_list_to_show()
            logging.debug('Printing tasks on list')
            for list_id, id_task, title, desc, tag in TodoListHandler(
            ).current_tasks(list_choice):
                logging.info(f'List # {list_id}')
                Printers.print_task(
                    id_task, title, desc, tag
                )

        @empty_not_found
        def list_all_todo_lists():
            logging.debug('Printing all list')
            for list_id, task, title, description, tags in TodoListHandler(
            ).show_all_lists():
                logging.info(f'List # {list_id}')
                Printers.print_task(task, title, description, tags)


        functions = {
            ListOptions.LIST_CURRENT_TASKS.value: list_current,
            ListOptions.LIST_TASK_ON_LIST.value: list_tasks_on_lists,
            ListOptions.LIST_ALL_TODO_LISTS.value: list_all_todo_lists
        }

        try:
            Printers().print_list_submenu()
            choice_list_submenu = UserMainInput.choice_main_menu()
            functions[choice_list_submenu]()
        except KeyError:
            logging.error('! Please insert a valid ID (number)')

    @staticmethod
    def obtain_submenu() -> None:
        """User choice from Obtain:"""

        @empty_not_found
        def obtain_task_by_id():
            id_task_choice = UserMainInput.choice_task_to_show()
            list_id, task, title, description, tags = TaskHandler(
            ).search_task_id(id_task_choice)
            logging.debug('Printing task')
            logging.info(f'List # {list_id}')
            Printers.print_task(task, title, description, tags)

        @empty_not_found
        def obtain_list_by_id():
            Printers.print_saved_lists()
            id_list_choice = UserMainInput.choice_list_to_show()
            for list_id, id_task, title, desc, tag in TodoListHandler(
            ).current_tasks(id_list_choice):
                logging.debug('Printing list')
                logging.info(f'List # {list_id}')
                Printers.print_task(
                    id_task, title, desc, tag
                )

        functions = {
            ObtainOptions.OBTAIN_TASK_BY_ID.value: obtain_task_by_id,
            ObtainOptions.OBTAIN_LIST_BY_ID.value: obtain_list_by_id
        }

        try:
            Printers().print_obtain_submenu()
            choice_obtain_submenu = UserMainInput.choice_main_menu()
            functions[choice_obtain_submenu]()
        except KeyError:
            logging.error('! Please insert a valid ID (number)')

    @classmethod
    def show_list(cls, list_choice):
        for list_id, id_task, title, desc, tag in TodoListHandler(
        ).current_tasks(list_choice):
            logging.debug('Printing list')
            logging.info(f'List # {list_id}')
            Printers.print_task(
                id_task, title, desc, tag
            )
        return list_choice

    @classmethod
    def modify_task(cls):
        Printers.print_saved_lists()
        list_choice = UserMainInput.choice_list_to_show()
        try:
            cls.show_list(list_choice)
            task_mod_choice = UserMainInput.choice_task_to_show()
            TaskHandler().find_task(list_choice, task_mod_choice)
        except (IndexError, ItemNotFoundError):
            logging.error('! Item not found')
            return False
        except EmptyListError:
            logging.error('! The list is empty')
            return False
        title, description, tags = UserTaskInput(
        ).new_task_params()
        id_task, title, description, tags = TaskHandler().modify_task(
            list_choice, task_mod_choice, title, description, tags
        )
        logging.info(f'Task # {id_task} successfully modified!')
        Printers.print_task(id_task, title, description, tags)

    @classmethod
    def delete_task(cls):
        Printers.print_saved_lists()
        list_choice = UserMainInput.choice_list_to_show()
        try:
            cls.show_list(list_choice)
            task_del_choice = UserMainInput.choice_task_to_show()
            TaskHandler().find_task(list_choice, task_del_choice)
        except (IndexError, ItemNotFoundError):
            logging.error('! Item not found')
            return False
        except EmptyListError:
            logging.error('! The list is empty')
            return False
        id_task = TaskHandler().delete_task(list_choice, task_del_choice)
        logging.info(f'Task # {id_task} successfully deleted!')

    @staticmethod
    def search_submenu() -> None:
        """User choice from Search:"""

        def search_task_by_title():
            task_title_search = UserMainInput.choice_task_title()
            search = list(TaskHandler.search_task_title(task_title_search))
            if not search:
                logging.error('! Item not found')
                return False
            logging.debug('Printing tasks')
            for list_id, task, title, description, tags in search:
                logging.info(f'List # {list_id}')
                Printers.print_task(task, title, description, tags)

        def search_task_by_description():
            task_desc_search = UserMainInput.choice_task_description()
            search = list(TaskHandler.search_task_desc(task_desc_search))
            if not search:
                logging.error('! Item not found')
                return False
            logging.debug('Printing tasks')
            for list_id, task, title, description, tags in search:
                logging.info(f'List # {list_id}')
                Printers.print_task(task, title, description, tags)

        functions = {
            SearchOptions.SEARCH_TASK_BY_TITLE.value: search_task_by_title,
            SearchOptions.SEARCH_TASK_BY_DESCRIPTION.value:
                search_task_by_description
        }
        try:
            Printers().print_search_submenu()
            choice_search_submenu = UserMainInput.choice_main_menu()
            functions[choice_search_submenu]()
        except KeyError:
            logging.error('! Please insert a valid ID (number)')

    @staticmethod
    def sortgroup_submenu():
        """User choice from Sort or Group by:"""

        def sort_task_asc():
            ordered = SortGroupQueriesHandler.query_order_asc()
            for task in ordered:
                logging.debug('Printing tasks')
                Printers.print_task(
                    task['id'], task['task_title'], task['task_description']
                )

        def sort_task_desc():
            ordered = SortGroupQueriesHandler.query_order_desc()
            for task in ordered:
                logging.debug('Printing tasks')
                Printers.print_task(
                    task['id'], task['task_title'], task['task_description']
                )

        def group_tasks_by_tags():
            tag = UserQueriesInput.input_tag_group()
            tasks = SortGroupQueriesHandler.query_group_tag(tag)
            if not tasks:
                logging.error('! Item not found')
                return False
            logging.info(f'Results for tag: {tag}')
            for task in tasks:
                logging.debug('Printing tasks')
                Printers.print_task(
                    task['id'], task['task_title'],
                    task['task_description'], [tag]
                )

        functions = {
            SortGroupOptions.SORT_ASC.value: sort_task_asc,
            SortGroupOptions.SORT_DESC.value: sort_task_desc,
            SortGroupOptions.GROUP_BY_TAGS.value: group_tasks_by_tags
        }
        try:
            Printers().print_sortgroup_submenu()
            choice_sortgroup_submenu = UserMainInput.choice_main_menu()
            functions[choice_sortgroup_submenu]()
        except KeyError:
            logging.error('! Please insert a valid ID (number)')
