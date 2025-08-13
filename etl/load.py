from extract import extract_api_meteorology, extract_api_exchangerate
from transform import alerta_climatica, alerta_tipo_cambio, indice_ivv  
from typing import Dict, Any, List

import json
import time

# Cordenadas ciudades a monitorear

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060, "moneda": "USD", "timezone": "America/New_York"},
    "Londres": {"lat": 51.5074, "lon": -0.1278, "moneda": "GBP", "timezone": "Europe/London"},
    "Tokio": {"lat": 35.6895, "lon": 139.6917, "moneda": "JPY", "timezone": "Asia/Tokyo"},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "moneda": "BRL", "timezone": "America/Sao_Paulo"},
    "Sídney": {"lat": -33.8688, "lon": 151.2093, "moneda": "AUD", "timezone": "Australia/Sydney"}
}

def load_data_apies_for_city(name_city: str, cities: Dict[str, Any]) -> Dict[str, Any]:

    dict_meteorology = extract_api_meteorology(name_city, cities[f"{name_city}"])

    dict_finanzas = extract_api_exchangerate(cities[f"{name_city}"]["moneda"])

    data_city = {**dict_meteorology, **dict_finanzas}

    data_complete = indice_ivv(alerta_tipo_cambio(data_city),alerta_climatica(data_city), data_city)

    return data_complete

def create_list_load_data_cities(cities: Dict[str, Any]) -> List:

    list_data_cities = []

    for j in range(2):
        for i in range(len(cities)):
            try:
                name_city = list(cities.keys())[i]
                data_city = load_data_apies_for_city(name_city, cities)
                list_data_cities.append(data_city)
            except Exception as e:
                print(f"No se pudo obtener datos para {name_city}: {e}")

    return list_data_cities

data_final = create_list_load_data_cities(cities)
print(json.dumps(data_final, indent=4, ensure_ascii=False))
    








