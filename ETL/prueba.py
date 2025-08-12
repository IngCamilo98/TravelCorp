# Intenta hacer la solicitud usando http://
import requests

try:
    response = requests.get('http://worldtimeapi.org/api/timezone/America/Bogota', timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("Conexión exitosa. Datos de la API:", data)
    else:
        print(f"Error en la respuesta: Código de estado {response.status_code}")

except requests.exceptions.ConnectionError as e:
    print(f"Error de conexión: {e}")