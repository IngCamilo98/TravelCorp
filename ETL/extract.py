import requests
import json
import time
from typing import Dict, Any
from datetime import datetime, timezone
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

def get_format_timestamp(times_stamp: str) -> str:
    """La función get_format_timestamp toma una cadena de fecha y hora (times_stamp) en formato ISO (por ejemplo, "2025-08-12T19:30") y la convierte en un objeto datetime con zona horaria UTC.
Luego, devuelve esa fecha y hora en formato ISO 8601, incluyendo la información de la zona horaria (+00:00 para UTC).

    Args:
        times_stamp (str): Dato timesstamp en formato string

    Returns:
        str: Dato timesstamp en formato ISO 8601 con zona horaria UTC
    """

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

    """La función get_pronostico_7_dias toma como entrada un diccionario con datos meteorológicos (de la API Open-Meteo) y construye una lista de diccionarios, cada uno representando el pronóstico diario para los próximos 7 días.

    Args:
        data_meteorology (Dict): datos meteorológicos (de la API Open-Meteo)

    Returns:
        _type_: Diccionario con el pronóstico de 7 días en el formato solicitado en los requerimientos.
    """

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

    """La función extract_api_meteorology consulta la API meteorológica Open-Meteo para una ciudad específica y devuelve un diccionario con información solicitado del clima en el formato de diccionario solicitado.

    Raises:
        ValueError: _description_
    
    Args:
        name_city (str): Nombre de la ciudad a buscar la información
        city (Dict[str, Any]): Diccionario con latitud y longitud de la ciudad

    Returns:
        _type_: Diccionario con la información del clima en el formato solicitado.
    """

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
                "pronostico_7_dias": get_pronostico_7_dias(data_meteorology),
                "precipitacion": data_meteorology['daily']['precipitation_probability_max'][0],
                "viento": data_meteorology['current']['wind_speed_10m'],
                "uv": data_meteorology['daily']['uv_index_max'][0]
            }
        }

        print(json.dumps(dict_meteorology, indent=4))
        return dict_meteorology

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


extract_api_meteorology("Nueva York",cities["Nueva York"])
#extract_api_exchangerate()
#extract_api_timezone()







