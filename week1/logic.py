from random import randint
import re


all_lists = []


def show_menu():
    """It prints the main menu."""
    print(r"          Menu")
    print('------------------------')
    print("1) Create a new empty todo list")
    print("2) Add a new task to the list")
    print("3) List:")
    print("4) Obtain:")
    print("5) Modify a specific task by id")
    print("6) Delete a specific task")
    print("7) Search:")
    print("8) Exit\n")
    return None


def new_list():
    """It creates a new To-Do list.

    Returns:
        tuple: id_list:int is the list's ID, todo_list:dict is the empty list
    """
    id_list = randint(1, 100)
    todo_list = {str(id_list): []}
    all_lists.append(todo_list)
    return id_list, todo_list


def add_task(id_list, todo_list, title, description):
    """_summary_

    Args:
        id_list (int): To-Do list's ID where the task will be added
        todo_list (dict): list where the task will be added
        title (str): task's title
        description (str): task's description

    Returns:
        int: task's ID
    """
    id_task = randint(1, 100)
    task = {f'{id_task}': [title, description]}
    todo_list[str(id_list)].append(task)
    return id_task

# helper


def available_lists():
    """It prints the saved lists.

    Returns:
        tuple: id_list:int is the list's ID, todo_list:dict is the empty list
    """
    print('\nAvailable lists:')
    for lists in all_lists:
        for list_id in lists.keys():
            print(f"# {list_id}")
    print('------------------------\n')
    return list_id, lists


def current_tasks(id_list, todo_list):
    """It lists all the current tasks.

    Args:
        id_list (int): current To-Do list's ID
        todo_list (_type_): current To-Do list
    """
    for tasks in todo_list[str(id_list)]:
        for task_id in tasks.keys():
            print(f'Id: # {task_id}')
            print(f'Title: {tasks[str(task_id)][0]}')
            print(f'Description: {tasks[str(task_id)][1]}')
            print('------------------------\n')
    return None


def tasks_on_list(list_choice):
    """It lists the task on a list.

    Args:
        list_choice (str): user's input, list ID
    """
    for lists in all_lists:
        if list(lists.keys())[0] == list_choice:
            print("\nSearch result")
            print('------------------------')
            print(f'List # {list(lists.keys())[0]}')
            print('------------------------')
            for task in lists[list(lists.keys())[0]]:
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {task[list(task.keys())[0]][0]}')
                print(f'Description: {task[list(task.keys())[0]][1]}')
                print('------------------------\n')
    return None


def show_all_lists():
    """It lists all To-Do lists."""
    for lists in all_lists:
        id_list = list(lists.keys())[0]
        print(f'List # {id_list}')
        print('------------------------\n')
        for tasks in lists[id_list]:
            for task_id in tasks.keys():
                print(f'Id: # {task_id}')
                print(f'Title: {tasks[str(task_id)][0]}')
                print(f'Description: {tasks[str(task_id)][1]}')
                print('------------------------\n')
    return None


def search_task_id(id_task_choice):
    """It obtains a specific task by id.

    Args:
        id_task_choice (str): user's input, task ID
    """
    for lists in all_lists:
        list_of_key = list(lists.keys())
        for task in lists[list_of_key[0]]:
            if list(task.keys())[0] == id_task_choice:
                print("\nSearch result")
                print('------------------------')
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {task[list(task.keys())[0]][0]}')
                print(f'Description: {task[list(task.keys())[0]][1]}')
                print('------------------------\n')
    return None


def search_list_id(id_list_choice):
    """It obtains a specific list by id.

    Args:
        id_list_choice (str): user's input, list ID
    """
    for lists in all_lists:
        if list(lists.keys())[0] == id_list_choice:
            print("\nSearch result")
            print('------------------------')
            print(f'List # {list(lists.keys())[0]}')
            print('------------------------')
            for task in lists[list(lists.keys())[0]]:
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {task[list(task.keys())[0]][0]}')
                print(f'Description: {task[list(task.keys())[0]][1]}')
                print('------------------------\n')
    return None


def modify_task(task_modify_choice):
    """It modifies a specific task by id.

    Args:
        task_modify_choice (str): user's input, task ID to modify
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            if list(task.keys())[0] == task_modify_choice:
                title = input("Please insert a new title for this task:\n")
                task[list(task.keys())[0]][0] = title
                des = input("Please insert a new description for this task:\n")
                task[list(task.keys())[0]][1] = des
                print("\nTask succesfuly modified!\n")
                print('\n------------------------')
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {title}')
                print(f'Description: {des}')
                print('------------------------\n')
                break
    return None


def delete_task(task_del_choice):
    """It deletes a specific task.

    Args:
        task_del_choice (str): user's input, task ID to delete
    """
    for lists in all_lists:
        list_of_key = list(lists.keys())
        for task in lists[list_of_key[0]]:
            list_of_key_tasks = list(task.keys())
            if list_of_key_tasks[0] == task_del_choice:
                lists[list_of_key[0]].remove(task)
                break
    return None


def search_task_title(task_title_search):
    """It searches for a task using its title.

    Args:
        task_title_search (str): user's input, task title to search
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            res = re.search(task_title_search, task[list(task.keys())[0]][0])
            if res:
                print("\nSearch result")
                print('------------------------')
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {task[list(task.keys())[0]][0]}')
                print(f'Description: {task[list(task.keys())[0]][1]}')
                print('------------------------\n')
    return None


def search_task_desc(task_desc_search):
    """It searches for a task using its description.

    Args:
        task_title_search (str): user's input, task title to search
    """
    for lists in all_lists:
        for task in lists[list(lists.keys())[0]]:
            res = re.search(task_desc_search, task[list(task.keys())[0]][1])
            if res:
                print("\nSearch result")
                print('------------------------')
                print(f'Task: # {list(task.keys())[0]}')
                print(f'Title: {task[list(task.keys())[0]][0]}')
                print(f'Description: {task[list(task.keys())[0]][1]}')
                print('------------------------\n')
    return None
