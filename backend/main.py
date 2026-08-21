import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api.ai_routes import router as ai_router
from app.api.truck_routes import router as truck_router

app = FastAPI(
    title="EasyFleet API",
    description="Fleet telemetry, route optimization, and predictive maintenance",
    version="0.1.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include both routers
app.include_router(ai_router)
app.include_router(truck_router)


@app.get("/")
async def root():
    return {"status": "online", "message": "EasyFleet backend operational"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}