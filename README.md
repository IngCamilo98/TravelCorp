# TravelCorp ETL

TravelCorp es un pipeline ETL (Extract, Transform, Load) que recopila, procesa y almacena información meteorológica y financiera de varias ciudades del mundo. El sistema genera alertas automáticas y notificaciones por email en caso de condiciones climáticas extremas o variaciones significativas en el tipo de cambio.

## Características principales
- Extracción de datos meteorológicos (Open-Meteo) y financieros (ExchangeRate-API) para ciudades configuradas.
- Procesamiento y transformación de datos para generar alertas y un Índice de Viabilidad de Viaje (IVV).
- Almacenamiento de resultados en un archivo `output.json` de forma acumulativa.
- Envío de emails automáticos ante alertas de severidad alta.
- Ejecución periódica y logs estructurados con timestamps.

## Estructura del proyecto
```
TravelCorp/
├── main.py                # Script principal, ejecuta el pipeline ETL periódicamente
├── scheduler.py           # (Opcional) Lógica de scheduling
├── config/                # Configuración general y constantes
│   ├── constants.py       # Ciudades y parámetros principales
│   ├── settings.py        # Configuración de tiempos y parámetros globales
│   └── ...
├── etl/                   # Lógica ETL
│   ├── extract.py         # Extracción de datos de APIs externas
│   ├── transform.py       # Generación de alertas y cálculo de IVV
│   ├── load.py            # Integración de datos y disparo de emails
│   └── ...
├── models/                # Modelos de datos
│   └── open_meteo_response.py
├── utils/                 # Utilidades auxiliares
│   └── email.py           # Envío de emails
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Este archivo
```

## Instalación
1. Clona el repositorio y entra en la carpeta del proyecto.
2. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración
1. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables para el envío de emails:
   ```env
   EMAIL_ADDRESS=tu_email@gmail.com
   EMAIL_APP_PASSWORD=tu_contraseña_de_aplicación
   ```
2. (Opcional) Ajusta las ciudades y parámetros en `config/constants.py` y `config/settings.py`.

## Ejecución
Para iniciar el pipeline ETL de forma continua:
```bash
python main.py
```
Los resultados se almacenarán en `output.json` y se enviarán emails ante alertas de severidad alta.

## APIs utilizadas
- **Open-Meteo**: Datos meteorológicos diarios y actuales.
- **ExchangeRate-API**: Tipos de cambio de monedas respecto al USD.

## Alertas y notificaciones
El sistema genera alertas automáticas cuando:
- Hay condiciones climáticas extremas (temperaturas fuera de rango, alta precipitación, viento fuerte).
- Se detectan variaciones significativas en el tipo de cambio.
Las alertas de severidad alta disparan un email automático al destinatario configurado.

## Dependencias principales
- `requests`
- `python-dotenv`
- `smtplib` (incluido en la librería estándar)


