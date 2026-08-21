from pydantic import BaseModel


class VehicleHealthProfile(BaseModel):
    vehicle_id: str
    age_years: float
    odometer_km: float
    harsh_braking_count_last_30d: int
    overheat_events_count: int
    days_since_last_service: int


class MaintenanceScore(BaseModel):
    risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    maintenance_urgency_percent: float
    recommended_action: str


def evaluate_maintenance_risk(
    profile: VehicleHealthProfile,
) -> MaintenanceScore:
    """Predictive heuristic / scoring model for vehicle component failure."""
    risk_score = 0.0

    # Age & Odometer weighting
    risk_score += min(30.0, (profile.odometer_km / 100_000.0) * 10.0)
    risk_score += min(20.0, profile.age_years * 3.0)

    # Wear-and-tear strain
    risk_score += min(25.0, profile.harsh_braking_count_last_30d * 2.5)
    risk_score += min(25.0, profile.overheat_events_count * 10.0)

    # Time since last service penalty
    if profile.days_since_last_service > 180:
        risk_score += 15.0

    urgency = min(100.0, risk_score)

    if urgency >= 75.0:
        return MaintenanceScore(
            risk_level="CRITICAL",
            maintenance_urgency_percent=urgency,
            recommended_action="Schedule immediate brake and engine inspection before next dispatch.",
        )
    elif urgency >= 50.0:
        return MaintenanceScore(
            risk_level="HIGH",
            maintenance_urgency_percent=urgency,
            recommended_action="Book scheduled service within the next 7 operating days.",
        )
    elif urgency >= 25.0:
        return MaintenanceScore(
            risk_level="MODERATE",
            maintenance_urgency_percent=urgency,
            recommended_action="Monitor telemetry; no immediate action required.",
        )
    return MaintenanceScore(
        risk_level="LOW",
        maintenance_urgency_percent=urgency,
        recommended_action="Vehicle operates within optimal safety margins.",
    )