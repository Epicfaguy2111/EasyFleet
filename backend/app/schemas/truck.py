from typing import Optional
from pydantic import BaseModel


class DriverCreate(BaseModel):
    name: Optional[str] = None
    licence: Optional[str] = None
    phone: Optional[str] = None


class TruckCreate(BaseModel):
    name: str
    registration: str
    weight: float
    height: float
    length: float
    fuel: float
    driver: Optional[DriverCreate] = None


class TruckResponse(TruckCreate):
    id: int

    class Config:
        from_attributes = True