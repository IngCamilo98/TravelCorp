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
    
    base_currency = data_exchangerate["base"]
    rates = data_exchangerate["rates"]

    rate_currency = rates[city_currency]
    print(rate_currency)

    

    return None



def mientras():

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
        currencies_to_show = ["USD", "GBP", "JPY", "BRL", "AUD"]
        
        for currency in currencies_to_show:
            if currency in rates:
                print(f"- **{currency}:** {rates[currency]:.2f}")

        # 2. Histórico últimos 5 días (simulado)
        print("\n" + "---" + "\n")
        print("### Histórico de los últimos 5 días (Simulado) 📈")

        today_rate = rates.get("BRL")
        today_date_str = data_exchangerate["date"]

        if today_rate and today_date_str:
            print(f"Simulación del tipo de cambio USD a BRL para los últimos 5 días:\n")
            
            today = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            current_rate = today_rate

            print("| Fecha      | Tasa de Cambio (Simulada) | Variación |")
            print("| :--------- | :------------------------ | :---: |")

            # Generar datos simulados para los últimos 5 días
            for i in range(5):
                date = today - timedelta(days=i)
                # Calcular una variación aleatoria entre -2% y +2%
                variation = random.uniform(-0.02, 0.02)

                # Ajustar la tasa para el día anterior (simulación inversa)
                if i > 0:
                    previous_rate = current_rate / (1 + variation)
                    current_rate = previous_rate
                    
                variation_percent = f"{variation * 100:+.2f}%"
                
                print(f"| {date.strftime('%Y-%m-%d')} | {current_rate:.2f} | {variation_percent} |")




        else:
            print("⚠️ No se pudo simular el historial, faltan datos de la tasa de cambio o la fecha.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")

    return None

extract_api_exchangerate("BRL")