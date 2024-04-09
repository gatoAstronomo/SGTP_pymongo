from requests import get, post, put, delete
from rut_chile import rut_chile

SERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def insert_task(rut: str, nombre: str, descripcion: str, hecha: str):
    task = {
        "nombre": nombre,
        "descripcion": descripcion,
        "hecha": "false"
    }
    data = {
        "rut": rut,
        "task": task
    }
    
    return post(f'{URL}/tasks', json=data)





def extraer_numeros(cadena):
    numeros_str = ""
    for caracter in cadena:
        if '0' <= caracter <= '9':  # Verifica si el carácter es un dígito numérico
            numeros_str += caracter
    return numeros_str

def validar_rut(rut: str):
    rut = extraer_numeros(rut)
    
    # Longitud correcta
    if len(rut) != 9:
        return False
    
    try:
        return rut_chile.is_valid_rut(rut)
    except:
        return False
    
def main():
    rut = "22969404"
    rut = rut + rut_chile.get_verification_digit(rut)

    if validar_rut(rut):
        response = insert_task(rut, "Hoy dia", "Lavar la ropa", "no")
        print(response.json())
    else:
        print("Ingrese un rut valido")
    

if __name__ == "__main__":
    main()