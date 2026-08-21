import os
import csv
from google import genai
from google.genai import types
from app.services.simulator import SAMPLE_FLEET

def get_fleet_context() -> str:
    """Aggregates active telemetry and CSV shipment records into a prompt context."""
    # 1. Telemetry Context
    fleet_lines = []
    for v in SAMPLE_FLEET:
        fleet_lines.append(
            f"- Vehicle {v.vehicle_id} ({v.make_model}): Driver {v.driver_name}, "
            f"Speed {v.speed:.1f} km/h, Fuel {v.fuel_level_liters:.1f}/{v.tank_capacity_liters:.1f}L, "
            f"Engine Temp {v.engine_temp_c:.1f}°C, Status: {v.status}, Odometer: {v.cumulative_distance_km:.1f} km"
        )
    fleet_summary = "\n".join(fleet_lines)

    # 2. Shipments Context from CSV
    shipment_lines = []
    if os.path.exists("shipments.csv"):
        with open("shipments.csv", mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                shipment_lines.append(
                    f"- Shipment {row.get('Shipment ID')}: Type '{row.get('Cargo Type')}', "
                    f"Driver '{row.get('Driver Name')}', Destination '{row.get('End Location')}', "
                    f"ETA '{row.get('Estimated Arrival')}', Status '{row.get('Status')}'"
                )
    shipment_summary = "\n".join(shipment_lines) if shipment_lines else "No active CSV shipments logged."

    return f"""
Current Live Fleet Status:
{fleet_summary}

Current Shipment Schedule:
{shipment_summary}
"""

def query_fleet_assistant(manager_query: str) -> str:
    """Queries Gemini with the injected fleet context."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is not set."

    client = genai.Client(api_key=api_key)
    fleet_context = get_fleet_context()

    system_instruction = (
        "You are EasyFleet AI, an intelligent fleet management assistant. "
        "Your role is to assist fleet supervisors by analyzing current vehicle telemetry, "
        "identifying maintenance or fuel anomalies, reporting shipment ETAs, and recommending operational actions. "
        "Be concise, clear, and prioritize urgent safety or efficiency warnings."
    )

    prompt = f"""
Context:
{fleet_context}

Manager Query:
{manager_query}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        ),
    )
    return response.text