import unittest
from unittest.mock import patch

from mytodolists.data_access import OldListsManager
from mytodolists.handlers import TodoListHandler, TaskHandler
from user_interface import UserInterfaceManager
from mytodolists.user_inputs import UserMainInput, UserListInput, UserTaskInput


class TestUserInterfaceManager(unittest.TestCase):

    def setUp(self) -> None:
        self.user_interface = UserInterfaceManager
        return super().setUp()

    @patch.object(TodoListHandler, 'create_list', return_value=(1, 'Gym'))
    @patch.object(UserListInput, 'new_list_params', return_value='gym')
    def test_create_new_list(self, mocked_create, mocked_list_params):
        with self.assertLogs('root', level='DEBUG') as log:

            self.user_interface.create_new_list()

            self.assertEqual(len(log.output), 2)
            self.assertEqual(log.output, [
                'DEBUG:root:Title recorded',
                'DEBUG:root:New list created'
            ])

    @patch.object(UserMainInput, 'choice_list_to_show')
    @patch.object(TodoListHandler, 'search_list_id')
    @patch.object(UserTaskInput, 'new_task_params')
    def test_add_new_task(
        self, mocked_task_params, mocked_choice_list,
        mocked_search
    ):
        mocked_choice_list.return_value = '1'
        mocked_search.return_value = '1'
        mocked_task_params.return_value = (
            'task_title', 'task_description', ['tags']
        )

        with patch.object(TodoListHandler, 'add_task_to_list', return_value=(
            1, 'task_title', 'task_description', ['tags'])
        ) as mocked_add:
            with patch.object(
                OldListsManager, "count_old_lists", return_value=3
            ) as mocked_count:
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.add_new_task()
                    self.assertEqual(len(log.output), 3)
                    self.assertEqual(log.output, [
                        'DEBUG:root:List available',
                        'DEBUG:root:Parameters inserted',
                        'INFO:root:Task created'
                    ])

    @patch.object(TodoListHandler, 'current_tasks', return_value=[(
        '1', 'test title', 'test desc', ['tag1', 'tag2']
    )])
    @patch.object(TodoListHandler, 'show_all_lists', return_value=[(
        '1', '1', 'test title', 'test desc', ['tag1', 'tag2']
    )])
    def test_list_submenu(self, mocked_current_tasks, mocked_lists):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_list_submenu:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.list_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing current tasks'
                ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=3
        ) as choice_list_submenu:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.list_submenu()
                self.assertEqual(len(log.output), 2)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing all list',
                    'INFO:root:List # 1'
                ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value='error'
        ) as choice_list_submenu:
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.list_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Please insert a valid ID (number)'
                ])

    @patch.object(UserMainInput, 'choice_task_to_show', return_value='1')
    @patch.object(TaskHandler, 'search_task_id', return_value=[(
        '1', '1', 'test title', 'test desc', ['tag1', 'tag2']
    )])
    def test_obtain_submenu(self, mocked_choice_list, mocked_search_task_id):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_obtain_submenu:
            with self.assertLogs('root', level='INFO') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'INFO:root:List # 1'
                ])

    @patch.object(UserMainInput, 'choice_list_to_show', return_value='1')
    @patch.object(UserMainInput, 'choice_task_to_show', return_value='2')
    @patch.object(UserInterfaceManager, 'show_list', return_value=None)
    @patch.object(UserTaskInput, 'new_task_params', return_value=(
        'task_title', 'task_description', ['tags']
    ))
    def test_modify_task_flow(
        self, mocked_choice_list, mocked_printer_lists,
        mocked_choice_task, mocked_task_params
    ):
        with patch.object(
            OldListsManager, "count_old_lists", return_value=3
        ) as mocked_count:
            with patch.object(TaskHandler, 'modify_task', return_value=(
                1, 'task_title', 'task_description', ['tags'])
            ) as mocked_add:
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.modify_task()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'INFO:root:Task # 1 successfully modified!'
                    ])

            with patch.object(
                TaskHandler, 'modify_task', return_value=False
            ) as mocked_add:
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.modify_task()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:! Please insert a valid ID (number)'
                    ])

    @patch.object(UserMainInput, 'choice_list_to_show', return_value='1')
    @patch.object(UserMainInput, 'choice_task_to_show', return_value='2')
    @patch.object(UserInterfaceManager, 'show_list', return_value=None)
    def test_delete_task_flow(
        self, mocked_choice_list, mocked_printer_lists,
        mocked_choice_task
    ):
        with patch.object(
            OldListsManager, "count_old_lists", return_value=3
        ) as mocked_count:
            with patch.object(
                TaskHandler, 'delete_task', return_value='2'
            ) as mocked_add:
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.delete_task()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'INFO:root:Task # 2 succesfuly deleted!'
                    ])

            with patch.object(
                TaskHandler, 'delete_task', return_value=False
            ) as mocked_add:
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.delete_task()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:! Please insert a valid ID (number)'
                    ])

    @patch.object(UserMainInput, 'choice_task_title', return_value='title')
    @patch.object(
        UserMainInput, 'choice_task_description', return_value='desc'
    )
    def test_search_submenu(self, mocked_choice_title, mocked_choice_desc):
        with patch.object(TaskHandler, 'search_task', return_value=[(
            '1', '1', 'test title', 'test desc', ['tag1', 'tag2']
        )]) as mocked_search_task:
            with patch.object(
                UserMainInput, 'choice_main_menu', return_value=1
            ) as choice_search_submenu:
                with self.assertLogs('root', level='INFO') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'INFO:root:List # 1'
                    ])

        with patch.object(
            TaskHandler, 'search_task', return_value=False
        ) as mocked_search_task:
            with patch.object(
                UserMainInput, 'choice_main_menu', return_value=1
            ) as choice_search_submenu:
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:Search result\nNo results'
                    ])

        with patch.object(TaskHandler, 'search_task', return_value=[(
            '1', '1', 'test title', 'test desc', ['tag1', 'tag2']
        )]) as mocked_search_task:
            with patch.object(
                UserMainInput, 'choice_main_menu', return_value=2
            ) as choice_search_submenu:
                with self.assertLogs('root', level='INFO') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'INFO:root:List # 1'
                    ])

        with patch.object(
            TaskHandler, 'search_task', return_value=False
        ) as mocked_search_task:
            with patch.object(
                UserMainInput, 'choice_main_menu', return_value=2
            ) as choice_search_submenu:
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:Search result\nNo results'
                    ])


if __name__ == '__main__':
    unittest.main()
