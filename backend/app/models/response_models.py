from pydantic import BaseModel
from typing import List


class OptimizeRouteResponse(BaseModel):
    optimized_order: List[int]

    total_distance_km: float

    total_duration_minutes: float

    geometry: str

    ordered_stops: List[int]