from typing import Any, Dict, List

# Default fleet fallback
SAMPLE_FLEET = [
    {
        "id": "1",
        "name": "Truck 1",
        "registration": "CA 1234",
        "fuel_type": "Diesel",
        "weight_kg": 16000,
        "status": "Active"
    },
    {
        "id": "2",
        "name": "Truck 2",
        "registration": "CA 5678",
        "fuel_type": "Diesel",
        "weight_kg": 18000,
        "status": "Active"
    }
]


def evaluate_driver_pre_trip(driver: Dict[str, Any], truck: Dict[str, Any]) -> Dict[str, Any]:
    score = 100
    deductions = []

    incidents: List[str] = driver.get("incidents", []) or []
    for inc in incidents:
        inc_lower = str(inc).lower()
        if "harsh braking" in inc_lower:
            score -= 6
            deductions.append("-6 pts: Historical harsh braking event")
        elif "overspeeding" in inc_lower:
            score -= 8
            deductions.append("-8 pts: Historical overspeeding record")
        elif "flat tyre" in inc_lower or "emergency" in inc_lower:
            score -= 4
            deductions.append("-4 pts: Historical emergency incident")
        else:
            score -= 3
            deductions.append("-3 pts: Recorded driving violation")

    hours = float(driver.get("driving_hours", 9.0) or 9.0)
    if hours < 4.0:
        score -= 15
        deductions.append("-15 pts: Low remaining driving hours (< 4 hrs fatigue risk)")
    elif hours < 6.0:
        score -= 8
        deductions.append("-8 pts: Moderate shift fatigue (< 6 hrs remaining)")

    final_score = max(20, min(100, score))
    if final_score >= 85:
        rating = "Low Risk (Optimal)"
        assessment = "Driver exhibits high reliability and standard compliance for this route."
    elif final_score >= 65:
        rating = "Moderate Risk"
        assessment = "Driver shows slight prior risk indicators. Recommend standard monitoring."
    else:
        rating = "High Risk"
        assessment = "High caution advised. Frequent past incidents or elevated fatigue risk detected."

    return {
        "score": final_score,
        "rating": rating,
        "assessment": assessment,
        "deductions": deductions
    }


def evaluate_driver_post_trip(trip_incidents: List[str], base_score: int = 100) -> Dict[str, Any]:
    score = base_score
    deductions = []

    for item in trip_incidents:
        item_lower = str(item).lower()
        if "harsh braking" in item_lower:
            score -= 10
            deductions.append("-10 pts: Trip harsh braking")
        elif "overspeeding" in item_lower:
            score -= 12
            deductions.append("-12 pts: Trip overspeeding violation")
        elif "flat tyre" in item_lower:
            score -= 5
            deductions.append("-5 pts: Route emergency stop")
        elif "overheating" in item_lower:
            score -= 8
            deductions.append("-8 pts: Engine stress threshold exceeded")
        else:
            score -= 5
            deductions.append("-5 pts: Miscellaneous route incident")

    final_score = max(10, min(100, score))
    if final_score >= 85:
        summary = "Outstanding trip performance with strong safety metrics."
    elif final_score >= 60:
        summary = "Satisfactory completion with moderate safety incidents noted."
    else:
        summary = "Sub-optimal trip safety score. Driver review recommended."

    return {
        "final_score": final_score,
        "trip_incidents_count": len(trip_incidents),
        "deductions": deductions,
        "summary": summary
    }


def query_fleet_assistant(query: str) -> str:
    cleaned = query.lower()
    if "score" in cleaned or "driver" in cleaned:
        return "EasyFleet AI continuously scores drivers pre-trip, live during transit, and post-trip on a 100-point scale based on fatigue and safety compliance."
    if "truck" in cleaned or "fleet" in cleaned:
        return "EasyFleet is actively monitoring vehicle telemetry, route optimization, and maintenance profiles."
    return f"EasyFleet Assistant received query: '{query}'. Telemetry and driver performance scoring engines are operating normally."