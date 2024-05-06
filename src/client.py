from requests import get, post, put, delete
import re

ARSERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
ARSERVER_PORT = 8081
ARURL = f'http://{ARSERVER_IP}:{ARSERVER_PORT}'

def get_tasks(ARrut: str):
    ARdata = {'rut': ARrut}
    ARresponse = get(f'{ARURL}/tasks', json=ARdata)
    ARstatus = ARresponse.status_code

    if ARstatus == 200:
        return ARresponse.json()
    elif ARstatus == 404:
        return []
    else:
        print("Error al descargar sus tareas")
        return []

def insert_task(ARrut: str, ARnombreuser: str, ARcorreo: str, ARnombre: str, ARdescripcion: str, ARhecha: str):
    ARtask = {
        "nombre": ARnombre,
        "descripcion": ARdescripcion,
        "hecha": ARhecha
    }
    ARdata = {
        "rut": ARrut,
        "nombreuser": ARnombreuser,
        "correo": ARcorreo,
        "task": ARtask
    }
    ARresponse = post(f'{ARURL}/tasks', json=ARdata)
    ARstatus = ARresponse.status_code
    
    if ARstatus == 200:
        print("Tarea insertada exitosamente")
    elif ARstatus == 400:
        print("No fue posible ingresar la tarea")
        print("Ya existe una tarea con ese nombre")
    else:
        print("No fue posible ingresar la tarea")
    return ARresponse

def update_task(ARrut: str, ARnombre: str, ARnew_nombre: str, ARnew_descripcion: str, ARnew_hecha: str):
    ARnew_task = {
        "new_nombre": ARnew_nombre,
        "new_descripcion": ARnew_descripcion,
        "new_hecha": ARnew_hecha
    }
    ARdata = {
        "rut": ARrut,
        "nombre": ARnombre, 
        "new_task": ARnew_task
    }
    ARresponse = put(f'{ARURL}/tasks', json=ARdata)
    ARstatus = ARresponse.status_code

    if ARstatus == 200:
        print("Tarea actualizada exitosamente")
    elif ARstatus == 404:
        print("No fue posible encontrar la tarea")
    else:
        print("Error al ingresar la tarea")

def delete_task(ARrut: str, ARnombre: str):
    ARdata = {
        "rut": ARrut,
        "nombre": ARnombre, 
    }
    ARresponse = delete(f'{ARURL}/tasks', json=ARdata)
    ARstatus = ARresponse.status_code

    if ARstatus == 200:
        print("Tarea eliminada exitosamente")
    elif ARstatus == 404:
        print("No fue posible encontrar la tarea")
    else:
        print("Error al eliminar la tarea")

def get_user(ARrut: str):
    ARdata = {"rut": ARrut}
    ARresponse = get('http://44.197.32.169:8081/users', json=ARdata)
    ARstatus = ARresponse.status_code
    if ARstatus == 200:
        return ARresponse.json()
    elif ARstatus == 404:
        print("No fue posible encontrar su usuario")
    print("Error al pedir sus datos")

def create_user(ARrut: str, ARnombreuser: str, ARcorreo: str):
    ARdata = {
        'rut': ARrut,
        'nombreuser': ARnombreuser,
        'correo': ARcorreo
    }
    ARresponse = post(f'{ARURL}/users', json=ARdata)
    ARstatus = ARresponse.status_code
    if ARstatus == 200:
        print("El usuario fue creado exitosamente")
    elif ARstatus == 400:
        print("El usuario ya EXISTE")

def validar_rut(ARrut):
    ARpatron = r'^\d{7,8}[0-9kK]$'
    if re.match(ARpatron, ARrut):
        return True
    else:
        return False

def pedir_rut():
    while True:
        ARrut = input("Ingrese su rut: ")
        if validar_rut(ARrut):
            return ARrut
        else:
            print("Ingrese un rut valido")

def pedir_opción():
    while True:
        try:
            return int(input("Ingrese una opcion: "))
        except:
            print("Opción invalida")

def pedir_hecha():
    print("La tarea esta completada?")
    print("1) Si")
    print("2) No")
    while True:    
        ARopcion = input()
        if ARopcion == '1':
            return "si"
        elif ARopcion == '2':
            return "no"
        else:
            print("opción incorrecta")
    
def print_task(ARtask: dict):
    print("Nombre: " + ARtask['nombre'] )
    print("Descripción: " + ARtask['descripcion'] )
    print("hecha: " + ARtask['hecha'] )

def print_list_tasks(ARlista_tasks: list):
    if len(ARlista_tasks) == 0:
        print("No tiene ninguna tarea\n")
    for ARtask in ARlista_tasks:
        print_task(ARtask)
        print("")
    
def limpiar_consola():
    print("\033[H\033[J")

def bienvenida():
    print("¡Bienvenido al Sistema de Gestion de Tareas Personales!")
    print("")

def print_menu():
    print("")
    print("1) Crear tarea")
    print("2) Listar tareas")
    print("3) Actualizar una tarea")
    print("4) Eliminar una tarea")
    print("5) Cambiar de rut")
    print("6) Salir")

def menu():
    limpiar_consola()
    bienvenida()
    ARrut = pedir_rut()
    ARnombreuser = input("Ingrese su nombre: ")
    ARcorreo = input("Ingrese su correo: ")
    print("El rut ha sido ingresado exitosamente")

    while True:
        print_menu()
        ARopcion = pedir_opción()

        if ARopcion == 1:
            # Crear tarea
            limpiar_consola()
            ARnombre = input("Ingrese el nombre de la tarea: ")
            ARdescripcion = input("Ingrese una descripción: ")
            ARhecha = "no"
            insert_task(ARrut, ARnombreuser, ARcorreo, ARnombre, ARdescripcion, ARhecha)
        elif ARopcion == 2:
            # Listar tareas
            limpiar_consola()
            ARtasks = get_tasks(ARrut)
            print_list_tasks(ARtasks)
            
        elif ARopcion == 3:
            # Actualizar una tarea
            limpiar_consola()
            ARnombre = input("Ingrese nombre de la tarea a modificar: ")
            ARnew_nombre = input("Ingrese el nuevo nombre: ")
            ARnew_descripcion = input("Ingrese la nueva descripción: ")
            ARnew_hecha = pedir_hecha()
            update_task(ARrut, ARnombre, ARnew_nombre, ARnew_descripcion, ARnew_hecha)

        elif ARopcion == 4:
            # Lógica para eliminar una tarea
            limpiar_consola()
            ARnombre = input("Ingrese nombre de la tarea a ELIMINAR: ")
            delete_task(ARrut, ARnombre)

        elif ARopcion == 5:
            # Lógica para cambiar de rut
            limpiar_consola()
            ARrut = pedir_rut()
            print("Rut cambiado exitosamente")

        elif ARopcion == 6:
            print("Saliendo del programa......")
            break

        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 6.")

def main():
    menu()

if __name__ == "__main__":
    main()
    # ruts: 218474383
    