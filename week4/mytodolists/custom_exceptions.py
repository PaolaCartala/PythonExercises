class InputNotValidError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ItemNotFoundError(Exception):

    def __init__(self):
        super().__init__('No items were found, please try again.')


class EmptyListError(Exception):

    def __init__(self) -> None:
        super().__init__('The list is empty')


class TableDoesntExistError(Exception):

    def __init__(self) -> None:
        super().__init__('Please initialize the database')


class DatabaseNotConnectedError(Exception):

    def __init__(self) -> None:
        super().__init__('Database not connected')
