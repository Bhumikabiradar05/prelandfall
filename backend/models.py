from datetime import datetime
from pydantic import BaseModel, Field


class Bulletin(BaseModel):
    landfall_lat: float = 19.80
    landfall_lon: float = 85.82
    landfall_time: datetime = datetime(2019, 5, 3, 8, 0)
    max_wind_kmph: float = Field(175, ge=0)
    pressure_hpa: float = Field(932, ge=800, le=1100)
    track_points: list[list[float]] = [[18.9, 86.4], [19.4, 86.1], [19.8, 85.82], [20.3, 85.6]]
