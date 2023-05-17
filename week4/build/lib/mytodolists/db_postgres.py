import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy.exc import ResourceClosedError
import os
import logging

from mytodolists.custom_exceptions import ItemNotFoundException


class InsertQueriesHandler:

    @staticmethod
    def query_insert_list(title: str):
        query = text("INSERT INTO lists (title) VALUES (:title) RETURNING id;")
        dict_vars = {'title': title.lower()}
        save_id = DBManager().queries_executer(query, dict_vars)[0]
        logging.debug('Query executed')
        return save_id['id']

    @staticmethod
    def query_insert_task(
        list_id: int, task_title: str, task_description: str
    ):
        query = text(
            "INSERT INTO tasks (list_id, task_title, task_description) \
            VALUES (:list_id, :task_title, :task_description) \
            RETURNING id;"
        )
        dict_vars = {
            'list_id': list_id, 'task_title': task_title.lower(),
            'task_description': task_description.lower()
        }
        save_id = DBManager().queries_executer(query, dict_vars)[0]
        logging.debug('Query executed')
        return save_id['id']

    @staticmethod
    def query_insert_tags(tag: str):
        query = text("INSERT INTO tag (tag_value) VALUES (:tag) RETURNING id;")
        dict_vars = {'tag': tag.lower()}
        save_id = DBManager().queries_executer(query, dict_vars)[0]
        logging.debug('Query executed')
        return save_id['id']

    @staticmethod
    def query_insert_tasktag(id_task: int, id_tag: int):
        query = text("INSERT INTO tasks_tag (task_id, tag_id) \
        VALUES (:id_task, :id_tag);")
        dict_vars = {'id_task': id_task, 'id_tag': id_tag}
        DBManager().queries_executer(query, dict_vars)
        logging.debug('Query executed')


class SelectQueriesHandler:

    @staticmethod
    def query_select_current(list_choice: int):
        query_current = text('SELECT * FROM tasks WHERE list_id = :id_list')
        dict_vars = {'id_list': list_choice}
        tasks = DBManager().queries_executer(query_current, dict_vars)
        logging.debug('Query executed')
        return tasks

    @staticmethod
    def query_select_task(list_choice: int, task_choice: int):
        query_current = text('SELECT * FROM tasks \
            WHERE list_id = :id_list AND id = :task_choice')
        dict_vars = {'id_list': list_choice, 'task_choice': task_choice}
        try:
            task = DBManager().queries_executer(query_current, dict_vars)
            logging.debug('Query executed')
            return task[0]
        except IndexError:
            logging.debug('! No item returned')
            raise ItemNotFoundException()

    @staticmethod
    def query_select_last_list():
        query_last_list = "SELECT MAX(id) FROM lists"
        id_list = DBManager().queries_executer(query_last_list)[0]['max']
        logging.debug('Query executed')
        return id_list

    @staticmethod
    def query_select_tags(task_id: int):
        query_id_tags = text("SELECT (tag.tag_value) FROM tasks \
            INNER JOIN tasks_tag ON tasks.id = tasks_tag.task_id \
                INNER JOIN tag ON tasks_tag.tag_id = tag.id \
                    WHERE tasks.id = :id;")
        dict_vars = {'id': task_id}
        all_tags = DBManager().queries_executer(query_id_tags, dict_vars)
        logging.debug('Query executed')
        if not all_tags:
            return False
        tags = [tag['tag_value'] for tag in all_tags]
        return tags

    @staticmethod
    def query_select_id_list(id_list_choice: int):
        query_id_list = text("SELECT id FROM lists WHERE id = :list_id")
        dict_vars = {'list_id': id_list_choice}
        try:
            list_data = DBManager().queries_executer(query_id_list, dict_vars)
            logging.debug('Query executed')
            return list_data[0]
        except IndexError:
            logging.debug('! No item returned')
            raise ItemNotFoundException()

    def query_select_all_lists():
        query_id_list = text("SELECT * FROM lists")
        list_data = DBManager().queries_executer(query_id_list)
        return list_data

    @staticmethod
    def query_select_task_id(task_choice: int):
        query_current = text('SELECT * FROM tasks \
            WHERE id = :task_choice')
        dict_vars = {'task_choice': task_choice}
        try:
            task = DBManager().queries_executer(query_current, dict_vars)
            logging.debug('Query executed')
            return task[0]
        except IndexError:
            logging.debug('! No item returned')
            raise ItemNotFoundException()

    @staticmethod
    def query_select_task_title(search: str):
        query_current = text(
            "SELECT * FROM tasks WHERE task_title LIKE :value"
        )
        dict_vars = {'value': f'%{search.lower()}%'}
        task = DBManager().queries_executer(query_current, dict_vars)
        logging.debug('Query executed')
        return task

    @staticmethod
    def query_select_task_desc(search: str):
        query_current = text(
            "SELECT * FROM tasks WHERE task_description LIKE :value"
        )
        dict_vars = {'value': f'%{search.lower()}%'}
        task = DBManager().queries_executer(query_current, dict_vars)
        logging.debug('Query executed')
        return task


class UpdateQueriesHandler:

    @staticmethod
    def query_update_task(id_task: int, title: str, desc: str):
        query_update = text(
            "UPDATE tasks SET task_title = :title, \
            task_description = :desc WHERE id = :id_task \
            RETURNING id, task_title, task_description"
        )
        dict_vars = {'title': title, 'desc': desc, 'id_task': id_task}
        task_data = DBManager().queries_executer(query_update, dict_vars)[0]
        logging.debug('Query executed')
        return task_data


class DeleteQueriesHandler:

    @staticmethod
    def query_delete_tags(id_task: int):
        query_tags = text("DELETE FROM tasks_tag WHERE task_id = :id")
        dict_tag_vars = {'id': id_task}
        DBManager().queries_executer(query_tags, dict_tag_vars)
        logging.debug('Query executed')

    @staticmethod
    def query_delete_task(id_task: int):
        query_task = text("DELETE FROM tasks WHERE id = :id")
        dict_task_vars = {'id': id_task}
        DBManager().queries_executer(query_task, dict_task_vars)
        logging.debug('Query executed')
        return id_task


class SortGroupQueriesHandler:

    @staticmethod
    def query_order_asc():
        query = "SELECT task_title, task_description \
            FROM tasks ORDER BY task_title ASC;"
        ordered = DBManager().queries_executer(query)
        return ordered

    @staticmethod
    def query_order_desc():
        query = "SELECT task_title, task_description \
            FROM tasks ORDER BY task_title DESC;"
        ordered = DBManager().queries_executer(query)
        return ordered

    @staticmethod
    def query_group_tag(tag: str):
        query = "SELECT tag.tag_value, task_title, task_description \
            FROM tasks INNER JOIN tasks_tag ON tasks.id = tasks_tag.task_id \
                INNER JOIN tag ON tasks_tag.tag_id = tag.id \
                    WHERE tag.tag_value = :tag \
                        GROUP BY tag.tag_value, task_title, task_description;"
        dict_vars = {'tag': tag}
        tasks = DBManager().queries_executer(query, dict_vars)
        return tasks


class DBManager:

    def __init__(self) -> None:
        self.db = sqlalchemy.create_engine(os.getenv('TODOLIST_DB'))
        logging.debug('Database loaded')

    def queries_executer(self, query: str, vars: dict = None):
        with self.db.connect() as connection:
            logging.debug('Successful connection')
            res = connection.execute(query, vars)
            try:
                result_list = [
                    {col: value for col, value in res_row._mapping.items()}
                    for res_row in res
                ]
                logging.debug('Returning row values')
                return result_list
            except ResourceClosedError:
                return res
