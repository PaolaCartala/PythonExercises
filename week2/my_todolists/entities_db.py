from dataclasses import dataclass


@dataclass
class TodoListDB:

    id_list: int
    tasks: dict

    def __str__(self) -> str:
        return f'List # {self.id_list}'


@dataclass
class TaskDB:

    id_task: int
    title: str
    description: str
    tags: list

    def __str__(self) -> str:
        return f'Task # {self.id_task}'
