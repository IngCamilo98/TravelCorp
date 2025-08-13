import requests
import json
import time
from typing import Dict, Any
from datetime import datetime, timezone

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Tokio": {"lat": 35.6895, "lon": 139.6917},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Sídney": {"lat": -33.8688, "lon": 151.2093}
}

def get_format_timestamp(times_stamp: str) -> str:

    # 1. Convertir la cadena a un objeto datetime
    # Se usa strptime() para parsear la cadena con el formato correcto.
    # El formato "%Y-%m-%dT%H:%M" coincide con '2025-08-12T19:30'
    fecha_hora = datetime.fromisoformat(times_stamp)

    # 2. Agregar la zona horaria UTC
    # Se le dice al objeto datetime que está en la zona horaria UTC.
    # La "Z" en el formato ISO 8601 representa UTC.
    fecha_hora_utc = fecha_hora.replace(tzinfo=timezone.utc)

    # 3. Formatear el objeto datetime al formato ISO 8601
    # La función isoformat() lo hace automáticamente.
    timestamp_formateado = fecha_hora_utc.isoformat()

    # Imprimir el resultado final
    #print(f"Timestamp original: {times_stamp}")
    #print(f"Timestamp formateado (con Z): {timestamp_formateado}")

    return timestamp_formateado

def get_pronostico_7_dias(data_meteorology : Dict) -> Dict:

    fechas = data_meteorology['daily']['time']
    temp_minimas = data_meteorology['daily']['temperature_2m_min']
    temp_maximas = data_meteorology['daily']['temperature_2m_max']
    probabilidad_precipitacion = data_meteorology['daily']['precipitation_probability_max']

    # --- Combinar las listas en el formato deseado ---
    pronostico_7_dias = []

    # zip() itera sobre todas las listas en paralelo
    for fecha, t_max, t_min, prec in zip(fechas, temp_maximas, temp_minimas, probabilidad_precipitacion):
        dia = {
            "fecha": fecha,
            "temp_max": t_max,
            "temp_min": t_min,
            "precipitacion": prec
        }
        pronostico_7_dias.append(dia)

    return pronostico_7_dias

def extract_api_meteorology(name_city: str, city: Dict[str, Any]) -> Dict[str, Any]:

    lat = city["lat"]
    lon = city["lon"]

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
        data_meteorology = response.json()
        # Validar que el JSON tiene los datos esperados
        if "current" not in data_meteorology:
            raise ValueError("Respuesta incompleta: falta 'current' en la API")

        dict_meteorology = {
            "timestamp": get_format_timestamp(data_meteorology['current']['time']),
            "ciudad": name_city,
            "clima": {
                "temperatura_actual": data_meteorology['current']['temperature_2m'],
                "pronostico_7_dias": get_pronostico_7_dias,
                "precipitacion": data_meteorology['daily']['precipitation_probability_max'][0],
                "viento": data_meteorology['current']['wind_speed_10m'],
                "uv": data_meteorology['daily']['uv_index_max'] 
            }
        }

        # Usar json.dumps() con indent=4 para una salida formateada
        salida_legible = json.dumps(data_meteorology, indent=4)
        print(salida_legible)


    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")
    return None

extract_api_meteorology("Nueva York",cities["Nueva York"])