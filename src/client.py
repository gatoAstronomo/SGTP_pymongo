from requests import get, post, put, delete
import re

SERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def get_tasks(rut: str):
    data = {'rut': rut}
    response = get(f'{URL}/tasks', json=data)
    status = response.status_code

    if status == 200:
        return response.json()
    elif status == 404:
        print("rut no encontrado")
    else:
        print("error al descargar sus tareas")


def insert_task(rut: str, nombre: str, descripcion: str, hecha: str):
    task = {
        "nombre": nombre,
        "descripcion": descripcion,
        "hecha": hecha
    }
    data = {
        "rut": rut,
        "task": task
    }
    response = post(f'{URL}/tasks', json=data)
    status = response.status_code
    if status == 200:
        print("tarea insertada exitosamente")
    elif status == 400:
        print("no fue posible ingresar la tarea")
    else:
        print("no fue posible ingresar la tarea")
    return response

def update_task(rut: str, nombre: str, new_nombre: str, new_descripcion: str, new_hecha: str):
    new_task = {
        "new_nombre": new_nombre,
        "new_descripcion": new_descripcion,
        "new_hecha": new_hecha
    }
    data = {
        "rut": rut,
        "nombre": nombre, 
        "new_task": new_task
    }
    response = put(f'{URL}/tasks', json=data)
    status = response.status_code

    if status == 200:
        print("tarea insertada exitosamente")
    elif status == 404:
        print("tarea no encontrada")
    else:
        print("error al ingresar la tarea")

def delete_task(rut: str, nombre: str):
    data = {
        "rut": rut,
        "nombre": nombre, 
    }
    response = delete(f'{URL}/tasks', json=data)
    status = response.status_code

    if status == 200:
        print("Tarea eliminada exitosamente")
    elif status == 404:
        print("La tarea no fue encontrada")
    else:
        print("error al eliminar la tarea")

def validar_rut(rut):
    patron = r'^\d{7,8}[0-9kK]$'
    if re.match(patron, rut):
        return True
    else:
        return False

def pedir_rut():
    while True:
        rut = input("Ingrese su rut")
        if validar_rut(rut):
            return rut
        else:
            print("Ingrese un rut valido")

def pedir_opción():
    while True:
        try:
            return int(input("Ingrese una opcion: "))
        except:
            print("Ingrese una opcion valida")

def pedir_hecha():
    print("La tarea esta completada?")
    print("1) Si")
    print("2) No")
    while True:    
        opcion = pedir_opción()
        if opcion == 1:
            return "si"
        elif opcion == 2:
            return "no"
        else:
            print("opción incorrecta")
    

def print_task(task: dict):
    print("Nombre: " + task['nombre'] )
    print("Descripción: " + task['descripcion'] )
    print("hecha: " + task['hecha'] )

def print_list_tasks(lista_tasks: list):
    for task in lista_tasks:
        print_task(task)
    
def limpiar_consola():
    print("\033[H\033[J")

def bienvenida():
    print("¡Bienvenido al Sistema de Gestion de Tareas Personales!")
    print("")

def print_menu():
    print("Sub menú:")
    print("1) Crear tarea")
    print("2) Listar tareas")
    print("3) Actualizar una tarea")
    print("4) Eliminar una tarea")
    print("5) Cambiar de rut")
    print("6) Salir")

def menu():
    bienvenida()
    rut = pedir_rut()

    while True:
        print_menu()
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            # Crear tarea
            limpiar_consola()
            nombre = input("Ingrese el nombre de la tarea: ")
            descripcion = input("Ingrese una descripción: ")
            hecha = "no"
            insert_task(rut, nombre, descripcion, hecha)
        elif opcion == '2':
            # Listar tareas
            limpiar_consola()
            tasks = get_tasks(rut)
            print_list_tasks(tasks)
            
        elif opcion == '3':
            # Actualizar una tarea
            limpiar_consola()
            nombre = input("Ingrese nombre de la tarea a modificar: ")
            new_nombre = input("Ingrese el nuevo nombre: ")
            new_descripcion = input("Ingrese la nueva descripción: ")
            new_hecha = pedir_hecha()
            update_task(nombre, new_nombre, new_descripcion, new_hecha)
        elif opcion == '4':
            # Lógica para eliminar una tarea
            limpiar_consola()
            nombre = input("Ingrese nombre de la tarea a ELIMINAR: ")
            delete_task(rut, nombre)
        elif opcion == '5':
            # Lógica para cambiar de rut
            limpiar_consola()
            rut = pedir_rut()
            print("Rut cambiado exitosamente")
        elif opcion == '6':
            print("cerrando el programa......")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 6.")

def main():
    menu()

if __name__ == "__main__":
    main()
