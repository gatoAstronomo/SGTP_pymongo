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

def existe_rut(rut: str):
    data = {'rut': rut}
    response = get(f'{URL}/ruts', json=data)
    status = response.status_code

    if status == 200:
        return True
    elif status == 400:
        return False
    else:
        return False

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
            return int(input("Ingrese una opcion"))
        except:
            print("Ingrese una opcion valida")
    
def main():
    rut = "21345404k"
    

    if validar_rut(rut):
        for x in range(7):
            delete_task(rut,"Tarea1")
    else:
        print("Ingrese un rut valido")
    

if __name__ == "__main__":
    main()