from pydantic import BaseModel, Field
from typing import List


class Location(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class OptimizeRouteRequest(BaseModel):
    depot: Location
    stops: List[Location]