from typing import Generator
import logging
import re

from mytodolists.custom_exceptions import InputNotValidException
from mytodolists.entities import TodoListDB, TaskDB
from mytodolists.data_access import OldListsManager, SaveList
from mytodolists.validators import validator_whitespaces


class TodoListHandler:
    """To-Do List"""

    @staticmethod
    def create_list(title):
        """Create a new To-Do list."""
        id_list = OldListsManager.count_old_lists()
        title_clean = validator_whitespaces(title)
        if not title_clean:
            logging.error('Title not valid')
            return False
        try:
            new_list = TodoListDB(
                id_list + 1, title_clean.capitalize(), dict()
            )
        except TypeError:
            return False
        logging.debug('List added to TodoListDB')
        SaveList().save_new_list(
            new_list.id_list, new_list.title, new_list.tasks
        )
        logging.debug('List saved to files')
        return new_list.id_list, new_list.title

    @staticmethod
    def add_task_to_list(
        choice_id_list, task_title, task_description, tags
    ) -> int:
        """Add a new task to the list.

        Args:
            title (str): task's title
            description (str): task's description
            tags (list): task's tags

        Returns:
            int: task's ID
        """
        id_list = OldListsManager.count_old_lists()
        title_clean = validator_whitespaces(task_title)
        description_clean = validator_whitespaces(task_description)
        if not title_clean or not description_clean or type(tags) != list:
            logging.error(
                f'Title: {title_clean}, desc: {description_clean}, tag: {tags}'
            )
            return False
        old_tasks_id = OldListsManager().charge_key_old_tasks(choice_id_list)
        tasks = OldListsManager().load_old_tasks(choice_id_list)
        if tasks == 'empty':
            logging.debug('The list is empty')
            tasks = {}
        new_task = TaskDB(
            old_tasks_id + 1, title_clean, task_description, tags
        )
        logging.debug('Task added to TaskDB')
        try:
            tasks[new_task.id_task] = [
                new_task.title, new_task.description, new_task.tags
            ]
        except TypeError:
            return False
        SaveList().save_list(id_list, tasks)
        logging.debug('Task saved to files')
        return (
            new_task.id_task, new_task.title,
            new_task.description, new_task.tags
        )

    @classmethod
    def current_tasks(
        cls, list_choice: str = 'default'
    ) -> Generator[str, str, str]:
        """List all the tasks in the current list.

        Yields:
            Generator[str, str, str, list]: task id, title,
            description and tags of each task
        """
        if list_choice == 'default':
            id_list = OldListsManager.count_old_lists()
            tasks = OldListsManager().load_old_tasks(str(id_list))
            logging.debug(f'Loading tasks: {tasks != False}')
        else:
            id_list = list_choice
            tasks = OldListsManager().load_old_tasks(id_list)
            logging.debug(f'Loading tasks: {tasks != False}')
        if not tasks and tasks != {}:
            logging.debug(f'Tasks: {tasks}')
            return False
        if tasks == {}:
            logging.info(f'The list # {id_list} is empty')
        for task in tasks:
            title, description, tags = tasks[str(task)]
            yield task, title, description, tags

    @staticmethod
    def search_list_id(id_list_choice: str) -> None:
        """Obtain a specific list by id.

        Args:
            id_list_choice (str): user's input, list ID
        """
        id_list_match = [
            id_list for id_list in OldListsManager.list_id_saved(
            ) if id_list == id_list_choice
        ]
        if not id_list_match:
            logging.error('List not found')
            return False
        return id_list_match[0]

    @classmethod
    def show_all_lists(cls) -> None:
        """List all saved To-Do lists."""
        for id_list in OldListsManager.list_id_saved():
            for task, title, description, tags in list(
                cls.current_tasks(id_list)
            ):
                yield id_list, task, title, description, tags


class TaskHandler:

    @classmethod
    def modify_task(
        cls, list_choice: str, task_choice: str,
        title: str, description: str, tags: list
    ) -> tuple[str, str, str, list]:
        """Modify a specific task by id.

        Args:
            list_choice (str): user's input, task ID to modify
            task_choice (str): user's input, task ID to modify

        Returns:
            tuple[str, str, str, list]: task_id, title, description
            and tags of the modified task
        """
        try:
            tasks, id_task = cls.find_task(list_choice, task_choice)
        except TypeError:
            return False
        title_clean = validator_whitespaces(title)
        desc_clean = validator_whitespaces(description)
        if not title_clean or not desc_clean or type(tags) != list:
            logging.error(
                f'Title: {title_clean}, desc: {desc_clean}, tag: {type(tags)}'
            )
            return False
        tasks[id_task][0] = title_clean
        tasks[id_task][1] = desc_clean
        tasks[id_task][2] = tags
        logging.debug('New params loaded')
        SaveList().save_list(list_choice, tasks)
        logging.debug('Task saved to files')
        return (
            id_task, tasks[id_task][0],
            tasks[id_task][1], tasks[id_task][2]
        )

    @classmethod
    def delete_task(cls, list_choice: str, task_choice: str) -> str:
        """Delete a specific task.

        Args:
            list_choice (str): user's input, list ID
            task_choice (str): user's input, task ID to delete

        Returns:
            str: deleted task's ID
        """
        try:
            tasks, id_task = cls.find_task(list_choice, task_choice)
        except TypeError:
            return False
        del tasks[id_task]
        logging.debug(f'Task {id_task} deleted')
        SaveList().save_list(list_choice, tasks)
        return id_task

    @classmethod
    def find_task(
        cls, list_choice: str, task_choice: str
    ) -> tuple[dict, str]:
        """Search task in a selected list."""
        tasks = OldListsManager().load_old_tasks(list_choice)
        if not tasks:
            logging.error('List not found')
            return False
        logging.debug(f'Loading tasks: {tasks != False}')
        try:
            id_task = [id_task for id_task in tasks if id_task == task_choice]
            if not id_task:
                return False
            return tasks, id_task[0]
        except IndexError:
            logging.exception('Task not found')
            return False

    @staticmethod
    def search_task_id(id_task_choice: str) -> None:
        """Obtain a specific task by id.

        Args:
            id_task_choice (str): user's input, task ID
        """
        all_lists = list(TodoListHandler().show_all_lists())
        for task in all_lists:
            if task[1] == id_task_choice:
                yield task[0], task[1], task[2], task[3], task[4]

    @staticmethod
    def search_task(
        search_by: int, task_search: str
    ) -> None:
        """Search for a task using its title or description.

        Args:
            search_by (str): (1) search by title, (2) search by description
            task_search (str): task to search
        """
        all_lists = list(TodoListHandler().show_all_lists())
        for task in all_lists:
            try:
                if re.search(task_search, task[int(search_by) + 1]):
                    yield task[0], task[1], task[2], task[3], task[4]
            except IndexError:
                raise InputNotValidException('Please insert a valid number')
            except ValueError:
                logging.error('! Please insert a valid number')
