from etl.extract import extract_api_meteorology, extract_api_exchangerate
from etl.load import create_list_load_data_cities
#from dotenv import load_dotenv

# Cordenadas ciudades a monitorear

cities = {
    "Nueva York": {"lat": 40.7128, "lon": -74.0060, "moneda": "USD", "timezone": "America/New_York"},
    "Londres": {"lat": 51.5074, "lon": -0.1278, "moneda": "GBP", "timezone": "Europe/London"},
    "Tokio": {"lat": 35.6895, "lon": 139.6917, "moneda": "JPY", "timezone": "Asia/Tokyo"},
    "São Paulo": {"lat": -23.5505, "lon": -46.6333, "moneda": "BRL", "timezone": "America/Sao_Paulo"},
    "Sídney": {"lat": -33.8688, "lon": 151.2093, "moneda": "AUD", "timezone": "Australia/Sydney"}
}

# ---------------------------------------------------------------
# Cargar datos de las ciudades
# ---------------------------------------------------------------   

list_data_cities = create_list_load_data_cities(cities)

print(list_data_cities)

"""
load_dotenv()  # take environment variables

from alerts.email import send_email

send_email("...", "Test Email", "This is a test email sent from the script.")
"""


