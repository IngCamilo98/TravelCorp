import os
from typing import Dict, Any

from utils.email import send_email
from .extract import extract_api_meteorology, extract_api_exchangerate
from .transform import alerta_climatica, alerta_tipo_cambio, indice_ivv


def send_email_for_alerts(data: Dict[str, Any]) -> None:
    notify_to = os.getenv("NOTIFY_TO").split(",") if os.getenv("NOTIFY_TO") else []
    for key, value in data.items():
        for alerta in value.get("alertas", []):
            if alerta.get("severidad") == "ALTA":
                for email in notify_to:
                    send_email(email, f"[ALERTA] {key} - {alerta['tipo']}",
                               f"Hubo una alerta de severidad alta en {key} relacionada con {alerta['tipo']}. Detalles: {alerta['mensaje']}")


def load_data_apies_for_city(name_city: str, city: Dict[str, Any]) -> Dict[str, Any]:
    dict_meteorology = extract_api_meteorology(name_city, city)
    dict_finanzas = extract_api_exchangerate(city["moneda"])
    data_city = {**dict_meteorology, **dict_finanzas}
    data_complete = indice_ivv(alerta_tipo_cambio(data_city), alerta_climatica(data_city), data_city)
    return data_complete


def create_list_load_data_cities(cities: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    cities_information: Dict[str, Dict[str, Any]] = {}
    for key, value in cities.items():
        cities_information[key] = load_data_apies_for_city(key, value)
    send_email_for_alerts(cities_information)
    return cities_information
