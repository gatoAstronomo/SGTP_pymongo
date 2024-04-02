from requests import get, post, put, delete

SERVER_IP = "44.197.32.169"
# SERVER_IP = "localhost"
SERVER_PORT = 8081
URL = f'http://{SERVER_IP}:{SERVER_PORT}'

def create_user(rut: str):
    data = {'rut': rut}
    response = post(f'{URL}/users', json=data)
    
    return response

def main():
    response = create_user("este_rut_prueba")
    print(response.json)
    
    
    

if __name__ == "__main__":
    main()