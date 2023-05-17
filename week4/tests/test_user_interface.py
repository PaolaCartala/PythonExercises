import unittest
from unittest.mock import patch

from mytodolists.handlers import TodoListHandler, TaskHandler
from mytodolists.front import Printers
from user_interface import UserInterfaceManager
from mytodolists.user_inputs import (
    UserMainInput, UserListInput, UserTaskInput, UserQueriesInput
)
from mytodolists.db_manager import (
    SelectQueriesHandler, SortGroupQueriesHandler
)
from mytodolists.custom_exceptions import ItemNotFoundError


class TestUserInterfaceManager(unittest.TestCase):

    def setUp(self):
        self.user_interface = UserInterfaceManager

    @patch.object(UserListInput, 'new_list_params', return_value='gym')
    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    def test_create_new_list(self, mocked_list_params, mocked_prints):
        with patch.object(
            TodoListHandler, 'create_list'
        ) as mocked_create:
            mocked_create.return_value = (1, 'testing')
            mocked_create.side_effect = None

            with self.assertLogs('root', level='INFO') as log:

                self.user_interface.create_new_list()

                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'INFO:root:New list created!'
                ])

    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    @patch.object(
        SelectQueriesHandler, "query_select_all_lists", return_value=[
            {'id': 1, 'title': 'test1'}, {'id': 2, 'title': 'test2'}
        ])
    @patch.object(
        UserInterfaceManager, 'create_new_list',
        side_effect=None, return_value=(2, 'mocked')
    )
    @patch.object(UserMainInput, 'choice_list_to_show', return_value=2)
    @patch.object(TodoListHandler, 'search_list_id', return_value=2)
    @patch.object(UserTaskInput, 'new_task_params', return_value=(
        'task_title', 'task_description', ['tags']
    ))
    @patch.object(Printers, 'print_task', side_effect=None)
    def test_add_new_task(
        self, mocked_print, mocked_all_lists, mocked_new_list,
        mocked_choice_list, mocked_search, mocked_task_params,
        mocked_print_task
    ):
        with patch.object(TodoListHandler, 'add_task_to_list', return_value=(
            1, 'task_title', 'task_description', ['tags'])
        ) as mocked_add:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.add_new_task()
                self.assertEqual(len(log.output), 3)
                self.assertEqual(log.output, [
                    'DEBUG:root:List available',
                    'DEBUG:root:Parameters inserted',
                    'INFO:root:Task created'
                ])

    @patch.object(TodoListHandler, 'current_tasks', return_value=[(
        1, 1, 'test title', 'test desc', ['tag1', 'tag2']
    )])
    @patch.object(UserMainInput, 'choice_list_to_show', return_value=1)
    @patch.object(TodoListHandler, 'show_all_lists', return_value=[(
        1, 1, 'test title', 'test desc', ['tag1', 'tag2']
    )])
    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    @patch.object(Printers, 'print_task', side_effect=None)
    @patch.object(Printers, 'print_list_submenu', side_effect=None)
    def test_list_submenu(
        self, mocked_current_tasks, mocked_choice, mocked_all_lists,
        mocked_print_list, mocked_print_task, mocked_submenu
    ):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_list_submenu:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.list_submenu()
                self.assertEqual(len(log.output), 2)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing current tasks',
                    'INFO:root:List # 1'
                ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=2
        ) as choice_list_submenu:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.list_submenu()
                self.assertEqual(len(log.output), 2)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing tasks on list',
                    'INFO:root:List # 1'
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
    @patch.object(TaskHandler, 'search_task_id', return_value=(
        1, 1, 'test title', 'test desc', ['tag1', 'tag2']
    ))
    @patch.object(UserMainInput, 'choice_list_to_show', return_value='1')
    @patch.object(TodoListHandler, 'current_tasks', return_value=[(
        1, 1, 'test title', 'test desc', ['tag1', 'tag2']
    )])
    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    @patch.object(Printers, 'print_task', side_effect=None)
    @patch.object(Printers, 'print_obtain_submenu', side_effect=None)
    def test_obtain_submenu(
        self, mocked_choice_task, mocked_search_task_id,
        mocked_choice_list, mocked_current,
        mocked_print_list, mocked_print_task, mocked_submenu
    ):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_obtain_submenu:
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 2)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing task',
                    'INFO:root:List # 1'
                ])

            mocked_search_task_id.side_effect = ItemNotFoundError
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Item not found'
                ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=2
        ) as choice_obtain_submenu:
            mocked_search_task_id.side_effect = None
            mocked_search_task_id.return_value = (
                1, 'test title', 'test desc', ['tag1', 'tag2']
            )
            with self.assertLogs('root', level='DEBUG') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 2)
                self.assertEqual(log.output, [
                    'DEBUG:root:Printing list',
                    'INFO:root:List # 1'
                ])

            mocked_search_task_id.side_effect = ItemNotFoundError
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Item not found'
                ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value='error'
        ) as choice_obtain_submenu:
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.obtain_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Please insert a valid ID (number)'
                ])

    @patch.object(UserMainInput, 'choice_list_to_show', return_value='1')
    @patch.object(UserMainInput, 'choice_task_to_show', return_value='2')
    @patch.object(UserInterfaceManager, 'show_list', side_effect=None)
    @patch.object(TaskHandler, 'find_task', side_effect=None)
    @patch.object(UserTaskInput, 'new_task_params', return_value=(
        'task_title', 'task_description', ['tags']
    ))
    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    @patch.object(Printers, 'print_task', side_effect=None)
    def test_modify_task_flow(
        self, mocked_choice_list, mocked_choice_task,
        mocked_show_list, mocked_find, mocked_task_params,
        mocked_printer_lists, mocked_print_task
    ):
        with patch.object(TaskHandler, 'modify_task', return_value=(
            2, 'task_title', 'task_description', ['tags'])
        ) as mocked_mod:
            with self.assertLogs('root', level='INFO') as log:
                self.user_interface.modify_task()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'INFO:root:Task # 2 successfully modified!'
                ])

            mocked_find.side_effect = ItemNotFoundError
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.modify_task()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Item not found'
                ])

    @patch.object(UserMainInput, 'choice_list_to_show', return_value='1')
    @patch.object(UserMainInput, 'choice_task_to_show', return_value='2')
    @patch.object(UserInterfaceManager, 'show_list', side_effect=None)
    @patch.object(TaskHandler, 'find_task', side_effect=None)
    @patch.object(Printers, 'print_saved_lists', side_effect=None)
    def test_delete_task_flow(
        self, mocked_choice_list, mocked_choice_task,
        mocked_show, mocked_find, mocked_printer_lists
    ):
        with patch.object(
            TaskHandler, 'delete_task', return_value=2
        ) as mocked_del:
            with self.assertLogs('root', level='INFO') as log:
                self.user_interface.delete_task()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'INFO:root:Task # 2 successfully deleted!'
                ])

            mocked_find.side_effect = ItemNotFoundError
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.delete_task()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Item not found'
                ])

    @patch.object(UserMainInput, 'choice_task_title', return_value='title')
    @patch.object(
        UserMainInput, 'choice_task_description', return_value='desc'
    )
    @patch.object(Printers, 'print_task', side_effect=(None, None))
    @patch.object(Printers, 'print_search_submenu', side_effect=None)
    def test_search_submenu(
        self, mocked_choice_title, mocked_choice_desc,
        mocked_print_task, mocked_submenu
    ):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_search_submenu:
            with patch.object(
                TaskHandler, 'search_task_title'
            ) as mocked_search_title:
                mocked_search_title.return_value = [(
                    1, 1, 'test title', 'test desc', ['tag1', 'tag2']
                )]
                with patch.object(
                    UserMainInput, 'choice_main_menu', return_value=1
                ) as choice_search_submenu:
                    with self.assertLogs('root', level='DEBUG') as log:
                        self.user_interface.search_submenu()
                        self.assertEqual(len(log.output), 2)
                        self.assertEqual(log.output, [
                            'DEBUG:root:Printing tasks',
                            'INFO:root:List # 1'
                        ])

                mocked_search_title.return_value = []
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:! Item not found'
                    ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=2
        ) as choice_search_submenu:
            with patch.object(
                TaskHandler, 'search_task_desc', return_value=[(
                    1, 1, 'test title', 'test desc', ['tag1', 'tag2']
                )]
            ) as mocked_search_desc:
                mocked_search_desc.return_value = [(
                    1, 1, 'test title', 'test desc', ['tag1', 'tag2']
                )]
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 2)
                    self.assertEqual(log.output, [
                        'DEBUG:root:Printing tasks',
                        'INFO:root:List # 1'
                    ])

                mocked_search_desc.return_value = []
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.search_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:! Item not found'
                    ])
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value='error'
        ) as choice_search_submenu:
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.search_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Please insert a valid ID (number)'
                ])

    @patch.object(UserQueriesInput, 'input_tag_group', return_value='test')
    @patch.object(Printers, 'print_task', side_effect=None)
    @patch.object(Printers, 'print_sortgroup_submenu', side_effect=None)
    def test_sortgroup_submenu(
        self, mocked_user_tag, mocked_print_task, mocked_submenu
    ):
        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=1
        ) as choice_sortgroup_submenu:
            with patch.object(
                SortGroupQueriesHandler, "query_order_asc"
            ) as mocked_asc_query:
                mocked_asc_query.return_value = [
                    {'id': 3, 'task_title': 'a',
                     'task_description': 'test desc'},
                    {'id': 2, 'task_title': 'b',
                     'task_description': 'test desc'},
                    {'id': 4, 'task_title': 'c',
                     'task_description': 'test desc'}
                ]
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.sortgroup_submenu()
                    self.assertEqual(len(log.output), 3)
                    self.assertEqual(log.output, [
                        'DEBUG:root:Printing tasks',
                        'DEBUG:root:Printing tasks',
                        'DEBUG:root:Printing tasks'
                    ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=2
        ) as choice_sortgroup_submenu:
            with patch.object(
                SortGroupQueriesHandler, "query_order_desc"
            ) as mocked_desc_query:
                mocked_desc_query.return_value = [
                    {'id': 4, 'task_title': 'c',
                     'task_description': 'test desc'},
                    {'id': 2, 'task_title': 'b',
                     'task_description': 'test desc'},
                    {'id': 3, 'task_title': 'a',
                     'task_description': 'test desc'}
                ]
                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.sortgroup_submenu()
                    self.assertEqual(len(log.output), 3)
                    self.assertEqual(log.output, [
                        'DEBUG:root:Printing tasks',
                        'DEBUG:root:Printing tasks',
                        'DEBUG:root:Printing tasks'
                    ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value=3
        ) as choice_sortgroup_submenu:
            with patch.object(
                SortGroupQueriesHandler, "query_group_tag"
            ) as mocked_desc_query:
                mocked_desc_query.return_value = [
                    {'tag_value': 'test', 'id': 3, 'task_title': 'task title',
                     'task_description': 'test desc'},
                    {'tag_value': 'test', 'id': 4, 'task_title': 'task title',
                     'task_description': 'test desc'}
                ]

                with self.assertLogs('root', level='DEBUG') as log:
                    self.user_interface.sortgroup_submenu()
                    self.assertEqual(len(log.output), 3)
                    self.assertEqual(log.output, [
                        'INFO:root:Results for tag: test',
                        'DEBUG:root:Printing tasks',
                        'DEBUG:root:Printing tasks'
                    ])

                mocked_desc_query.return_value = []
                with self.assertLogs('root', level='ERROR') as log:
                    self.user_interface.sortgroup_submenu()
                    self.assertEqual(len(log.output), 1)
                    self.assertEqual(log.output, [
                        'ERROR:root:! Item not found'
                    ])

        with patch.object(
            UserMainInput, 'choice_main_menu', return_value='error'
        ) as choice_list_submenu:
            with self.assertLogs('root', level='ERROR') as log:
                self.user_interface.sortgroup_submenu()
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output, [
                    'ERROR:root:! Please insert a valid ID (number)'
                ])


if __name__ == '__main__':
    unittest.main()
