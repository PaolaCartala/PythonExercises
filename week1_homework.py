#%%
from random import randint
import re

#%%

all_lists = []

#%%
# funcion que cree una lista todo vacia
def new_list():  # la funcion la crea, despues hay que guardarla
    """_summary_

    Returns:
        _type_: _description_
    """
    # crear una lista de tareas nueva, vacía
    # se crea con un id para buscarla
    # TODO definir si conviene crearla con # o agregarlo despues
    id_list = randint(1, 100)
    # agrega la todo list nueva a todas las listas
    todo_list = {str(id_list): []}
    # devuelve la lista creada, para imprimirla y verificar que se creó
    # deberia guardar el id para saber donde guardar las tasks
    return id_list, todo_list

#%%
id_list, todo_list = new_list()
all_lists.append(todo_list)

print(f'Todo: {all_lists}')
print(f'Lista actual: {todo_list}')

#%%
# funcion que agregue una task a la lista
def add(id_list):
    """_summary_

    Args:
        todo (_type_): _description_
        task (_type_): _description_

    Returns:
        _type_: _description_
    """
    # titulo de la task
    title = input("Please introduce a title for this task:\n")
    # descripcion de la task
    description = input("Please introduce a description for this task:\n")
    # id de la task
    id_task = randint(1, 100)
    # crea la task
    task = {f'{id_task}': [title, description]}
    # la agrega al diccionario
    todo_list[str(id_list)].append(task)
    # retorna la task nueva
    return task

#%%
new_task = add(id_list)
print(f'New task: {new_task}')
print(f'Lista actual: {todo_list}')


#%%
print(f'Todo: {all_lists}')
print(f'Lista actual: {todo_list}')
print(f'New task: {new_task}')

#%%
# mostrar todas las tasks actuales
print("Current tasks\n-------------")
for tasks in todo_list[str(id_list)]:
    for task_id in tasks.keys():
        print(f'Id: # {task_id}')
        print(f'Title: {tasks[str(task_id)][0]}')
        print(f'Description: {tasks[str(task_id)][1]}')


#%%
# mostrar las tasks en una lista
#def tasks_on_list():

print(f'Listas disponibles:')
for lists in all_lists:
    for list_id in lists.keys():
        print(f"# {list_id}")
list_choice = input("Elija la lista a mostrar:")
for lists in all_lists:
    if list(lists.keys())[0] == list_choice:
        print("Resultado de la búsqueda\n------------------------")
        print(f'Lista # {list(lists.keys())[0]}\n------------------------')
        for task in lists[list(lists.keys())[0]]:
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}\n------------------------')
        break


#%%
# mostrar todas las listas

print(f'Listas disponibles:')
for lists in all_lists:
    for list_id in lists.keys():
        print(f"# {list_id}\n-------------")
        print("Tasks:")
        for tasks in lists[list_id]:
            for task_id in tasks.keys():
                print(f'Id: # {task_id}')
                print(f'Title: {tasks[str(task_id)][0]}')
                print(f'Description: {tasks[str(task_id)][1]}')


#%%
# buscar y mostrar una task segun su id

task_choice = input("Elija la tarea a mostrar:")

for lists in all_lists:
    list_of_key = list(lists.keys())
    # print(f'Lista # {list_of_key[0]}')
    for task in lists[list_of_key[0]]:
        if list(task.keys())[0] == task_choice:
            print("Resultado de la búsqueda\n------------------------")
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}')
            break


#%%
# buscar y mostrar una lista segun su id
list_choice = input("Elija la lista a mostrar:")

for lists in all_lists:
    if list(lists.keys())[0] == list_choice:
        print("Resultado de la búsqueda\n------------------------")
        print(f'Lista # {list(lists.keys())[0]}\n------------------------')
        for task in lists[list(lists.keys())[0]]:
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}\n------------------------')
        break


#%%
# modificar una task segun su id
task_modify_choice = input("Elija la tarea a modificar:")

for lists in all_lists:
    for task in lists[list(lists.keys())[0]]:
        if list(task.keys())[0] == task_modify_choice:
            task[list(task.keys())[0]][0] = input("Please introduce a title for this task:\n")
            task[list(task.keys())[0]][1] = input("Please introduce a description for this task:\n")
            print("Tarea modificada con éxito\n------------------------")
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}')
            break


#%%
# eliminar una task por su id
task_del_choice = input("Elija la tarea a eliminar:")

for lists in all_lists:
    for task in lists[list(lists.keys())[0]]:
        if list(task.keys())[0] == task_del_choice:
            print(lists[list(lists.keys())[0]])
            # del lists[list(lists.keys())[0]]


#%%
# buscar una task por su titulo
task_title_search = input("Ingrese el título que quiere buscar:")

for lists in all_lists:
    for task in lists[list(lists.keys())[0]]:
        list(task.keys())[0]
        x = re.search(task_title_search, task[list(task.keys())[0]][0])
        if x:
            print("Resultado de la búsqueda\n------------------------")
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}\n------------------------')

#%%
# buscar una task por su contenido
task_desc_search = input("Ingrese la descripción de la task que quiere buscar:")

for lists in all_lists:
    for task in lists[list(lists.keys())[0]]:
        list(task.keys())[0]
        x = re.search(task_desc_search, task[list(task.keys())[0]][1])
        if x:
            print("Resultado de la búsqueda\n------------------------")
            print(f'Task: # {list(task.keys())[0]}')
            print(f'Titulo: {task[list(task.keys())[0]][0]}')
            print(f'Descripción: {task[list(task.keys())[0]][1]}\n------------------------')
