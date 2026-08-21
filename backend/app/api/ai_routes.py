from app.services.ai_telemetry_analyzer import TelemetryAIAnalyzer, TelemetryFrame
from app.services.predictive_maintenance import (
    VehicleHealthProfile,
    evaluate_maintenance_risk,
)
from app.services.route_optimizer import evaluate_route_safety
from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["AI & Analytics"])
analyzer = TelemetryAIAnalyzer()


@router.post("/telemetry/analyze")
async def analyze_telemetry(frame: TelemetryFrame):
    alerts = analyzer.analyze_frame(frame)
    return {"status": "analyzed", "alerts": alerts}


@router.post("/maintenance/predict")
async def predict_maintenance(profile: VehicleHealthProfile):
    return evaluate_maintenance_risk(profile)


@router.post("/routes/check-risk")
async def check_route_risk(waypoints: list[tuple[float, float]]):
    return evaluate_route_safety(waypoints)