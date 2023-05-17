import os
import json


class OldListsManager:
    """Manage saved files."""

    def count_old_lists(self) -> int:
        return len(os.listdir('lists/'))

    def list_folder_content(self) -> list:
        folder = sorted(os.listdir('lists/'))
        id_lists = [file[:-5] for file in folder]
        return id_lists  # ['1', '2', '3', '4']

    def load_old_tasks(self, id_list: str) -> dict:
        try:
            with open(f'lists/{id_list}.json', 'r') as file:
                tasks = json.load(file)
            return tasks
        except FileNotFoundError:
            return False

    def count_old_tasks(self, id_list):
        try:
            return len(list(self.load_old_tasks(id_list).keys()))
        except AttributeError:
            return 0


class TxtSaver:
    """Save objects in .txt files."""

    def save_list(self, id_list, tasks) -> None:
        """Save a new To-Do list into .json file."""
        with open(f'lists/{id_list}.json', 'w') as f:
            json.dump(tasks, f, indent=2)

    def save_tasks(self, id_list: str, tasks: dict) -> None:
        """Write tasks into json file."""
        with open(f'lists/{id_list}.json', 'w') as f:
            json.dump(tasks, f, indent=2)
