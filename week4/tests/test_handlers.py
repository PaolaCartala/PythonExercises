import unittest
from unittest.mock import patch

from mytodolists.handlers import TodoListHandler, TaskHandler
from mytodolists.db_manager import (
    SelectQueriesHandler, InsertQueriesHandler,
    UpdateQueriesHandler, DeleteQueriesHandler
)
from mytodolists.custom_exceptions import ItemNotFoundError
from mytodolists.validators import CustomValidators


class TestTodoList(unittest.TestCase):

    def setUp(self) -> None:
        self.todo_list = TodoListHandler
        return super().setUp()

    @patch.object(InsertQueriesHandler, "query_insert_list", return_value=2)
    def test_create_list(self, mocked_insert):
        title = 'Test'

        self.assertEqual(
            self.todo_list.create_list(title), (2, 'Test')
        )

        title_error = '         '
        with self.assertLogs('root', level='ERROR') as log:
            self.todo_list.create_list(title_error)
            self.assertEqual(len(log.output), 1)
            self.assertEqual(log.output, [
                'ERROR:root:Title not valid'
            ])

    @patch.object(CustomValidators, 'params_validator', return_value=(
        'testing_title', 'testing_description'
    ))
    @patch.object(InsertQueriesHandler, "query_insert_task", return_value=3)
    @patch.object(InsertQueriesHandler, "query_insert_tags", return_value=2)
    @patch.object(
        InsertQueriesHandler, "query_insert_tasktag", return_value=None
    )
    def test_add_task_to_list(
        self, mocked_validator, mocked_insert,
        mocked_insert_tags, mocked_insert_tasktag
    ):
        add_task = self.todo_list.add_task_to_list(
            2, 'testing_title',
            'testing_description',
            ['testing_tag1', 'testing_tag2', 'testing_tag3']
        )

        self.assertEqual(add_task, (
            3, 'testing_title',
            'testing_description',
            ['testing_tag1', 'testing_tag2', 'testing_tag3']
        ))

        add_task_notags = self.todo_list.add_task_to_list(
            2, 'testing_title',
            'testing_description',
            []
        )

        self.assertEqual(add_task_notags, (
            3, 'testing_title',
            'testing_description',
            []
        ))

    @patch.object(
        SelectQueriesHandler, "query_select_last_list", return_value=1
    )
    @patch.object(TodoListHandler, 'search_list_id', return_value=2)
    @patch.object(SelectQueriesHandler, 'query_select_tags', side_effect=[
        [], ['tag1', 'tag2'], [], ['tag1', 'tag2']
    ])
    def test_current_tasks(self, mocked_list, mocked_search, mocked_tags):
        with patch.object(
            SelectQueriesHandler, "query_select_current", return_value=[
                {'id': 1, 'list_id': 1, 'task_title': 'test title1',
                 'task_description': 'test desc1'},
                {'id': 2, 'list_id': 1, 'task_title': 'test title2',
                 'task_description': 'test desc2'}
            ]
        ) as mocked_tasks:

            self.assertEqual(list(self.todo_list.current_tasks()), [(
                1, 1, 'test title1', 'test desc1', []),
                (1, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])
            ])

            self.assertEqual(list(self.todo_list.current_tasks('2')), [(
                2, 1, 'test title1', 'test desc1', []),
                (2, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])
            ])

    @patch.object(
        SelectQueriesHandler, "query_select_all_lists", return_value=[
            {'id': 1, 'title': 'test1'}, {'id': 2, 'title': 'test2'}
        ])
    def test_show_all_lists(self, mocked_list_saved):

        with patch.object(
            TodoListHandler, 'current_tasks'
        ) as mocked_current_tasks:
            items = [(
                1, 1, 'test title1', 'test desc1', []),
                (1, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])]
            mocked_current_tasks.return_value = items

            espected_return = [
                (1, 1, 'test title1', 'test desc1', []),
                (1, 2, 'test title2', 'test desc2', ['tag1', 'tag2']),
                (1, 1, 'test title1', 'test desc1', []),
                (1, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]

            self.assertEqual(
                list(self.todo_list.show_all_lists()), espected_return
            )


class TestTask(unittest.TestCase):

    def setUp(self) -> None:
        self.task = TaskHandler
        return super().setUp()

    @patch.object(TodoListHandler, "search_list_id", return_value=1)
    def test_find_task(self, mocked_search):
        with patch.object(
            SelectQueriesHandler, 'query_select_task'
        ) as mocked_tasks:
            mocked_tasks.return_value = {
                'id': 2, 'list_id': 1, 'task_title': 'test title',
                'task_description': 'test desc'
            }

            espected_return = {
                'id': 2, 'list_id': 1, 'task_title': 'test title',
                'task_description': 'test desc'
            }
            self.assertEqual(
                self.task.find_task(1, 2), (espected_return, 2)
            )

            mocked_tasks.return_value = False
            self.assertRaises(
                ItemNotFoundError, self.task.find_task, 1, 'test_false'
            )

    @patch.object(TaskHandler, "find_task")
    @patch.object(CustomValidators, 'params_validator', return_value=(
        'modified title', 'modified description'
    ))
    @patch.object(UpdateQueriesHandler, "query_update_task")
    @patch.object(InsertQueriesHandler, "query_insert_tags", return_value=2)
    @patch.object(
        InsertQueriesHandler, "query_insert_tasktag", return_value=None
    )
    def test_modify_task(
        self, mocked_find, mocked_validator, mocked_update_task,
        mocked_insert_tags, mocked_insert_tasktag
    ):
        mocked_find.return_value = ({
            'id': 2, 'list_id': 1, 'task_title': 'test title',
            'task_description': 'test desc'
        }, 2)

        mocked_update_task.return_value = {
            'id': 2, 'list_id': 1, 'task_title': 'modified title',
            'task_description': 'modified description'
        }
        espected_return = (
            2,
            'modified title', 'modified description',
            ['tests tag1', 'tests tag2']
        )
        self.assertEqual(self.task.modify_task(
            'mocked', '2',
            'modified title', 'modified description',
            ['tests tag1', 'tests tag2']
        ), espected_return)

    @patch.object(
        DeleteQueriesHandler, "query_delete_task", return_value=2
    )
    def test_delete_task(self, mocked_delete):
        with patch.object(TaskHandler, "find_task") as mocked_find:
            mocked_find.return_value = ({
                'id': 2, 'list_id': 1, 'task_title': 'test title',
                'task_description': 'test desc'
            }, 2)

            self.assertEqual(self.task.delete_task('mocked', 2), 2)

    @patch.object(
        SelectQueriesHandler, 'query_select_tags',
        return_value=['tests tag1', 'tests tag2']
    )
    def test_search_task_id(
        self, mocked_tags
    ):
        with patch.object(
            SelectQueriesHandler, 'query_select_task_id'
        ) as mocked_task:
            mocked_task.return_value = {
                'id': 2, 'list_id': 1, 'task_title': 'test title1',
                'task_description': 'test desc1'
            }

            espected_return = [
                1, 2, 'test title1', 'test desc1', ['tests tag1', 'tests tag2']
            ]
            self.assertEqual(
                list(self.task.search_task_id(2)), espected_return
            )

    @patch.object(SelectQueriesHandler, 'query_select_tags', side_effect=[
        [], ['tag1', 'tag2']
    ])
    def test_search_task_title(
        self, mocked_tags
    ):
        with patch.object(
            SelectQueriesHandler, 'query_select_task_title'
        ) as mocked_search:
            mocked_search.return_value = [
                {'id': 2, 'list_id': 1, 'task_title': 'test title1',
                    'task_description': 'test desc1'},
                {'id': 2, 'list_id': 2, 'task_title': 'test title2',
                    'task_description': 'test desc2'}
            ]

            espected_return = [
                (1, 2, 'test title1', 'test desc1', []),
                (2, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]

            self.assertEqual(
                list(self.task.search_task_title('test')), espected_return
            )

            mocked_search.return_value = []
            self.assertEqual(
                list(self.task.search_task_title('mocked')), []
            )

    @patch.object(SelectQueriesHandler, 'query_select_tags', side_effect=[
        [], ['tag1', 'tag2']
    ])
    def test_search_task_desc(
        self, mocked_tags
    ):
        with patch.object(
            SelectQueriesHandler, 'query_select_task_desc'
        ) as mocked_search:
            mocked_search.return_value = [
                {'id': 2, 'list_id': 1, 'task_title': 'test title1',
                    'task_description': 'test desc1'},
                {'id': 2, 'list_id': 2, 'task_title': 'test title2',
                    'task_description': 'test desc2'}
            ]

            espected_return = [
                (1, 2, 'test title1', 'test desc1', []),
                (2, 2, 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]

            self.assertEqual(
                list(self.task.search_task_desc('test')), espected_return
            )

            mocked_search.return_value = []
            self.assertEqual(
                list(self.task.search_task_desc('mocked')), []
            )


if __name__ == '__main__':
    unittest.main()
