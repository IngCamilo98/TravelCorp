import requests
import json
import time
from typing import Dict, Any
from datetime import datetime, timezone

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060, "currency": "USD"},
    "Londres": {"lat": 51.5074, "lon": -0.1278, "currency": "GBP"},
    "Tokio": {"lat": 35.6895, "lon": 139.6917, "currency": "JPY"},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "currency": "BRL"},
    "Sídney": {"lat": -33.8688, "lon": 151.2093, "currency": "AUD"}
}

def extract_api_exchangerate(city: Dict[str, Any]) -> Dict:

    currency = city["currency"]

    try:
        url_exchangerate = (f"https://api.exchangerate-api.com"
                            f"/v4"
                            f"/latest"
                            f"/{currency}"
                            )

        response = requests.get(url_exchangerate, timeout=10)
        response.raise_for_status()  # Lanza error si status != 200
        data_exchangerate = response.json()

        print(data_exchangerate)
        

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")

    return None

extract_api_exchangerate(cities["Nueva York"])