from sqlalchemy import Column, Float, Integer, String
from app.core.database import Base


class DriverDB(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    licence = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    driving_hours = Column(Float, default=9.0)
    incidents_json = Column(String, default="[]")