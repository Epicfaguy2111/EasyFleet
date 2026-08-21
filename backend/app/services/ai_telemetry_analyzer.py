from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TelemetryFrame:
    vehicle_id: str
    speed: float  # km/h
    fuel_level_liters: float
    baseline_burn_l_per_100km: float
    distance_delta_km: float
    idle_minutes: float
    engine_temp: float


@dataclass
class AnomalyAlert:
    alert_type: str  # FUEL_THEFT, HARSH_BRAKING, EXCESSIVE_IDLING, ENGINE_OVERHEAT
    severity: str  # LOW, MEDIUM, CRITICAL
    message: str
    confidence_score: float


class TelemetryAIAnalyzer:
    def __init__(self):
        self.last_fuel_readings = {}

    def analyze_frame(
        self, frame: TelemetryFrame, prev_speed: Optional[float] = None
    ) -> List[AnomalyAlert]:
        alerts = []

        # 1. Fuel Theft Anomaly Detection
        if frame.vehicle_id in self.last_fuel_readings:
            prev_fuel = self.last_fuel_readings[frame.vehicle_id]
            expected_consumption = (
                frame.distance_delta_km / 100.0
            ) * frame.baseline_burn_l_per_100km
            fuel_drop = prev_fuel - frame.fuel_level_liters

            # Sudden drop greater than 5L beyond expected burn while stationary or low movement
            if (
                fuel_drop > (expected_consumption + 5.0)
                and frame.speed < 10.0
            ):
                alerts.append(
                    AnomalyAlert(
                        alert_type="FUEL_THEFT",
                        severity="CRITICAL",
                        message=f"Suspicious fuel drop of {fuel_drop:.2f}L detected with minimal movement.",
                        confidence_score=0.92,
                    )
                )

        self.last_fuel_readings[frame.vehicle_id] = frame.fuel_level_liters

        # 2. Harsh Braking Detection
        if prev_speed is not None:
            deceleration = prev_speed - frame.speed
            if (
                deceleration > 30.0
            ):  # Speed drop > 30 km/h over single sampling interval
                alerts.append(
                    AnomalyAlert(
                        alert_type="HARSH_BRAKING",
                        severity="MEDIUM",
                        message=f"Harsh braking registered (-{deceleration:.1f} km/h).",
                        confidence_score=0.88,
                    )
                )

        # 3. Excessive Idling Detection
        if frame.idle_minutes >= 10.0:
            alerts.append(
                AnomalyAlert(
                    alert_type="EXCESSIVE_IDLING",
                    severity="LOW",
                    message=f"Vehicle idling for {frame.idle_minutes:.1f} continuous minutes.",
                    confidence_score=0.95,
                )
            )

        # 4. Engine Health & Overheating
        if frame.engine_temp > 105.0:
            alerts.append(
                AnomalyAlert(
                    alert_type="ENGINE_OVERHEAT",
                    severity="CRITICAL",
                    message=f"High engine temperature registered: {frame.engine_temp:.1f}°C.",
                    confidence_score=0.99,
                )
            )

        return alerts