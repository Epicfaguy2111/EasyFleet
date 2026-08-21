from datetime import date
from typing import Optional
from pydantic import BaseModel


class TruckCreate(BaseModel):
    name: str
    fleet_number: str
    registration: str
    vin: str
    make: str
    model: str
    year: int
    fuel_type: str
    vehicle_type: str
    axles: int
    engine_power: float
    weight: float
    payload: float
    fuel: float
    length: float
    width: float
    height: float
    odometer: float
    status: str
    last_service_date: Optional[date] = None
    next_service_km: Optional[float] = None


class TruckResponse(TruckCreate):
    id: int

    class Config:
        from_attributes = True