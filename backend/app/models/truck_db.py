from app.core.database import Base
from sqlalchemy import Column, Date, Float, Integer, String


class TruckDB(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    fleet_number = Column(String, unique=True, index=True, nullable=False)
    registration = Column(String, unique=True, index=True, nullable=False)
    vin = Column(String, unique=True, index=True, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    fuel_type = Column(String, default="diesel")
    vehicle_type = Column(String, nullable=False)
    axles = Column(Integer, default=2)
    engine_power = Column(Float, default=0.0)
    weight = Column(Float, default=0.0)  # GVWR
    payload = Column(Float, default=0.0)
    fuel = Column(Float, default=0.0)  # Tank Capacity
    length = Column(Float, default=0.0)
    width = Column(Float, default=0.0)
    height = Column(Float, default=0.0)
    odometer = Column(Float, default=0.0)
    status = Column(String, default="active")
    last_service_date = Column(Date, nullable=True)
    next_service_km = Column(Float, nullable=True)