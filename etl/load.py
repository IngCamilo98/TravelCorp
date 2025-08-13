from extract import extract_api_meteorology, extract_api_exchangerate
from transform import alerta_climatica, alerta_tipo_cambio, indice_ivv  
from typing import Dict, Any    

import json

# Cordenadas ciudades a monitorear

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060, "moneda": "USD", "timezone": "America/New_York"},
    "Londres": {"lat": 51.5074, "lon": -0.1278, "moneda": "GBP", "timezone": "Europe/London"},
    "Tokio": {"lat": 35.6895, "lon": 139.6917, "moneda": "JPY", "timezone": "Asia/Tokyo"},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "moneda": "BRL", "timezone": "America/Sao_Paulo"},
    "Sídney": {"lat": -33.8688, "lon": 151.2093, "moneda": "AUD", "timezone": "Australia/Sydney"}
}

name_cities = list(cities.keys())

dict_meteorology = extract_api_meteorology(name_cities[0], cities["Nueva York"])

dict_finanzas = extract_api_exchangerate(cities["Nueva York"]["moneda"])

data_city = {**dict_meteorology, **dict_finanzas}

data_complete = indice_ivv(alerta_tipo_cambio(data_city),alerta_climatica(data_city), data_city)


print(json.dumps(data_complete, indent=4, ensure_ascii=False))










