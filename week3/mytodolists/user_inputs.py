from mytodolists.validators import validator_whitespaces


class UserMainInput:

    @staticmethod
    def choice_main_menu():
        return int(input("\nPlease select a choice: \n"))

    @staticmethod
    def choice_list_to_show():
        return input("\nPlease choose the list ID:\n")

    @staticmethod
    def choice_task_to_show():
        return input("\nPlease choose the task ID:\n")

    @staticmethod
    def choice_task_title():
        task_title = validator_whitespaces(
            input("Insert the title that you want to search:\n")
        )
        while not task_title:
            task_title = validator_whitespaces(
                input("Insert the title that you want to search:\n")
            )
        return task_title

    @staticmethod
    def choice_task_description():
        task_desc = validator_whitespaces(
            input("Insert the description that you want to search:\n")
        )
        while not task_desc:
            task_desc = validator_whitespaces(
                input("Insert the description that you want to search:\n")
            )
        return task_desc


class UserTaskInput:

    @classmethod
    def new_task_params(cls):
        """User inputs title, description, tags"""
        task_title = validator_whitespaces(
            input("\nPlease insert a title for this task:\n")
        )
        while not task_title:
            task_title = validator_whitespaces(
                input("\nPlease insert a title for this task:\n")
            )
        task_desc = validator_whitespaces(
            input("\nPlease insert a description:\n")
        )
        while not task_desc:
            task_desc = validator_whitespaces(
                input("\nPlease insert a description:\n")
            )
        tags = cls.add_tags()
        return task_title, task_desc, tags

    @classmethod
    def add_tags(cls):
        add = True
        tags = []
        while add:
            new_tag = input(
                "\nPlease insert a tag, leave blank to continue:\n"
            )
            if new_tag:
                tags.append(new_tag)
            else:
                add = False
        return tags


class UserListInput:

    @staticmethod
    def new_list_params():
        """User inputs title"""
        list_title = validator_whitespaces(
            input("\nPlease insert a title for this list:\n").capitalize()
        )
        while not list_title:
            list_title = validator_whitespaces(
                input("\nPlease insert a title for this list:\n").capitalize()
            )
        return list_title
