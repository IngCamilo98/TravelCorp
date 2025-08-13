import requests
import json
import time
from typing import Dict, Any
# Cordenadas ciudades a monitorear

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Tokio": {"lat": 35.6895, "lon": 139.6917},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Sídney": {"lat": -33.8688, "lon": 151.2093}
}

# ---------------------------------------------------------------
# Primera API 
# A. API Meteorológica - Open-Mete
# ---------------------------------------------------------------

def extract_api_meteorology() -> Dict[str, Any]:

    # URL con parámetros necesarios
    lat = 40.7128
    lon = -74.0060

    url_meteo = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,uv_index_max"
        f"&timezone=auto"
        f"&forecast_days=7"
    )
    try:
        response = requests.get(url_meteo, timeout=10)
        response.raise_for_status()  # Lanza error si status != 200
        data_meteo = response.json()
        # Validar que el JSON tiene los datos esperados
        if "current" not in data_meteo:
            raise ValueError("Respuesta incompleta: falta 'current' en la API")

        print("------------------------------------------------------------------")
        print("Datos obtenidos correctamente ✅\n")
        print("Ciudad = Nueva York")
        print("Ubicación:", data_meteo.get("latitude"), data_meteo.get("longitude"))
        print("Temperatura actual:", data_meteo["current"].get("temperature_2m"), "°C")
        print("Pronostico 7 dias:")
        print("------------------------------------------------------------------")
        # Extraer las listas de datos diarios
        fechas = data_meteo['daily']['time']
        temp_minimas = data_meteo['daily']['temperature_2m_min']
        temp_maximas = data_meteo['daily']['temperature_2m_max']
        probabilidad_precipitacion = data_meteo['daily']['precipitation_probability_max']
        indices_uv = data_meteo['daily']['uv_index_max']    
        # --- Imprimir día y pronóstico de temperatura ---
        print("--- Pronóstico de Temperatura ---")
        for i in range(len(fechas)):
            print(f"El pronóstico de temperatura para el {fechas[i]} es de {temp_minimas[i]}°C a {temp_maximas[i]}°C.")

        print("\n" + "="*40 + "\n")

        # --- Imprimir día y probabilidad de precipitación ---
        print("--- Probabilidad de Precipitación ---")
        for i in range(len(fechas)):
            print(f"La probabilidad de precipitación para el {fechas[i]} es del {probabilidad_precipitacion[i]}%.")
        
        print("\n" + "="*40 + "\n")

        # --- Imprimir día e índice UV ---
        print("--- Índice UV ---")
        for i in range(len(fechas)):
            print(f"El índice UV máximo para el {fechas[i]} es de {indices_uv[i]}.")    
        print("------------------------------------------------------------------")
        print("Viento actual:", data_meteo["current"].get("wind_speed_10m"), "km/h")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")
    return None

# ---------------------------------------------------------------
#   Segunda API
# B. API de Tipos de Cambio - ExchangeRate-API
# ---------------------------------------------------------------

def extract_api_exchangerate() -> dict:
    try:
        url_exchangerate = (f"https://api.exchangerate-api.com"
                            f"/v4"
                            f"/latest"
                            f"/USD"
                            )

        response = requests.get(url_exchangerate, timeout=10)
        response.raise_for_status()  # Lanza error si status != 200
        data_exchangerate = response.json()

        # 1. Conversión USD a monedas locales
        base_currency = data_exchangerate["base"]
        rates = data_exchangerate["rates"]

        print("### Conversión de USD a monedas locales 💵")
        print(f"La tasa base es de **1 {base_currency}**.\n")
        print("Aquí están algunas de las tasas de conversión más comunes:")
        
        # Ejemplos de monedas para mostrar
        currencies_to_show = ["EUR", "MXN", "COP", "JPY", "GBP"]
        for currency in currencies_to_show:
            if currency in rates:
                print(f"- **{currency}:** {rates[currency]:.2f}")
        

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")
    return None

# ---------------------------------------------------------------
#   Tercera API
# c. API time Zone - ExchangeRate-API
# ---------------------------------------------------------------

def extract_api_timezone() -> dict:

    ciudades = {
        "Nueva York": "America/New_York",
        "Londres": "Europe/London",
        "Tokio": "Asia/Tokyo",
        "São Paulo": "America/Sao_Paulo",
        "Sídney": "Australia/Sydney",
        "Bogotá": "America/Bogota"
    }

    def obtener_datos_ciudad(zona, reintentos=3, espera=2):
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
    return None


extract_api_meteorology()
#extract_api_exchangerate()
#extract_api_timezone()







