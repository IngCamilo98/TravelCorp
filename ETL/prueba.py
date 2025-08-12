import requests
import time

url = 'http://worldtimeapi.org/api/timezone/America/Bogota'
max_reintentos = 5
espera_segundos = 3

for intento in range(1, max_reintentos + 1):
    try:
        print(f"Intento {intento} de {max_reintentos}...")
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print("Conexión exitosa. Datos de la API:", data)
            break
        else:
            print(f"Error en la respuesta: Código de estado {response.status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión: {e}")
        if intento < max_reintentos:
            print(f"Reintentando en {espera_segundos} segundos...")
            time.sleep(espera_segundos)
        else:
            print("Se agotaron los intentos. No se pudo conectar a la API.")
