import requests
import json
import time
from typing import Dict, Any
from datetime import datetime, timezone
from datetime import timedelta
import requests
import json
import random
from datetime import datetime, timedelta

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060, "currency": "USD"},
    "Londres": {"lat": 51.5074, "lon": -0.1278, "currency": "GBP"},
    "Tokio": {"lat": 35.6895, "lon": 139.6917, "currency": "JPY"},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "currency": "BRL"},
    "Sídney": {"lat": -33.8688, "lon": 151.2093, "currency": "AUD"}
}

def get_5days_history() -> Dict[str, Any]:
    

    return None

def extract_api_exchangerate(city_currency: str)->Dict[str, Any]:
    
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
        "tipo_de_cambio_actual":rates[city_currency],
        "variacion_diaria": average_variation,
        "tendencia_5_dias": tendencia,
    }


    return finanzas

finanzas = extract_api_exchangerate("BRL")
pretty_json = json.dumps(finanzas, indent=4)
print(pretty_json)
