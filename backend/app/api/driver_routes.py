import json
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.driver_db import DriverDB
from app.schemas.driver import DriverCreate, DriverResponse, IncidentRecord

# Ensure data directory exists
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DRIVER_DB_PATH = DATA_DIR / "drivers.db"

driver_engine = create_engine(
    f"sqlite:///{DRIVER_DB_PATH}", connect_args={"check_same_thread": False}
)
DriverSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=driver_engine
)


def get_driver_db():
    db = DriverSessionLocal()
    try:
        yield db
    finally:
        db.close()


DriverDB.__table__.create(bind=driver_engine, checkfirst=True)

router = APIRouter(prefix="/drivers", tags=["Drivers"])


def format_driver(db_driver: DriverDB) -> DriverResponse:
    try:
        incidents = json.loads(db_driver.incidents_json or "[]")
    except Exception:
        incidents = []
    return DriverResponse(
        id=db_driver.id,
        name=db_driver.name,
        licence=db_driver.licence,
        phone=db_driver.phone,
        driving_hours=db_driver.driving_hours,
        incidents=incidents,
    )


@router.get("", response_model=List[DriverResponse])
@router.get("/", response_model=List[DriverResponse], include_in_schema=False)
def get_all_drivers(db: Session = Depends(get_driver_db)):
    drivers = db.query(DriverDB).all()
    return [format_driver(d) for d in drivers]


@router.post("", response_model=DriverResponse)
@router.post("/", response_model=DriverResponse, include_in_schema=False)
def create_driver(driver: DriverCreate, db: Session = Depends(get_driver_db)):
    existing = (
        db.query(DriverDB).filter(DriverDB.licence == driver.licence).first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Driver with this licence number already exists",
        )

    db_driver = DriverDB(
        name=driver.name,
        licence=driver.licence,
        phone=driver.phone,
        driving_hours=driver.driving_hours,
        incidents_json="[]",
    )
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return format_driver(db_driver)


@router.post("/{driver_id}/incidents", response_model=DriverResponse)
def add_driver_incident(
    driver_id: int,
    record: IncidentRecord,
    db: Session = Depends(get_driver_db),
):
    db_driver = db.query(DriverDB).filter(DriverDB.id == driver_id).first()
    if not db_driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    try:
        incidents = json.loads(db_driver.incidents_json or "[]")
    except Exception:
        incidents = []

    incidents.append(record.incident)
    db_driver.incidents_json = json.dumps(incidents)
    db.commit()
    db.refresh(db_driver)
    return format_driver(db_driver)