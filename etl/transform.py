from typing import Dict, Any


def alerta_climatica(info_city: Dict[str, Any]) -> Dict[str, Any]:
    if (info_city["clima"]["temperatura_actual"] > 35 or info_city["clima"]["temperatura_actual"] < 0) and (
            info_city["clima"]["precipitacion"] > 70) and (info_city["clima"]["viento"] > 50):
        return {
            "tipo": "CLIMA",
            "severidad": "ALTA",
            "mensaje": "Posibilidad de lluviias a mas del 70%"
        }
    return {
        "tipo": "CLIMA",
        "severidad": "BAJA",
        "mensaje": "Los parametros estan dentro de lo establecido"
    }


def alerta_tipo_cambio(info_city: Dict[str, Any]) -> Dict[str, Any]:
    if (info_city["variacion_diaria"] > 3) and (info_city["tendencia_5_dias"] != 'Estable'):
        return {
            "tipo": "CAMBIO",
            "severidad": "ALTA",
            "mensaje": "La variacion diaria esta por encima del 3 prociento y la tendencia de los ultimos dias no es estable"
        }
    return {
        "tipo": "CAMBIO",
        "severidad": "BAJA",
        "mensaje": "Los parametros estan dentro de lo establecido"
    }


def indice_ivv(alerta_tipo_cambio: Dict[str, Any], alerta_climatica: Dict[str, Any], info_city: Dict[str, Any]) -> Dict[
    str, Any]:
    contador_alerta_climatica = 0

    if (alerta_climatica["severidad"] == "ALTA"):
        contador_alerta_climatica += 1

    if (alerta_tipo_cambio["severidad"] == "ALTA"):
        contador_alerta_cambio = 50
    else:
        contador_alerta_cambio = 100

    clima_score = 100 - (contador_alerta_climatica * 25)
    cambio_score = contador_alerta_cambio
    uv_score = 0

    if (info_city["clima"]["uv"] < 6):
        uv_score = 100
    elif (info_city["clima"]["uv"] > 6) and (info_city["clima"]["uv"] < 8):
        uv_score = 75
    elif (info_city["clima"]["uv"] > 8):
        uv_score = 50

    indice_ivv = (clima_score * 0.4) + (cambio_score * 0.3) + (uv_score * 0.3)

    componentes_ivv = {
        "componentes_ivv": {
            "clima_score": clima_score,
            "cambio_score": cambio_score,
            "uv_sore": uv_score
        },
        "indice_ivv": indice_ivv
    }

    dict_final = info_city | componentes_ivv
    dict_final["alertas"] = [alerta_tipo_cambio, alerta_climatica]

    return dict_final
