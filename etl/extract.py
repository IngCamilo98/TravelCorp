import random
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

import requests

from config.constants import CITIES
from models.open_meteo_response import WeatherData
from pydantic import ValidationError



# ---------------------------------------------------------------
# Primera API 
# A. API Meteorológica - Open-Mete
# ---------------------------------------------------------------

def get_format_timestamp(times_stamp: str) -> str:
    """La función get_format_timestamp toma una cadena de fecha y hora (times_stamp) en formato ISO (por ejemplo,
    "2025-08-12T19:30") y la convierte en un objeto datetime con zona horaria UTC.
    Luego, devuelve esa fecha y hora en formato ISO 8601, incluyendo la información de la zona horaria (+00:00 para UTC).

    Args:
        times_stamp (str): Dato timesstamp en formato string

    Returns:
        str: Dato timesstamp en formato ISO 8601 con zona horaria UTC
    """
    fecha_hora = datetime.fromisoformat(times_stamp)
    fecha_hora_utc = fecha_hora.replace(tzinfo=timezone.utc)
    timestamp_formateado = fecha_hora_utc.isoformat()

    return timestamp_formateado


def get_pronostico_siete_dias(data_meteorology: Dict[str, Any]) -> Dict:
    """La función get_pronostico_siete_dias toma como entrada un diccionario con datos meteorológicos (de la API Open-Meteo)
     y construye una lista de diccionarios, cada uno representando el pronóstico diario para los próximos 7 días.

    Args:
        data_meteorology (Dict[str, Any]): datos meteorológicos (de la API Open-Meteo)

    Returns:
        _type_: Diccionario con el pronóstico de 7 días en el formato solicitado en los requerimientos.
    """

    data_meteorology = WeatherData(**data_meteorology)
    fechas = data_meteorology.daily.time
    temp_minimas = data_meteorology.daily.temperature_2m_min
    temp_maximas = data_meteorology.daily.temperature_2m_max
    probabilidad_precipitacion = data_meteorology.daily.precipitation_probability_max

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
                "pronostico_7_dias": get_pronostico_siete_dias(data_meteorology),
                "precipitacion": data_meteorology['daily']['precipitation_probability_max'][0],
                "viento": data_meteorology['current']['wind_speed_10m'],
                "uv": data_meteorology['daily']['uv_index_max'][0]
            }
        }

        return dict_meteorology

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValidationError as e:
        print(f"⚠️ Error de validación de datos: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")

    return None


# ---------------------------------------------------------------
#   Segunda API
# B. API de Tipos de Cambio - ExchangeRate-API
# ---------------------------------------------------------------

def extract_api_exchangerate(city_currency: str) -> Dict[str, Any]:
    """La función extract_api_exchangerate consulta la API ExchangeRate-API para obtener información financiera sobre
    el tipo de cambio de una moneda específica respecto al dólar estadounidense (USD) y lo transfomra en un diccionario
    con los requerimints solicitados.

    Args:
        city_currency (str): Se requiere la nomenclatura de la moneda a consultar, por ejemplo: "BRL" para el Real Brasileño.

    Returns:
        Dict[str, Any]: se retorno el diccionario con la información financiera solicitada.
    """

    # URL de la API de ExchangeRate-API
    url_exchangerate = (f"https://api.exchangerate-api.com"
                        f"/v4"
                        f"/latest"
                        f"/USD"
                        )

    response = requests.get(url_exchangerate, timeout=10)
    response.raise_for_status()  # Lanza error si status != 200
    data_exchangerate = response.json()

    # 1. tipo_de_cambio_actual USD/Moneda
    rates = data_exchangerate["rates"]

    # 2. Tendecia de los últimos 5 días
    today_rate_brl = data_exchangerate["rates"][city_currency]
    today_date_str = data_exchangerate["date"]
    today = datetime.strptime(today_date_str, "%Y-%m-%d").date()

    current_rate = today_rate_brl
    historical_variations = []
    historical_data = []

    # Generar datos simulados para los últimos 5 días
    for i in range(5):
        date = today - timedelta(days=i)
        variation_percent = random.uniform(-2, 2)
        historical_variations.append(variation_percent)

        # La tasa anterior se calcula a partir de la actual y la variación simulada
        previous_rate = current_rate / (1 + (variation_percent / 100))
        current_rate = previous_rate

    # Calcular el promedio de las variaciones para la tendencia
    average_variation = sum(historical_variations) / len(historical_variations)

    if average_variation <= 1.5:
        tendencia = "Estable"
    else:
        tendencia = "Volátil"

    finanzas = {
        "tipo_de_cambio_actual": rates[city_currency],
        "variacion_diaria": average_variation,
        "tendencia_5_dias": tendencia,
    }

    return finanzas


# ---------------------------------------------------------------
#   Tercera API
# c. API time Zone - ExchangeRate-API
# ---------------------------------------------------------------

def extract_api_timezone() -> None:
    """La función extract_api_timezone consulta la API worldtimeapi.org para obtener la hora local y la diferencia horaria con Bogotá para varias ciudades.
    """

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


# ---------------------------------------------------------------
# Cuarto Indices
# ---------------------------------------------------------------

dict_meteorology = extract_api_meteorology("Nueva York", CITIES["Nueva York"])
# print(dict_meteorology)

dict_finanzas = extract_api_exchangerate("BRL")
# pretty_json = json.dumps(finanzas, indent=4)
# print(pretty_json)

merged_dict = {**dict_meteorology, **dict_finanzas}

# print(json.dumps(merged_dict, indent=4, ensure_ascii=False))
