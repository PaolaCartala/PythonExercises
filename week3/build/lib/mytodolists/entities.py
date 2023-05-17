from typing import Generator

from entities_db import TodoListDB, TaskDB
from logic import OldListsManager, save_list, save_new_list
from user_inputs import (
    UserMainInput, UserTaskInput, UserListInput
)


class TodoList:
    """To-Do List"""

    def __init__(self) -> None:
        self.id_list = OldListsManager().count_old_lists()
        self.all_id_lists = OldListsManager().list_id_saved()

    def create_list(self):
        """Create a new To-Do list."""
        title = UserListInput().new_list_params()
        new_list = TodoListDB(self.id_list + 1, title, dict())
        save_new_list(new_list.id_list, new_list.title, new_list.tasks)
        return new_list.id_list, new_list.title

    def add_task_to_list(self) -> int:
        """Add a new task to the list.

        Args:
            title (str): task's title
            description (str): task's description
            tags (list): task's tags

        Returns:
            int: task's ID
        """
        if self.id_list == 0:
            self.id_list = self.create_list()[0]
        id_list = UserMainInput().choice_list_to_show()
        try:
            tasks = OldListsManager().load_old_tasks(id_list)
        except FileNotFoundError:
            return False
        try:
            old_tasks = int(list(tasks.keys())[-1])
        except IndexError:
            old_tasks = 0
        task_title, task_description, tags = UserTaskInput().new_task_params()
        new_task = TaskDB(
            old_tasks + 1, task_title, task_description, tags
        )
        tasks[new_task.id_task] = [
            new_task.title, new_task.description, new_task.tags
        ]
        save_list(self.id_list, tasks)
        return (
            new_task.id_task, new_task.title,
            new_task.description, new_task.tags
        )

    def current_tasks(self) -> Generator[str, str, str]:
        """List all the tasks in the current list.

        Yields:
            Generator[str, str, str, list]: task id, title,
            description and tags of each task
        """
        """try:"""
        tasks = OldListsManager().load_old_tasks(self.id_list)
        for task in tasks:
            title, description, tags = tasks[task]
            yield task, title, description, tags
        """except TypeError:
            return False"""

    def tasks_on_list(self, list_choice: str) -> Generator[str, str, str]:
        """List the task in the selected list.

        Args:
            list_choice (str): user's input, list ID

        Yields:
            Generator[str, str, str, list]: task id, title,
            description and tags of each task
        """
        self.id_list = list_choice
        for task, title, description, tags in self.current_tasks():
            yield task, title, description, tags

    def search_list_id(self, id_list_choice: str) -> None:
        """Obtain a specific list by id.

        Args:
            id_list_choice (str): user's input, list ID
        """
        id_list_match = [
            file for file in OldListsManager(
            ).list_id_saved() if file == id_list_choice
        ]
        if id_list_match == []:
            return False
        self.id_list = id_list_match[0]
        for task, title, description, tags in self.current_tasks():
            yield task, title, description, tags

    def show_all_lists(self) -> None:
        """List all saved To-Do lists."""
        for file in OldListsManager().list_id_saved():
            self.id_list = file
            for task, title, description, tags in self.current_tasks():
                yield self.id_list, task, title, description, tags

    def __str__(self) -> str:
        tasks_num = OldListsManager().count_old_tasks(self.id_list)
        return f'List # {self.id_list}, Tasks: {tasks_num}'


class Task:

    def modify_task(
        self, list_choice: str, task_choice: str
    ) -> tuple[str, str, str, list]:
        """Modify a specific task by id.

        Args:
            list_choice (str): user's input, task ID to modify
            task_choice (str): user's input, task ID to modify

        Returns:
            tuple[str, str, str, list]: task_id, title, description
            and tags of the modified task
        """
        if not self.find_task(list_choice, task_choice):
            return False
        tasks, id_task = self.find_task(list_choice, task_choice)
        title, description, tags = UserTaskInput().new_task_params()
        tasks[id_task][0] = title
        tasks[id_task][1] = description
        tasks[id_task][2] = tags
        save_list(list_choice, tasks)
        return (
            id_task, tasks[id_task][0],
            tasks[id_task][1], tasks[id_task][2]
            )

    def delete_task(self, list_choice: str, task_choice: str) -> str:
        """Delete a specific task.

        Args:
            list_choice (str): user's input, list ID
            task_choice (str): user's input, task ID to delete

        Returns:
            str: deleted task's ID
        """
        if not self.find_task(list_choice, task_choice):
            return False
        tasks, id_task = self.find_task(list_choice, task_choice)
        del tasks[id_task]
        save_list(list_choice, tasks)
        return id_task

    def find_task(
        self, list_choice: str, task_choice: str
    ) -> tuple[dict, str]:
        """Search task in a selected list."""
        try:
            tasks = OldListsManager().load_old_tasks(list_choice)
            for id_task in tasks:
                if id_task == task_choice:
                    return tasks, id_task
        except FileNotFoundError:
            return False

    def search_task_id(self, id_task_choice: str) -> None:
        """Obtain a specific task by id.

        Args:
            id_task_choice (str): user's input, task ID
        """
        for file in OldListsManager().list_id_saved():
            for task in TodoList().tasks_on_list(file):
                if task[0] == id_task_choice:
                    yield file, task[0], task[1], task[2], task[3]

    def search_task(
        self, choice: int, task_search: str
    ) -> None:
        """Search for a task using its title or description.

        Args:
            choice (str): (1) search by title, (2) search by description
            task_search (str): task to search
        """
        for id_list in range(1, OldListsManager().count_old_lists() + 1):
            tasks = OldListsManager().load_old_tasks(str(id_list))
            for task in tasks:
                if task_search in tasks[task][choice - 1]:
                    title, description, tags = tasks[task]
                    yield id_list, task, title, description, tags
