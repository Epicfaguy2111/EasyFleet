import math
from typing import List, Tuple


def haversine_distance_km(
    coord1: Tuple[float, float], coord2: Tuple[float, float]
) -> float:
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 6371.0  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# Example known high-risk coordinates (Lat, Lon, Radius km)
HIGH_RISK_ZONES = [
    {"name": "Zone Alpha Hotspot", "coords": (-26.1850, 28.0120), "radius_km": 3.0},
    {"name": "Corridor Beta Hazard", "coords": (-29.8200, 30.9800), "radius_km": 4.5},
]


def evaluate_route_safety(
    waypoints: List[Tuple[float, float]],
) -> dict:
    flagged_zones = []

    for point in waypoints:
        for zone in HIGH_RISK_ZONES:
            dist = haversine_distance_km(point, zone["coords"])
            if dist <= zone["radius_km"]:
                flagged_zones.append(
                    {
                        "zone_name": zone["name"],
                        "distance_to_center_km": round(dist, 2),
                    }
                )

    return {
        "is_safe": len(flagged_zones) == 0,
        "hazard_count": len(flagged_zones),
        "hazards": flagged_zones,
        "recommended_reroute": len(flagged_zones) > 0,
    }