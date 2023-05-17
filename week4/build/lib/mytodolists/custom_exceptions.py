class InputNotValidException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ItemNotFoundException(Exception):

    def __init__(self):
        super().__init__('No items were found, please try again.')
