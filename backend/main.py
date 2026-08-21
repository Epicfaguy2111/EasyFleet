import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ai_routes import router as ai_router

app = FastAPI(
    title="EasyFleet API",
    description="Fleet telemetry, route optimization, and predictive maintenance",
    version="0.1.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)


@app.get("/")
async def root():
    return {"status": "online", "message": "EasyFleet backend operational"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}