import asyncio
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import random
from typing import List


@dataclass
class VehicleState:
    vehicle_id: str
    make_model: str
    driver_id: str
    driver_name: str
    lat: float
    lon: float
    speed: float  # km/h
    fuel_level_liters: float  # current fuel in tank
    tank_capacity_liters: float
    baseline_l_per_100km: float
    engine_temp_c: float
    status: str  # "EN_ROUTE", "IDLING", "MAINTENANCE_ALERT", "INCIDENT"
    cumulative_distance_km: float


# Sample routes around South Africa / major transport corridors
SAMPLE_FLEET = [
    VehicleState(
        vehicle_id="TRK-101",
        make_model="Volvo FH16",
        driver_id="DRV-001",
        driver_name="Sipho Ndlovu",
        lat=-26.2041,
        lon=28.0473,  # Johannesburg
        speed=65.0,
        fuel_level_liters=280.0,
        tank_capacity_liters=300.0,
        baseline_l_per_100km=32.0,
        engine_temp_c=88.0,
        status="EN_ROUTE",
        cumulative_distance_km=1420.0,
    ),
    VehicleState(
        vehicle_id="TRK-102",
        make_model="Scania R500",
        driver_id="DRV-002",
        driver_name="Thabo Molefe",
        lat=-29.8587,
        lon=31.0218,  # Durban
        speed=0.0,
        fuel_level_liters=190.0,
        tank_capacity_liters=250.0,
        baseline_l_per_100km=30.0,
        engine_temp_c=75.0,
        status="IDLING",
        cumulative_distance_km=890.0,
    ),
    VehicleState(
        vehicle_id="TRK-103",
        make_model="Mercedes-Benz Actros",
        driver_id="DRV-003",
        driver_name="Johan van der Merwe",
        lat=-33.9249,
        lon=18.4241,  # Cape Town
        speed=80.0,
        fuel_level_liters=210.0,
        tank_capacity_liters=320.0,
        baseline_l_per_100km=34.0,
        engine_temp_c=91.0,
        status="EN_ROUTE",
        cumulative_distance_km=2340.0,
    ),
]


def update_telemetry(vehicle: VehicleState, step_seconds: float = 2.0) -> dict:
    """Updates vehicle coordinates, fuel consumption, and detects anomaly triggers."""
    # 1. Coordinate step (small random movement)
    lat_delta = (random.random() - 0.5) * 0.005
    lon_delta = (random.random() - 0.5) * 0.005
    vehicle.lat += lat_delta
    vehicle.lon += lon_delta

    # 2. Speed and distance
    if vehicle.status == "IDLING":
        vehicle.speed = 0.0
    else:
        # Vary speed between 50 and 95 km/h
        vehicle.speed = max(
            40.0, min(100.0, vehicle.speed + (random.random() - 0.5) * 10)
        )

    distance_step_km = (vehicle.speed * (step_seconds / 3600.0))
    vehicle.cumulative_distance_km += distance_step_km

    # 3. Fuel calculation
    expected_burn = (distance_step_km / 100.0) * vehicle.baseline_l_per_100km
    events: List[str] = []

    # Injected Anomaly 1: Fuel Theft / Rapid Leak (0.5% chance)
    if random.random() < 0.005:
        theft_amount = random.uniform(15.0, 30.0)
        vehicle.fuel_level_liters = max(
            0.0, vehicle.fuel_level_liters - theft_amount
        )
        events.append(f"CRITICAL: Sudden fuel drop (-{theft_amount:.1f}L)")

    # Injected Anomaly 2: Harsh Braking (2% chance if moving)
    elif vehicle.speed > 50 and random.random() < 0.02:
        vehicle.speed = max(10.0, vehicle.speed - 40.0)
        events.append("WARNING: Harsh braking event registered")

    # Injected Anomaly 3: Prolonged Idling
    elif vehicle.speed == 0.0 and random.random() < 0.1:
        vehicle.status = "IDLING"
        expected_burn += 0.05  # baseline idle burn
        events.append("INFO: Vehicle idling")
    else:
        vehicle.status = "EN_ROUTE"
        vehicle.fuel_level_liters = max(
            0.0, vehicle.fuel_level_liters - expected_burn
        )

    # 4. Engine temperature fluctuations
    vehicle.engine_temp_c += (random.random() - 0.5) * 1.5
    if vehicle.engine_temp_c > 102.0:
        events.append(
            f"WARNING: High engine temp ({vehicle.engine_temp_c:.1f}°C)"
        )

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "telemetry": asdict(vehicle),
        "events": events,
    }


async def run_telemetry_stream(interval_seconds: float = 2.0):
    """Simulates real-time telemetry streaming."""
    print("🚀 Starting EasyFleet Live Telemetry Streamer...")
    print("Press Ctrl + C to stop.\n" + "=" * 60)

    while True:
        for vehicle in SAMPLE_FLEET:
            payload = update_telemetry(vehicle, step_seconds=interval_seconds)
            t = payload["telemetry"]
            events_str = (
                f" | ⚠️  {', '.join(payload['events'])}"
                if payload["events"]
                else ""
            )

            print(
                f"[{payload['timestamp'][:19]}] {t['vehicle_id']} ({t['make_model']}) | "
                f"Pos: ({t['lat']:.4f}, {t['lon']:.4f}) | "
                f"Speed: {t['speed']:.1f} km/h | Fuel: {t['fuel_level_liters']:.1f}L | "
                f"Status: {t['status']}{events_str}"
            )
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    try:
        asyncio.run(run_telemetry_stream())
    except KeyboardInterrupt:
        print("\n🛑 Telemetry stream stopped.")