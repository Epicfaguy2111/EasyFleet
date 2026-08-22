import asyncio
import math
from pathlib import Path
import random
import sys
from typing import Any, Dict, Tuple

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import API Routers
from app.api.ai_routes import router as ai_router
from app.api.driver_routes import router as driver_router
from app.api.truck_routes import router as truck_router

# 1. FastAPI Application Instance
app = FastAPI(
    title="EasyFleet API",
    description="Fleet telemetry, route optimization, predictive maintenance, and driver management",
    version="0.1.0",
)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount Frontend Directory
frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/frontend", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

# 4. Register Routers
app.include_router(ai_router)
app.include_router(truck_router)
app.include_router(driver_router)


# 5. Route Calculation Helpers
CITY_COORDINATES = {
    "cape town": (-33.9249, 18.4241),
    "johannesburg": (-26.2041, 28.0473),
    "durban": (-29.8587, 31.0218),
    "port elizabeth": (-33.9608, 25.6022),
    "gqeberha": (-33.9608, 25.6022),
    "bloemfontein": (-29.1167, 26.2167),
    "pretoria": (-25.7479, 28.2293),
    "east london": (-33.0153, 27.9116),
}


class RouteRequest(BaseModel):
    start: str
    destination: str
    truck: Dict[str, Any]
    driver: Dict[str, Any]


def get_coords(name: str) -> Tuple[float, float]:
    cleaned = name.lower().strip()
    for city, coords in CITY_COORDINATES.items():
        if city in cleaned:
            return coords
    return (-33.9249, 18.4241)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


# 6. Core Endpoints
@app.get("/")
async def root():
    return {"status": "online", "message": "EasyFleet backend operational"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/route")
async def calculate_route_endpoint(req: RouteRequest):
    c1 = get_coords(req.start)
    c2 = get_coords(req.destination)
    dist = round(max(haversine(c1[0], c1[1], c2[0], c2[1]) * 1.25, 20.0), 1)

    hours = int(dist / 75.0)
    mins = int(((dist / 75.0) - hours) * 60)
    fuel = round((dist / 100.0) * 34.0, 1)

    return {
        "distance_km": dist,
        "duration_text": f"{hours}h {mins}m",
        "fuel_required_liters": fuel,
        "start_coord": list(c1),
        "dest_coord": list(c2),
        "waypoints": [
            list(c1),
            [(c1[0] + c2[0]) / 2, (c1[1] + c2[1]) / 2],
            list(c2),
        ],
    }


# 7. WebSocket Live Telemetry Simulation Endpoint
@app.websocket("/ws/simulate-route")
async def websocket_simulate_route(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        coordinates = data.get("coordinates", [])
        truck_info = data.get("truck", {})
        driver_info = data.get("driver", {})
        route_id = data.get("route_id", "1")

        if not coordinates or len(coordinates) < 2:
            await websocket.send_json({"error": "Invalid route coordinates"})
            return

        fuel_remaining = float(
            truck_info.get("fuel_tank_capacity_l", 300.0) or 300.0
        )
        speed = 70.0
        engine_temp = 87.0

        step_stride = max(1, len(coordinates) // 250)
        route_points = coordinates[::step_stride]
        if route_points[-1] != coordinates[-1]:
            route_points.append(coordinates[-1])

        for i, (lon, lat) in enumerate(route_points):
            speed = max(45.0, min(105.0, speed + (random.random() - 0.5) * 8))
            engine_temp = max(82.0, min(106.0, engine_temp + (random.random() - 0.5) * 0.9))
            fuel_remaining = max(0.0, fuel_remaining - 0.08)

            events = []
            if random.random() < 0.03:
                speed = max(25.0, speed - 35.0)
                events.append("Harsh braking detected")
            elif speed > 80.0:
                events.append(f"Overspeeding warning ({speed:.0f} km/h)")
            elif random.random() < 0.1:
                speed = 0.0
                events.append("Emergency: Flat tyre detected")
            elif engine_temp > 102.0:
                events.append(f"Engine overheating ({engine_temp:.1f}°C)")

            telemetry_tick = {
                "route_id": route_id,
                "step": i + 1,
                "total_steps": len(route_points),
                "lat": lat,
                "lon": lon,
                "speed": round(speed, 1),
                "fuel": round(fuel_remaining, 1),
                "engine_temp": round(engine_temp, 1),
                "status": "INCIDENT" if events else "EN_ROUTE",
                "events": events,
                "is_completed": (i == len(route_points) - 1)
            }

            await websocket.send_json(telemetry_tick)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Simulation client disconnected")