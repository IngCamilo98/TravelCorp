import requests

# Cordenadas ciudades a monitorear

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060},
    "Londres": {"lat": 51.5074, "lon": -0.1278},
    "Tokio": {"lat": 35.6895, "lon": 139.6917},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333},
    "Sídney": {"lat": -33.8688, "lon": 151.2093}
}

# URL con parámetros necesarios

for city, coords in cities.items():
    lat = coords["lat"]
    lon = coords["lon"]

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,wind_speed_10m"
        f"&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza error si status != 200

        data = response.json()

        # Validar que el JSON tiene los datos esperados
        if "current" not in data:
            raise ValueError("Respuesta incompleta: falta 'current' en la API")
        print("------------------------------------------------------------------")
        print("Datos obtenidos correctamente ✅\n")
        print(f"Ciudad = {city}")
        print("📍 Ubicación:", data.get("latitude"), data.get("longitude"))
        print("🌡️ Temperatura actual:", data["current"].get("temperature_2m"), "°C")
        print("💨 Viento actual:", data["current"].get("wind_speed_10m"), "km/h")
        print("------------------------------------------------------------------")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión con la API: {e}")
    except ValueError as e:
        print(f"⚠️ Datos incompletos o formato inesperado: {e}")
    except Exception as e:
        print(f"🚨 Error inesperado: {e}")
