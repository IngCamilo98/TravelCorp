from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class CurrentUnits(BaseModel):
    time: str
    interval: str
    temperature_2m: str
    wind_speed_10m: str


class Current(BaseModel):
    time: datetime
    interval: int
    temperature_2m: float
    wind_speed_10m: float


class DailyUnits(BaseModel):
    time: str
    temperature_2m_max: str
    temperature_2m_min: str
    precipitation_probability_max: str
    uv_index_max: str


class Daily(BaseModel):
    time: List[date]
    temperature_2m_max: List[float]
    temperature_2m_min: List[float]
    precipitation_probability_max: List[int]
    uv_index_max: List[float]


class WeatherData(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_units: CurrentUnits
    current: Current
    daily_units: DailyUnits
    daily: Daily
