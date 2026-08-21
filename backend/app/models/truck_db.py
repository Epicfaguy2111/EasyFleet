from app.core.database import Base
from sqlalchemy import Column, Float, Integer, String


class TruckDB(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    registration = Column(String, unique=True, index=True, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    fuel = Column(Float, nullable=False)
    driver_name = Column(String, nullable=True)
    driver_licence = Column(String, nullable=True)
    driver_phone = Column(String, nullable=True)