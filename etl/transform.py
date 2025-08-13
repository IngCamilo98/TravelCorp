from typing import Dict, Any

def alerta_climatica(info_city: Dict[str, Any]) -> int:
    
    print(info_city["clima"]["temperatura_actual"])
    print(info_city["clima"]["precipitacion"])
    print(info_city["clima"]["viento"])

    if (info_city["clima"]["temperatura_actual"] > 35 or info_city["clima"]["temperatura_actual"]<0) and (info_city["clima"]["precipitacion"]>70) and (info_city["clima"]["viento"]> 50):

        return 1
    else:
        return 0

def alerta_tipo_cambio(info_city: Dict[str, Any]) -> int:

    print(info_city["variacion_diaria"])
    print(info_city["tendencia_5_dias"])

    if (info_city["variacion_diaria"] > 3) and (info_city["tendencia_5_dias"] != 'Estable'):
        return 1
    else:
        return 0

def indice_ivv(alerta_tipo_cambio: int, alerta_climatica: int, info_city: Dict[str, Any]) -> str:

    clima_score = 100 - (alerta_climatica * 25)
    cambio_score = 0

    if alerta_tipo_cambio == 1:
        cambio_score = 50
    else:
        cambio_score = 100


    uv_score = 0

    if info_city["uv"] < 6:
        uv_score = 100
    elif info_city["uv"] >= 6 and info_city["uv"] <= 8:
        uv_score = 75
    elif info_city["uv"] > 8:
        uv_score = 50
    
    ivv = (clima_score * 0.4) + (cambio_score*0.3) + (uv_score*0.3)

    return ivv

