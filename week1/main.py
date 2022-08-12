from logic import (
    show_menu, new_list, add_task, available_lists,
    current_tasks, tasks_on_list, show_all_lists,
    search_task_id, search_list_id, modify_task,
    delete_task, search_task_title, search_task_desc
)


print("\nWelcome to your To-Do Lists!")
print('--------------------------\n')


def app():
    """Main app."""

    show_menu()

    ask = True
    while ask:
        choice = int(input("Please select a choice: \n"))
        if choice == 1:
            global id_list
            global todo_list
            id_list, todo_list = new_list()
            print("\nToDo list created!\n")
            available_lists()
            show_menu()
        elif choice == 2:
            title = input("\nPlease introduce a title for this task:\n")
            description = input(
                "\nPlease introduce a description for this task:\n")
            id_task = add_task(id_list, todo_list, title, description)
            print("\nTask created!\n")
            print('------------------------')
            print(f'Id: # {id_task}')
            print(f'Title: {title}')
            print(f'Description: {description}')
            print('------------------------\n')
            show_menu()
        elif choice == 3:
            print("\n1) List current tasks")
            print("2) List tasks on a list")
            print("3) List all To-Do lists")
            choice_3 = int(input("\nPlease select a choice: \n"))
            if choice_3 == 1:
                print("\nCurrent tasks")
                print('------------------------\n')
                current_tasks(id_list, todo_list)
                show_menu()
            elif choice_3 == 2:
                available_lists()
                list_choice = input("Please choose the list to show:\n")
                tasks_on_list(list_choice)
                show_menu()
            elif choice_3 == 3:
                available_lists()
                print('------------------------')
                print("Tasks:")
                print('------------------------')
                show_all_lists()
                show_menu()
            else:
                print("\n! Please select a choice from the list\n")
                show_menu()
                continue
        elif choice == 4:
            print("\n1) Obtain a specific task by id")
            print("2) Obtain a specific list by id")
            choice_4 = int(input("\nPlease select a choice: \n"))
            if choice_4 == 1:
                id_task_choice = input(
                    "\nPlease choose the task id to show:\n")
                search_task_id(id_task_choice)
                show_menu()
            elif choice_4 == 2:
                available_lists()
                id_list_choice = input("Please choose the list id to show:\n")
                search_list_id(id_list_choice)
                show_menu()
            else:
                print("\n! Please select a choice from the list")
                show_menu()
                continue
        elif choice == 5:
            show_all_lists()
            task_modify_choice = input("Please choose the task to modify:\n")
            modify_task(task_modify_choice)
            show_menu()
        elif choice == 6:
            show_all_lists()
            task_del_choice = input(
                "\nPlease choose the task to delete:\n")
            delete_task(task_del_choice)
            print("\nTask succesfuly deleted!\n")
            print('\n------------------------')
            show_menu()
        elif choice == 7:
            print("\n1) Search for a task by its title")
            print("2) Search for a task by its content")
            choice_7 = int(input("\nPlease select a choice: \n"))
            if choice_7 == 1:
                task_title_search = input(
                    "Insert the title that you want to search:\n")
                search_task_title(task_title_search)
                show_menu()
            elif choice_7 == 2:
                task_desc_search = input(
                    "Insert the description that you want to search:\n")
                search_task_desc(task_desc_search)
                show_menu()
            else:
                print("\n! Please select a choice from the list")
                show_menu()
        elif choice == 8:
            ask = False
        else:
            print("\n! Please, insert a number from the menu\n")
            show_menu()
    return None


if __name__ == '__main__':
    app()
