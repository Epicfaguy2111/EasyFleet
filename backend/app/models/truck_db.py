from app.core.database import Base
from sqlalchemy import Column, Date, Float, Integer, String


class TruckDB(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    fleet_number = Column(String, unique=True, index=True, nullable=False)
    registration = Column(String, unique=True, index=True, nullable=False)
    vin = Column(String, unique=True, index=True, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    fuel_type = Column(String, default="diesel")
    vehicle_type = Column(String, default="single_rigid")
    axle_count = Column(Integer, default=2)
    engine_power_kw = Column(Float, default=0.0)
    gross_vehicle_weight_kg = Column(Float, default=0.0)
    payload_capacity_kg = Column(Float, default=0.0)
    fuel_tank_capacity_l = Column(Float, default=0.0)
    length_m = Column(Float, default=0.0)
    width_m = Column(Float, default=0.0)
    height_m = Column(Float, default=0.0)
    odometer_km = Column(Float, default=0.0)
    status = Column(String, default="active")
    last_service_date = Column(Date, nullable=True)
    next_service_due_km = Column(Float, nullable=True)