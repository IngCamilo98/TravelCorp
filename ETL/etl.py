import requests
import json

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

# ---------------------------------------------------------------
#   Segunda API
# B. API de Tipos de Cambio - ExchangeRate-API
# ---------------------------------------------------------------

