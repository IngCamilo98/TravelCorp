from typing import Dict, Any

def alerta_climatica(info_city: Dict[str, Any]) -> bool:
    
    print(info_city["clima"]["temperatura_actual"])
    if info_city["clima"]["temperatura_actual"] > 35 | info_city["clima"]["temperatura_actual"] < 0:
        return True
    elif info_city["clima"]["temperatura_actual"] < 0:
        return True
    else:
        return False

    return None

def alerta_tipo_cambio(info_city: Dict[str, Any]) -> bool:

    return None

def indice_ivv():

    return None

