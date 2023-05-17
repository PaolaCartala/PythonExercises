from typing import Generator
import re

from front import printer_lists, available_lists


all_lists = []


def new_list() -> tuple[int, dict[str, list]]:
    """Create a new To-Do list.

    Returns:
        tuple[int, dict[str, list]]: id_list:int is the list's ID,
        todo_list:dict is the empty list
    """
    id_list = len(all_lists) + 1
    todo_list = {str(id_list): []}
    all_lists.append(todo_list)
    available_lists(all_lists)
    return id_list, todo_list


def add_task(
    id_list: int, todo_list: dict[str, list], title: str, description: str
) -> int:
    """Add a new task to the list.

    Args:
        id_list (int): To-Do list's ID where the task will be added
        todo_list (dict[str, list]): list where the task will be added
        title (str): task's title
        description (str): task's description

    Returns:
        int: task's ID
    """
    if len(todo_list[str(id_list)]) == 0:
        id_task = len(todo_list[str(id_list)]) + 1
    else:
        task_id = [list(task.keys())[0] for task in todo_list[str(id_list)]]
        id_task = int(task_id[-1]) + 1
    task = {f'{id_task}': [title, description]}
    todo_list[str(id_list)].append(task)
    return id_task


def current_tasks(
    id_list: int, todo_list: dict[str, list]
) -> Generator[str, str, str]:
    """List all the current tasks.

    Args:
        id_list (int): current To-Do list's ID
        todo_list (dict[str, list]): current To-Do list

    Yields:
        Generator[str, str, str]: task_id, title and description of each task
    """
    for task in todo_list[str(id_list)]:
        task_id = list(task.keys())[0]
        title = task[list(task.keys())[0]][0]
        description = task[list(task.keys())[0]][1]
        yield task_id, title, description


def tasks_on_list(list_choice: str) -> Generator[str, str, str]:
    """List the task on a list.

    Args:
        list_choice (str): user's input, list ID

    Yields:
        Generator[str, str, str]: task_id, title and description
        of each task in the list
    """
    for lists in all_lists:
        if list(lists.keys())[0] == list_choice:
            list_id = list(lists.keys())[0]
            printer_lists(list_id)
            for task in lists[list(lists.keys())[0]]:
                task_id = list(task.keys())[0]
                title = task[list(task.keys())[0]][0]
                description = task[list(task.keys())[0]][1]
                yield task_id, title, description


def show_all_lists() -> Generator[str, str, str]:
    """List all To-Do lists.

    Yields:
        Generator[str, str, str]: task_id, title and description of each task
        in each list
    """
    for lists in all_lists:
        list_id = list(lists.keys())[0]
        printer_lists(list_id)
        for task in lists[list(lists.keys())[0]]:
            task_id = list(task.keys())[0]
            title = task[list(task.keys())[0]][0]
            description = task[list(task.keys())[0]][1]
            yield task_id, title, description


def search_task_id(id_task_choice: str) -> tuple[str, str, str]:
    """Obtain a specific task by id.

    Args:
        id_task_choice (str): user's input, task ID

    Returns:
        tuple[str, str, str]: task_id, title and description of searched task
    """
    for lists in all_lists:
        list_of_key = list(lists.keys())
        for task in lists[list_of_key[0]]:
            if list(task.keys())[0] == id_task_choice:
                task_id = list(task.keys())[0]
                title = task[list(task.keys())[0]][0]
                description = task[list(task.keys())[0]][1]
                return task_id, title, description


def search_list_id(id_list_choice: str) -> Generator[str, str, str]:
    """Obtain a specific list by id.

    Args:
        id_list_choice (str): user's input, list ID

    Yields:
        Generator[str, str, str]: task_id, title and description of each task
        in the searched list
    """
    for lists in all_lists:
        if list(lists.keys())[0] == id_list_choice:
            list_id = list(lists.keys())[0]
            printer_lists(list_id)
            for task in lists[list(lists.keys())[0]]:
                task_id = list(task.keys())[0]
                title = task[list(task.keys())[0]][0]
                description = task[list(task.keys())[0]][1]
                yield task_id, title, description


def modify_task(task_modify_choice: str) -> tuple[str, str, str]:
    """Modify a specific task by id.

    Args:
        task_modify_choice (str): user's input, task ID to modify

    Returns:
        tuple[str, str, str]: task_id, title and description of modified task
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            if list(task.keys())[0] == task_modify_choice:
                id_task = list(task.keys())[0]
                title = input("Please insert a new title for this task:\n")
                task[list(task.keys())[0]][0] = title
                description = input(
                    "Please insert a new description for this task:\n")
                task[list(task.keys())[0]][1] = description
                return id_task, title, description


def delete_task(task_del_choice: str) -> str:
    """Delete a specific task.

    Args:
        task_del_choice (str): user's input, task ID to delete

    Returns:
        str: deleted task's ID
    """
    for lists in all_lists:
        list_of_key = list(lists.keys())
        for task in lists[list_of_key[0]]:
            list_of_key_tasks = list(task.keys())
            if list_of_key_tasks[0] == task_del_choice:
                lists[list_of_key[0]].remove(task)
                return task_del_choice


def search_task_title(task_title_search: str) -> tuple[str, str, str]:
    """Search for a task using its title.

    Args:
        task_title_search (str): user's input, task title to search

    Returns:
        tuple[str, str, str]: task_id, title and description
        of the searched task
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            res = re.search(task_title_search, task[list(task.keys())[0]][0])
            if res:
                task_id = list(task.keys())[0]
                title = task[list(task.keys())[0]][0]
                description = task[list(task.keys())[0]][1]
                return task_id, title, description
            else:
                return None


def search_task_desc(task_desc_search: str) -> tuple[str, str, str]:
    """Search for a task using its description.

    Args:
        task_title_search (str): user's input, task title to search

    Returns:
        tuple[str, str, str]: task_id, title and description
        of the searched task
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            res = re.search(task_desc_search, task[list(task.keys())[0]][1])
            if res:
                task_id = list(task.keys())[0]
                title = task[list(task.keys())[0]][0]
                description = task[list(task.keys())[0]][1]
                return task_id, title, description
            else:
                return None
