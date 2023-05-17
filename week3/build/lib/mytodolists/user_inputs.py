from logic import validator_whitespaces


class UserMainInput:

    def choice_main_menu(self):
        return int(input("\nPlease select a choice: \n"))

    def choice_list_to_show(self):
        return input("\nPlease choose the list ID:\n")

    def choice_task_to_show(self):
        return input("\nPlease choose the task ID:\n")

    def choice_task_title(self):
        task_title = validator_whitespaces(
            input("Insert the title that you want to search:\n")
        )
        while not task_title:
            task_title = validator_whitespaces(
                input("Insert the title that you want to search:\n")
            )
        return task_title

    def choice_task_description(self):
        task_desc = validator_whitespaces(
            input("Insert the description that you want to search:\n")
        )
        while not task_desc:
            task_desc = validator_whitespaces(
                input("Insert the description that you want to search:\n")
            )
        return task_desc


class UserTaskInput:

    def new_task_params(self):
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
        tags = self.add_tags()
        return task_title, task_desc, tags

    def add_tags(self):
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

    def new_list_params(self):
        """User inputs title"""
        list_title = validator_whitespaces(
            input("\nPlease insert a title for this list:\n").capitalize()
        )
        while not list_title:
            list_title = validator_whitespaces(
                input("\nPlease insert a title for this list:\n").capitalize()
            )
        return list_title
