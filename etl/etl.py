from extract import extract_api_meteorology, extract_api_exchangerate
from transform import alerta_climatica
from transform import alerta_tipo_cambio, indice_ivv
from typing import Dict, Any
from config.constants import CITIES

import json

# Cordenadas ciudades a monitorear


name_cities = list(CITIES.keys())

dict_meteorology = extract_api_meteorology(name_cities[0], CITIES["Nueva York"])
#print(dict_meteorology)
dict_finanzas = extract_api_exchangerate(CITIES["Nueva York"]["moneda"])
#print(dict_finanzas)
merged_dict = {**dict_meteorology, **dict_finanzas}
print(json.dumps(merged_dict, indent=4, ensure_ascii=False))

option = alerta_climatica(merged_dict)
print(f"Alerta climática: {option}")





