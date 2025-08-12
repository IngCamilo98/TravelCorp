import requests
import time

ciudades = {
    "Nueva York": "America/New_York",
    "Londres": "Europe/London",
    "Tokio": "Asia/Tokyo",
    "São Paulo": "America/Sao_Paulo",
    "Sídney": "Australia/Sydney",
    "Bogotá": "America/Bogota"
}

def obtener_datos_ciudad(zona, reintentos=5, espera=2):
    for intento in range(reintentos):
        try:
            url = f"http://worldtimeapi.org/api/timezone/{zona}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error {response.status_code} para {zona}")
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión para {zona}: {e}")
            time.sleep(espera)
    return None  # Si no se logra obtener respuesta

# Primero obtenemos Bogotá
datos_bogota = obtener_datos_ciudad(ciudades["Bogotá"])
if not datos_bogota:
    print("No se pudo obtener la hora de Bogotá. Abortando...")
    exit()

offset_bogota = datos_bogota["utc_offset"]

print("\n--- Hora local y diferencia horaria con Bogotá ---")
for ciudad, zona in ciudades.items():
    datos = obtener_datos_ciudad(zona)
    if datos:
        hora_local = datos["datetime"]
        offset_ciudad = datos["utc_offset"]

        dif_horas = int(offset_ciudad.split(":")[0]) - int(offset_bogota.split(":")[0])

        print(f"\nCiudad: {ciudad}")
        print(f"Hora local: {hora_local}")
        print(f"Diferencia con Bogotá: {dif_horas} horas")
    else:
        print(f"No se pudo obtener datos para {ciudad}")
