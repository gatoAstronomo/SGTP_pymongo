from requests import get, post, put, delete
from rut_chile import rut_chile

SERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def create_user(rut: str):
    data = {'rut': rut}    
    return post(f'{URL}/users', json=data)

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
    rut = "21.512.921-7"
    print(validar_rut(rut))
    print(rut_chile.format_capitalized_rut_with_dots(rut))
    """
    if validar_rut(rut):
        response = create_user(rut)
        print(response.json())
    else:
        print("Ingrese un rut valido")"""
    
    
    
    

if __name__ == "__main__":
    main()