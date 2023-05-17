import logging
import os
import json


class OldListsManager:
    """Manage saved files."""

    @staticmethod
    def count_old_lists() -> int:
        """Count files in lists folder"""
        try:
            return len(os.listdir('lists/'))
        except FileNotFoundError:
            logging.critical('Please create a lists/ folder')

    @classmethod
    def list_id_title_saved(cls) -> list:
        """List id and title of saved lists"""
        folder = sorted(os.listdir('lists/'))
        lists = [files.split('_') for files in folder]
        return lists

    @staticmethod
    def list_id_saved() -> list[str]:
        """List id of saved lists"""
        folder = sorted(os.listdir('lists/'))
        id_lists = [files.split('_')[0] for files in folder]
        return id_lists

    @classmethod
    def load_title_saved(cls, id_list: str) -> str:
        """Load title of saved lists"""
        for saved_list in cls.list_id_title_saved():
            if str(id_list) == saved_list[0]:
                title = saved_list[1][:-5]
                return title
        return False

    @classmethod
    def load_old_tasks(cls, id_list: str) -> dict:
        """Load tasks of saved lists"""
        if not cls.load_title_saved(id_list):
            return False
        title = cls.load_title_saved(id_list)
        with open(f'lists/{id_list}_{title}.json', 'r') as file:
            tasks = json.load(file)
            return tasks

    @classmethod
    def count_old_tasks(cls, id_list) -> int:
        """Count tasks of saved lists"""
        try:
            return len(list(cls.load_old_tasks(id_list).keys()))
        except AttributeError:
            return 0

    @classmethod
    def charge_key_old_tasks(cls, id_list) -> int:
        """Load saved task's id"""
        tasks = cls.load_old_tasks(id_list)
        try:
            old_tasks_id = int(list(tasks.keys())[-1])
            return old_tasks_id
        except (IndexError, AttributeError):
            return 0


class SaveList:

    @staticmethod
    def save_list(id_list, tasks) -> None:
        for saved_list in OldListsManager().list_id_title_saved():
            if str(id_list) == saved_list[0]:
                with open(f'lists/{saved_list[0]}_{saved_list[1]}', 'w') as f:
                    json.dump(tasks, f, indent=2)
                break

    @staticmethod
    def save_new_list(id_list, title, tasks):
        """Save a new To-Do list into .json file."""
        if not int(id_list) or not title or type(tasks) != dict:
            return False
        with open(f'lists/{id_list}_{title}.json', 'w') as f:
            json.dump(tasks, f, indent=2)
