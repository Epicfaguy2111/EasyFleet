from datetime import date
from typing import Optional
from pydantic import BaseModel


class TruckCreate(BaseModel):
    name: str = ""
    fleet_number: str
    registration: str
    vin: str
    make: str
    model: str
    year: int
    fuel_type: str = "diesel"
    gross_vehicle_weight_kg: float = 0.0
    payload_capacity_kg: float = 0.0
    engine_power_kw: float = 0.0
    fuel_tank_capacity_l: float = 0.0
    axle_count: int = 2
    vehicle_type: str = "single_rigid"
    length_m: float = 0.0
    width_m: float = 0.0
    height_m: float = 0.0
    odometer_km: float = 0.0
    status: str = "active"
    last_service_date: Optional[date] = None
    next_service_due_km: Optional[float] = None


class TruckResponse(TruckCreate):
    id: int

    class Config:
        from_attributes = True