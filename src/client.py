from requests import get, post, put, delete
from rut_chile import rut_chile

SERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def create_user(rut: str):
    data = {'rut': rut}    
    return post(f'{URL}/users', json=data)

def main():
    rut = "85742345"
    if rut_chile.is_valid_rut(rut):
        response = create_user(rut)
        print(response.json())
    else:
        print("Ingrese un rut valido")
    
    
    
    

if __name__ == "__main__":
    main()