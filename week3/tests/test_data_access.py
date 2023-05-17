import unittest
from unittest.mock import patch

from mytodolists.data_access import OldListsManager


class TestOldListsManager(unittest.TestCase):

    def setUp(self) -> None:
        self.list_manager = OldListsManager
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @patch('os.listdir')
    def test_count_old_lists(self, mocked_files):
        mocked_files.return_value = [
            '1_Gym.json', '2_Supermarket.json', '3_Shopping.json'
        ]

        self.assertEqual(self.list_manager.count_old_lists(), 3)

    @patch('os.listdir')
    def test_list_id_title_saved(self, mocked_files):
        mocked_files.return_value = [
            '1_Gym.json', '2_Supermarket.json', '3_Shopping.json'
        ]

        espected_return = [
            ['1', 'Gym.json'],
            ['2', 'Supermarket.json'],
            ['3', 'Shopping.json']
        ]

        self.assertEqual(
            self.list_manager.list_id_title_saved(), espected_return
        )

    @patch('os.listdir')
    def test_list_id_saved(self, mocked_files):
        mocked_files.return_value = [
            '1_Gym.json', '2_Supermarket.json', '3_Shopping.json'
        ]

        self.assertEqual(
            self.list_manager.list_id_saved(),
            ['1', '2', '3']
        )

    @patch('os.listdir')
    def test_load_title_saved(self, mocked_files):
        mocked_files.return_value = [
            '1_Gym.json', '2_Supermarket.json', '3_Shopping.json'
        ]
        with patch.object(OldListsManager, 'list_id_saved') as mocked_id_saved:
            mocked_id_saved.return_value = ['1', '2', '3']

            self.assertEqual(
                self.list_manager.load_title_saved('2'),
                'Supermarket'
            )

            self.assertEqual(
                self.list_manager.load_title_saved('error'),
                False
            )

    @patch.object(OldListsManager, 'load_old_tasks')
    def test_count_old_tasks(self, mocked_old_tasks):
        mocked_old_tasks.return_value = {
            '1': ['test title1', 'test desc1', []],
            '2': ['test title2', 'test desc2', []]
        }

        self.assertEqual(self.list_manager.count_old_tasks('2'), 2)

        mocked_old_tasks.return_value = False

        self.assertEqual(self.list_manager.count_old_tasks('error'), 0)

    @patch.object(OldListsManager, 'load_old_tasks')
    def test_charge_key_old_tasks(self, mocked_old_tasks):
        mocked_old_tasks.return_value = {
            '1': ['test title1', 'test desc1', []],
            '2': ['test title2', 'test desc2', []]
        }

        self.assertEqual(self.list_manager.charge_key_old_tasks('2'), 2)

        mocked_old_tasks.return_value = False
        self.assertEqual(self.list_manager.charge_key_old_tasks('error'), 0)


if __name__ == '__main__':
    unittest.main()
