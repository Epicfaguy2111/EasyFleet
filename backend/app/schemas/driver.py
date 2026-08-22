from typing import List
from pydantic import BaseModel


class DriverCreate(BaseModel):
    name: str
    licence: str
    phone: str
    driving_hours: float = 9.0


class IncidentRecord(BaseModel):
    incident: str


class DriverResponse(DriverCreate):
    id: int
    incidents: List[str] = []

    class Config:
        from_attributes = True