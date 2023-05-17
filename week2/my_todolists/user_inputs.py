class UserMainInput:

    def choice_main_menu(self):
        return int(input("\nPlease select a choice: \n"))

    def choice_list_to_show(self):
        return input("Please choose the list ID:\n")

    def choice_task_to_show(self):
        return input("\nPlease choose the task ID:\n")

    def choice_task_title(self):
        return input("Insert the title that you want to search:\n")

    def choice_task_description(self):
        return input("Insert the description that you want to search:\n")


class UserTaskInput:

    def new_task_params(self):
        """User inputs title, description, tags"""
        title = input("\nPlease insert a title for this task:\n")
        description = input(
            "\nPlease insert a description:\n")
        tags = self.add_tags()
        return title, description, tags

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
