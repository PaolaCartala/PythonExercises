import os
import json


class OldListsManager:
    """Manage saved files."""

    def count_old_lists(self) -> int:
        return len(os.listdir('lists/'))

    def list_id_title_saved(self):
        folder = sorted(os.listdir('lists/'))
        lists = [files.split('_') for files in folder]
        return lists

    def list_id_saved(self) -> tuple[list]:
        folder = sorted(os.listdir('lists/'))
        id_lists = [files.split('_')[0] for files in folder]
        return id_lists

    def load_title_saved(self, id_list: str):
        for saved_list in self.list_id_title_saved():
            if str(id_list) == saved_list[0]:
                title = saved_list[1][:-5]
                return title
        return False

    def load_old_tasks(self, id_list: str) -> dict:
        if not self.load_title_saved(id_list):
            return False
        title = self.load_title_saved(id_list)
        try:
            with open(f'lists/{id_list}_{title}.json', 'r') as file:
                tasks = json.load(file)
            return tasks
        except FileNotFoundError:
            return False

    def count_old_tasks(self, id_list):
        try:
            return len(list(self.load_old_tasks(id_list).keys()))
        except AttributeError:
            return 0


def save_list(id_list, tasks) -> None:
    for saved_list in OldListsManager().list_id_title_saved():
        if str(id_list) == saved_list[0]:
            with open(f'lists/{saved_list[0]}_{saved_list[1]}', 'w') as f:
                json.dump(tasks, f, indent=2)
            break


def save_new_list(id_list, title, tasks):
    """Save a new To-Do list into .json file."""
    with open(f'lists/{id_list}_{title}.json', 'w') as f:
        json.dump(tasks, f, indent=2)


def validator_whitespaces(string: str):
    string_clean = string.strip()
    if string_clean == '':
        return False
    return string_clean
