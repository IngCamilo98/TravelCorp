from typing import Dict, Any

def alerta_climatica(info_city: Dict[str, Any]) -> Dict[str, Any]:

    alerta_climatica = {}

    if (info_city["clima"]["temperatura_actual"] > 35 or info_city["clima"]["temperatura_actual"]<0) and (info_city["clima"]["precipitacion"]>70) and (info_city["clima"]["viento"]> 50):
        alerta_climatica = {
            "alertas":{
            "tipo": "CLIMA",
            "severidad":"ALTA",
            "mensaje":"Posibilidad de lluviias a mas del 70%"
            }
        }
        return alerta_climatica
    else:
        alerta_climatica = {
            "alertas":{
            "tipo": "CLIMA",
            "severidad":"BAJA",
            "mensaje":"Los parametros estab dentro de lo establecido"
            }
        }        
        return alerta_climatica

def alerta_tipo_cambio(info_city: Dict[str, Any]) -> Dict[str, Any]:

    alerta_tipo_cambio = {}
    if (info_city["variacion_diaria"] > 3) and (info_city["tendencia_5_dias"] != 'Estable'):
        alerta_tipo_cambio = {
            "alertas":{
            "tipo": "CAMBIO",
            "severidad":"ALTA",
            "mensaje":"La variacion diaria esta por encima del 3 prociento y la tendencia de los ultimos dias no es estable" 
            }           
        }
        return alerta_tipo_cambio
    else:
        alerta_tipo_cambio = {
            "alertas":{
            "tipo": "CAMBIO",
            "severidad":"BAJA",
            "mensaje":"Los parametros estan dentro de lo establecido"   
            }         
        }
        return alerta_tipo_cambio

def indice_ivv(alerta_tipo_cambio: Dict[str, Any], alerta_climatica: Dict[str, Any], info_city: Dict[str, Any]) -> Dict[str, Any]:

    cont_alerta_climatica = 0
    cont_alert_cambio = 0

    if (alerta_climatica["alertas"]["severidad"] == "ALTA"):
        cont_alerta_climatica += 1

    if (alerta_tipo_cambio["alertas"]["severidad"]=="ALTA"):
        cont_alert_cambio = 50
    else:
        cont_alert_cambio = 100


    clima_score = 100 - (cont_alerta_climatica * 25)
    cambio_score = cont_alert_cambio
    uv_score = 0

    if (info_city["clima"]["uv"]<6):
        uv_score = 100
    elif (info_city["clima"]["uv"]>6) and (info_city["clima"]["uv"]<8):
        uv_score = 75
    elif (info_city["clima"]["uv"]>8):
        uv_score = 50

    indice_ivv = (clima_score * 0.4) + (cambio_score*0.3) + (uv_score*0.3)

    componentes_ivv = {
        "componentes_ivv":{
            "clima_score":clima_score,
            "cambio_score":cambio_score,
            "uv_sore":uv_score
        },
        "indice_ivv":indice_ivv
    }

    dict_final = {**info_city, **alerta_tipo_cambio, **alerta_climatica, **componentes_ivv}



    return dict_final

