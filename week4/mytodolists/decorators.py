import logging

from mytodolists.custom_exceptions import EmptyListError, ItemNotFoundError


def empty_not_found(function):
    def wrapper():
        try:
            function()
        except EmptyListError:
            logging.info('The list is empty')
        except (TypeError, IndexError, ItemNotFoundError):
            logging.error('! Item not found')
            return False
    return wrapper
