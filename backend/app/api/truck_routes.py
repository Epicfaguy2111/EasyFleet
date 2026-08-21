from typing import List
from app.core.database import Base, engine, get_db
from app.models.truck_db import TruckDB
from app.schemas.truck import TruckCreate, TruckResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/trucks", tags=["Trucks"])


@router.post("/", response_model=TruckResponse)
def create_truck(truck: TruckCreate, db: Session = Depends(get_db)):
    # Check if registration already exists
    existing = (
        db.query(TruckDB)
        .filter(
            (TruckDB.registration == truck.registration)
            | (TruckDB.vin == truck.vin)
            | (TruckDB.fleet_number == truck.fleet_number)
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Vehicle with this VIN, Registration, or Fleet Number already exists",
        )

    db_truck = TruckDB(**truck.model_dump())
    db.add(db_truck)
    db.commit()
    db.refresh(db_truck)
    return db_truck


@router.get("/", response_model=List[TruckResponse])
def get_all_trucks(db: Session = Depends(get_db)):
    return db.query(TruckDB).all()