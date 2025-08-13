import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
import logging
import requests

from models.open_meteo_response import WeatherData


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

    return {"pronostico_7_dias": pronostico_7_dias}


def extract_api_meteorology(name_city: str, city: Dict[str, Any], retry: bool = True, max_retries: int = 2) -> Dict[
    str, Any]:
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
    logging.info(f"{url_meteo=}")

    while retry and max_retries > 0:
        try:
            response = requests.get(url_meteo, timeout=30)
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
            logging.error(f"❌ Error de conexión con la API: {e}")
        except ValueError as e:
            logging.warning(f"⚠️ Datos incompletos o formato inesperado: {e}")
        except Exception as e:
            logging.error(f"🚨 Error inesperado: {e}")
        retry -= 1
    raise Exception("❌ No se pudo obtener datos de la API meteorológica después de varios intentos.")


# ---------------------------------------------------------------
#   Segunda API
# B. API de Tipos de Cambio - ExchangeRate-API
# ---------------------------------------------------------------

def extract_api_exchangerate(city_currency: str, retry: bool = True, max_retries: int = 2) -> Dict[str, Any]:
    """La función extract_api_exchangerate consulta la API ExchangeRate-API para obtener información financiera sobre
    el tipo de cambio de una moneda específica respecto al dólar estadounidense (USD) y lo transfomra en un
    diccionario con los requerimints solicitados.

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
    while retry and max_retries > 0:
        try:
            response = requests.get(url_exchangerate, timeout=30)
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
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Error de conexión con la API: {e}")
        max_retries -= 1
    raise Exception("❌ No se pudo obtener datos de la API de tipos de cambio después de varios intentos.")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
