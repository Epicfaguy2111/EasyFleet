from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Path for the isolated SQLite database file
DRIVER_DATABASE_URL = "sqlite:///./drivers.db"

driver_engine = create_engine(
    DRIVER_DATABASE_URL, connect_args={"check_same_thread": False}
)

DriverSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=driver_engine
)

DriverBase = declarative_base()


def get_driver_db():
    db = DriverSessionLocal()
    try:
        yield db
    finally:
        db.close()