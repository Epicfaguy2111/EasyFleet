import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from app.api.ai_routes import router as ai_router

app = FastAPI(
    title="EasyFleet API",
    description="Fleet telemetry, route optimization, and predictive maintenance",
    version="0.1.0",
)

app.include_router(ai_router)


@app.get("/")
async def root():
    return {"status": "online", "message": "EasyFleet backend operational"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}