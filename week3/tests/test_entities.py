import unittest

from mytodolists.entities import TaskDB, TodoListDB


class TestTodoListDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.todolist = TodoListDB(1, 'supermarket', dict())
        return super().setUpClass()

    def test_id_list(self):
        self.assertEqual(self.todolist.id_list, 1)

    def test_title(self):
        self.assertEqual(self.todolist.title, 'supermarket')

    def test_tasks(self):
        self.assertEqual(self.todolist.tasks, {})

    def test_str(self):
        self.assertEqual(str(self.todolist), 'List # 1')


class TestTaskDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.task = TaskDB(1, 'test title', 'test description', ['tag1'])
        return super().setUpClass()

    def test_id_task(self):
        self.assertEqual(self.task.id_task, 1)

    def test_title(self):
        self.assertEqual(self.task.title, 'test title')

    def test_description(self):
        self.assertEqual(self.task.description, 'test description')

    def test_tags(self):
        self.assertEqual(self.task.tags, ['tag1'])

    def test_str(self):
        self.assertEqual(self.task.__str__(), 'Task # 1')


if __name__ == '__main__':
    unittest.main()
