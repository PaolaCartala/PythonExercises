import unittest
from unittest.mock import patch

from mytodolists.handlers import TodoListHandler, TaskHandler
from mytodolists.data_access import OldListsManager, SaveList


class TestTodoList(unittest.TestCase):

    def setUp(self) -> None:
        self.todo_list = TodoListHandler
        return super().setUp()

    @patch.object(OldListsManager, "count_old_lists", return_value=3)
    @patch.object(SaveList, "save_new_list")
    def test_create_list(self, mocked_count, mocked_save):
        title = 'Supermarket'

        self.assertEqual(
            self.todo_list.create_list(title), (4, 'Supermarket')
        )

        title_error = '         '
        self.assertEqual(self.todo_list.create_list(title_error), False)

    @patch.object(SaveList, "save_list")
    @patch.object(OldListsManager, "count_old_lists", return_value=3)
    @patch.object(OldListsManager, "load_old_tasks")
    def test_add_task_to_list(
        self, mocked_save, mocked_count, mocked_loader
    ):
        add_task_error = self.todo_list.add_task_to_list(
            '3', '       ',
            'testing_description',
            ['testing_tag1', 'testing_tag2']
        )
        self.assertEqual(add_task_error, False)

        with patch.object(
            OldListsManager, "charge_key_old_tasks", return_value=2
        ) as mocked_id_saved:
            mocked_loader.return_value = {
                '1': ['test title1', 'test desc1', []],
                '2': ['test title2', 'test desc2', []]
            }

            add_task = self.todo_list.add_task_to_list(
                '2', 'testing_title',
                'testing_description',
                ['testing_tag1', 'testing_tag2', 'testing_tag3']
            )
            self.assertEqual(add_task, (
                3, 'testing_title',
                'testing_description',
                ['testing_tag1', 'testing_tag2', 'testing_tag3']
            ))

            with self.assertLogs('root', level='DEBUG') as log:
                with patch.object(
                    OldListsManager, "load_old_tasks", return_value='empty'
                ) as mocked_loader:
                    self.todo_list.add_task_to_list(
                        '2', 'testing_title',
                        'testing_description',
                        ['testing_tag1', 'testing_tag2', 'testing_tag3']
                    )
                    self.assertEqual(len(log.output), 3)
                    self.assertEqual(log.output, [
                        'DEBUG:root:The list is empty',
                        'DEBUG:root:Task added to TaskDB',
                        'DEBUG:root:Task saved to files'
                    ])

            with patch.object(
                TodoListHandler, 'create_list'
            ) as mocked_create_list:
                mocked_count.return_value = 0
                mocked_create_list.return_value = (1, 'mocked title')

                mocked_loader.return_value = {}
                mocked_id_saved.return_value = 0

                add_task = self.todo_list.add_task_to_list(
                    '1', 'testing_title',
                    'testing_description',
                    ['testing_tag1', 'testing_tag2']
                )

                self.assertEqual(add_task, (
                    1, 'testing_title',
                    'testing_description',
                    ['testing_tag1', 'testing_tag2']
                ))

    @patch.object(OldListsManager, "count_old_lists", return_value=3)
    def test_current_tasks(self, mocked_count):
        return_loader = {
            '1': ['test title1', 'test desc1', []],
            '2': ['test title2', 'test desc2', ['tag1', 'tag2']]
        }
        with patch.object(
            OldListsManager, "load_old_tasks", return_value=return_loader
        ) as mocked_loader:

            self.assertEqual(list(self.todo_list.current_tasks()), [(
                '1', 'test title1', 'test desc1', []),
                ('2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ])

            self.assertEqual(list(self.todo_list.current_tasks('2')), [(
                '1', 'test title1', 'test desc1', []),
                ('2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ])

            mocked_loader.return_value = False

            self.assertEqual(
                list(self.todo_list.current_tasks('test')), []
            )

            with self.assertLogs('root', level='DEBUG') as log:
                with patch.object(
                    OldListsManager, "load_old_tasks", return_value={}
                ) as mocked_loader:
                    list(self.todo_list.current_tasks())
                    self.assertEqual(len(log.output), 2)
                    self.assertEqual(log.output, [
                        'DEBUG:root:Loading tasks: True',
                        'INFO:root:The list # 3 is empty'
                    ])

    @patch.object(
        OldListsManager, "list_id_saved", return_value=['1', '2', '3']
    )
    def test_search_list_id(self, mocked_list_saved):
        with patch.object(
            TodoListHandler, 'current_tasks'
        ) as mocked_current_tasks:
            items = [(
                '1', 'test title1', 'test desc1', []),
                ('2', 'test title2', 'test desc2', ['tag1', 'tag2'])]
            mocked_current_tasks.return_value = items

            self.assertEqual(self.todo_list.search_list_id('2'), '2')

            self.assertEqual(self.todo_list.search_list_id('4'), False)

    @patch.object(OldListsManager, "list_id_saved")
    def test_show_all_lists(self, mocked_list_saved):
        mocked_list_saved.return_value = ['1', '2']

        with patch.object(
            TodoListHandler, 'current_tasks'
        ) as mocked_current_tasks:
            items = [(
                '1', 'test title1', 'test desc1', []),
                ('2', 'test title2', 'test desc2', ['tag1', 'tag2'])]
            mocked_current_tasks.return_value = items

            espected_return = [
                ('1', '1', 'test title1', 'test desc1', []),
                ('1', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('2', '1', 'test title1', 'test desc1', []),
                ('2', '2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]

            self.assertEqual(
                list(self.todo_list.show_all_lists()), espected_return
            )


class TestTask(unittest.TestCase):

    def setUp(self) -> None:
        self.task = TaskHandler
        return super().setUp()

    @patch.object(SaveList, "save_list")
    def test_modify_task(self, mocked_save):
        with patch.object(TaskHandler, "find_task") as mocked_find_task:
            mocked_find_task.return_value = ({
                '1': ['test title1', 'test desc1', []],
                '2': ['test title2', 'test desc2', ['tag1', 'tag2']]
            }, '2')

            espected_return = (
                '2',
                'modified title', 'modified description',
                ['tests tag1', 'tests tag2']
            )
            self.assertEqual(self.task.modify_task(
                'mocked', '2',
                'modified title', 'modified description',
                ['tests tag1', 'tests tag2']
            ), espected_return)

            with self.assertLogs('root', level='ERROR') as log:
                self.task.modify_task(
                    '2', '2',
                    False, 'descr',
                    ['tag1', 'tag2']
                )

                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    "ERROR:root:Title: False, desc: descr, tag: <class 'list'>"
                ])

            mocked_find_task.return_value = False

            self.assertEqual(self.task.modify_task(
                'mocked', 'test_false',
                'modified title', 'modified description',
                ['tests tag1', 'tests tag2']
            ), False)

    @patch.object(SaveList, "save_list")
    def test_delete_task(self, mocked_save):
        with patch.object(TaskHandler, "find_task") as mocked_find_task:
            mocked_find_task.return_value = ({
                '1': ['test title1', 'test desc1', []],
                '2': ['test title2', 'test desc2', ['tag1', 'tag2']]
            }, '2')

            self.assertEqual(self.task.delete_task('mocked', '2'), '2')

            mocked_find_task.return_value = False

            self.assertEqual(
                self.task.delete_task('mocked', 'test_false'), False
            )

    @patch.object(OldListsManager, "load_old_tasks")
    def test_find_task(self, mocked_loader):
        mocked_loader.return_value = {
            '1': ['test title1', 'test desc1', []],
            '2': ['test title2', 'test desc2', ['tag1', 'tag2']]
        }

        tasks = mocked_loader.return_value

        self.assertEqual(
            self.task.find_task('mocked', '2'), (tasks, '2')
        )

        mocked_loader.return_value = False

        self.assertEqual(
            self.task.find_task('mocked', 'test_false'), False
        )

    @patch.object(TodoListHandler, 'current_tasks')
    @patch.object(OldListsManager, "count_old_lists", return_value=3)
    @patch.object(OldListsManager, "list_id_saved")
    def test_search_task_id(
        self, mocked_current_tasks, mocked_count, mocked_id_saved
    ):
        with patch.object(TodoListHandler, 'show_all_lists') as mocked_lists:
            mocked_id_saved.return_value = ['1', '2', '3']
            items = [
                ('1', '1', 'test title1', 'test desc1', []),
                ('1', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('2', '1', 'test title1', 'test desc1', []),
                ('2', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('3', '1', 'test title1', 'test desc1', []),
                ('3', '2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]
            mocked_current_tasks.return_value = items

            mocked_lists.return_value = mocked_current_tasks.return_value

            espected_return = [
                ('1', '1', 'test title1', 'test desc1', []),
                ('2', '1', 'test title1', 'test desc1', []),
                ('3', '1', 'test title1', 'test desc1', [])
            ]
            self.assertEqual(
                list(self.task.search_task_id('1')), espected_return
            )

            self.assertEqual(
                list(self.task.search_task_id('test')), []
            )

    @patch.object(TodoListHandler, 'current_tasks')
    @patch.object(OldListsManager, "count_old_lists", return_value=3)
    @patch.object(OldListsManager, "list_id_saved")
    def test_search_task(
        self, mocked_current_tasks, mocked_count, mocked_id_saved
    ):
        with patch.object(TodoListHandler, 'show_all_lists') as mocked_lists:
            mocked_id_saved.return_value = ['1', '2', '3']
            items = [
                ('1', '1', 'test title1', 'test desc1', []),
                ('1', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('2', '1', 'test title1', 'test desc1', []),
                ('2', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('3', '1', 'test title1', 'test desc1', []),
                ('3', '2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]
            mocked_current_tasks.return_value = items

            mocked_lists.return_value = mocked_current_tasks.return_value

            espected_return = [
                ('1', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('2', '2', 'test title2', 'test desc2', ['tag1', 'tag2']),
                ('3', '2', 'test title2', 'test desc2', ['tag1', 'tag2'])
            ]

            self.assertEqual(
                list(self.task.search_task(1, '2')), espected_return
            )

            self.assertEqual(
                list(self.task.search_task(2, 'desc2')), espected_return
            )

            self.assertEqual(
                list(self.task.search_task(1, 'error')), []
            )

            self.assertEqual(
                list(self.task.search_task('error', '2')), []
            )


if __name__ == '__main__':
    unittest.main()
