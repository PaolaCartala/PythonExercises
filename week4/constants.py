from enum import Enum


class MainOptions(Enum):
    CREATE_NEW_LIST = 1
    ADD_NEW_TASK = 2
    LIST_OPTIONS = 3
    OBTAIN_OPTIONS = 4
    MODIFY_TASK = 5
    DELETE_TASK = 6
    SEARCH_OPTIONS = 7
    SORT_GROUP_TASKS = 8
    EXIT = 9


class ListOptions(Enum):
    LIST_CURRENT_TASKS = 1
    LIST_TASK_ON_LIST = 2
    LIST_ALL_TODO_LISTS = 3


class ObtainOptions(Enum):
    OBTAIN_TASK_BY_ID = 1
    OBTAIN_LIST_BY_ID = 2


class SearchOptions(Enum):
    SEARCH_TASK_BY_TITLE = 1
    SEARCH_TASK_BY_DESCRIPTION = 2


class SortGroupOptions(Enum):
    SORT_ASC = 1
    SORT_DESC = 2
    GROUP_BY_TAGS = 3
