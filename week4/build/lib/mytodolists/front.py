import logging

from mytodolists.db_manager import SelectQueriesHandler


class Printers:

    @staticmethod
    def print_welcome() -> None:
        logging.info("Welcome to your To-Do Lists!\
                     \n----------------------------")

    @staticmethod
    def print_menu() -> None:
        """Print the main menu."""
        logging.info("          Menu\n------------------------")
        logging.info("1) Create a new empty todo list\
                    \n2) Add a new task to the list\
                    \n3) List:\
                    \n4) Obtain:\
                    \n5) Modify a specific task by id\
                    \n6) Delete a specific task\
                    \n7) Search:\
                    \n8) Exit\n")

    @staticmethod
    def print_list_submenu() -> None:
        """Submenu List:"""
        logging.info("1) List current tasks\
                    \n2) List tasks on a list\
                    \n3) List all To-Do lists\n")

    @staticmethod
    def print_obtain_submenu() -> None:
        """Subenu Obtain:"""
        logging.info("1) Obtain a specific task by id\
                    \n2) Obtain a specific list by id\n")

    @staticmethod
    def print_search_submenu() -> None:
        """Subenu Search:"""
        logging.info("1) Search for a task by its title\
                    \n2) Search for a task by its content\n")

    @staticmethod
    def print_error_choice() -> None:
        logging.info("! Please select a choice from the list")

    @staticmethod
    def print_saved_lists() -> None:
        """Print the saved lists."""
        logging.info('Available lists:')
        all_lists = SelectQueriesHandler.query_select_all_lists()
        for record in all_lists:
            logging.info(f"# {record['id']} {record['title'].capitalize()}")

    @staticmethod
    def print_task(
        id_task: str, title: str, description: str, tags: list
    ) -> None:
        """Print a task."""
        try:
            logging.info(f'Task: # {id_task}\nTitle: {title.capitalize()}\
                        \nDescription: {description.capitalize()}\nTags: {",".join(tags)}')
        except TypeError:
            logging.info(f'Task: # {id_task}\nTitle: {title.capitalize()}\
                        \nDescription: {description.capitalize()}')
