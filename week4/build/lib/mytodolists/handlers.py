from typing import Generator
import logging

from mytodolists.validators import validator_whitespaces, params_validator
from mytodolists.db_manager import (
    InsertQueriesHandler, SelectQueriesHandler,
    UpdateQueriesHandler, DeleteQueriesHandler
)


class TodoListHandler:
    """To-Do List"""

    @staticmethod
    def create_list(title: str) -> tuple[int, str]:
        """Create a new To-Do list."""
        title_clean = validator_whitespaces(title)
        if not title_clean:
            logging.error('Title not valid')
            return False
        list_id = InsertQueriesHandler().query_insert_list(title_clean)
        logging.debug(f'List {list_id} saved to DB')
        return list_id, title_clean

    @staticmethod
    def add_task_to_list(
        choice_id_list: int, task_title: str, task_description: str, tags: list
    ) -> tuple[int, str, str, list]:
        """Add a new task to the list.

        Args:
            title (str): task's title
            description (str): task's description
            tags (list): task's tags

        Returns:
            int: task's ID
        """
        title_clean, description_clean = params_validator(
            task_title, task_description, tags
        )
        task_id = InsertQueriesHandler(
        ).query_insert_task(choice_id_list, title_clean, description_clean)
        if tags:
            for tag in tags:
                tag_id = InsertQueriesHandler().query_insert_tags(tag)
                InsertQueriesHandler().query_insert_tasktag(task_id, tag_id)
        logging.debug('Task saved to files')
        return (
            task_id, title_clean, description_clean, tags
        )

    @classmethod
    def current_tasks(
        cls, list_choice: int = 0
    ) -> Generator[int, str, str]:
        """List all the tasks in the current list.

        Yields:
            Generator[str, str, str, list]: task id, title,
            description and tags of each task
        """
        if list_choice == 0:
            list_id = SelectQueriesHandler.query_select_last_list()
        else:
            list_id = cls.search_list_id(list_choice)
        logging.info(f'List # {list_id}')
        tasks = SelectQueriesHandler(
        ).query_select_current(list_id)
        if not tasks:
            logging.info('The list is empty')
        for task in tasks:
            tags = SelectQueriesHandler.query_select_tags(task['id'])
            yield (
                task['id'], task['task_title'],
                task['task_description'], tags
            )

    @classmethod
    def search_list_id(cls, id_list_choice: str) -> int:
        """Obtain a specific list by id.

        Args:
            id_list_choice (str): user's input, list ID
        """
        list_match = SelectQueriesHandler.query_select_id_list(id_list_choice)
        return list_match['id']

    @classmethod
    def show_all_lists(cls) -> Generator[int, str, str]:
        """List all saved To-Do lists."""
        all_lists = SelectQueriesHandler.query_select_all_lists()
        for lists in all_lists:
            for id_task, title, description, tags in list(
                cls.current_tasks(lists['id'])
            ):
                yield id_task, title, description, tags


class TaskHandler:

    @classmethod
    def find_task(
        cls, list_choice: str, task_choice: str
    ) -> tuple[dict, int]:
        """Search task in a selected list."""
        list_id = TodoListHandler().search_list_id(list_choice)
        task = SelectQueriesHandler.query_select_task(list_id, task_choice)
        logging.debug(f'Loading tasks: {task != False}')
        return task, task['id']

    @classmethod
    def modify_task(
        cls, list_choice: int, task_choice: int,
        title: str, description: str, tags: list
    ) -> tuple[int, str, str, list]:
        """Modify a specific task by id.

        Args:
            list_choice (str): user's input, task ID to modify
            task_choice (str): user's input, task ID to modify

        Returns:
            tuple[str, str, str, list]: task_id, title, description
            and tags of the modified task
        """
        id_task_search = cls.find_task(list_choice, task_choice)[1]
        title_clean, desc_clean = params_validator(
            title, description, tags
        )
        task_data = UpdateQueriesHandler.query_update_task(
            id_task_search, title_clean, desc_clean
        )
        DeleteQueriesHandler.query_delete_tags(task_data['id'])
        if tags:
            for tag in tags:
                tag_id = InsertQueriesHandler().query_insert_tags(tag)
                InsertQueriesHandler().query_insert_tasktag(
                    task_data['id'], tag_id
                )
        return (
            task_data['id'], task_data['task_title'],
            task_data['task_description'], tags
        )

    @classmethod
    def delete_task(cls, list_choice: str, task_choice: str) -> int:
        """Delete a specific task.

        Args:
            list_choice (str): user's input, list ID
            task_choice (str): user's input, task ID to delete

        Returns:
            str: deleted task's ID
        """
        id_task_search = cls.find_task(list_choice, task_choice)[1]
        id_task = DeleteQueriesHandler.query_delete_task(id_task_search)
        logging.debug(f'Task {id_task} deleted')
        return id_task

    @staticmethod
    def search_task_id(id_task_choice: str) -> Generator[int, str, str]:
        """Obtain a specific task by id.

        Args:
            id_task_choice (str): user's input, task ID
        """
        task = SelectQueriesHandler.query_select_task_id(id_task_choice)
        logging.info(f'List # {task["list_id"]}')
        tags = SelectQueriesHandler.query_select_tags(task['id'])
        return (
            task['id'], task['task_title'],
            task['task_description'], tags
        )

    @staticmethod
    def search_task_title(search: str) -> Generator[int, str, str]:
        """Search for a task using its title.

        Args:
            task_search (str): task to search
        """
        tasks = SelectQueriesHandler.query_select_task_title(search)
        for task in tasks:
            logging.info(f'List # {task["list_id"]}')
            tags = SelectQueriesHandler.query_select_tags(task['id'])
            yield (
                task['id'], task['task_title'],
                task['task_description'], tags
            )

    @staticmethod
    def search_task_desc(search: str) -> Generator[int, str, str]:
        """Search for a task using its description.

        Args:
            task_search (str): task to search
        """
        tasks = SelectQueriesHandler.query_select_task_desc(search)
        for task in tasks:
            logging.info(f'List # {task["list_id"]}')
            tags = SelectQueriesHandler.query_select_tags(task['id'])
            yield (
                task['id'], task['task_title'],
                task['task_description'], tags
            )
