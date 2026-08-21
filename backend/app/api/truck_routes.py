from typing import List
from app.core.database import Base, engine, get_db
from app.models.truck_db import TruckDB
from app.schemas.truck import TruckCreate, TruckResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Create database tables automatically
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/trucks", tags=["Trucks"])


@router.get("/", response_model=List[TruckResponse])
def get_all_trucks(db: Session = Depends(get_db)):
    return db.query(TruckDB).all()


@router.post("/", response_model=TruckResponse)
def create_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(TruckDB)
        .filter(TruckDB.registration == truck.registration)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="Registration number already registered"
        )

    db_truck = TruckDB(
        name=truck.name,
        registration=truck.registration,
        weight=truck.weight,
        height=truck.height,
        length=truck.length,
        fuel=truck.fuel,
        driver_name=truck.driver.name if truck.driver else None,
        driver_licence=truck.driver.licence if truck.driver else None,
        driver_phone=truck.driver.phone if truck.driver else None,
    )
    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)
    return db_truck