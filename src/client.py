from requests import get, post, put, delete

SERVER_IP = "44.197.32.169"
SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def create_user(rut: str):
    data = {'rut': '12341234'}
    response = post(f'{URL}/users', json=data)
    
    return response

def main():
    create_user("este_rut_prueba")
    
    

if __name__ == "__main__":
    main()