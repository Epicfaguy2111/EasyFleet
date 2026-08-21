from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_assistant import query_fleet_assistant
from app.services.ai_telemetry_analyzer import TelemetryAIAnalyzer, TelemetryFrame
from app.services.predictive_maintenance import (
    VehicleHealthProfile,
    evaluate_maintenance_risk,
)
from app.services.route_optimizer import evaluate_route_safety

router = APIRouter(prefix="/ai", tags=["AI & Analytics"])
analyzer = TelemetryAIAnalyzer()


# Pydantic schema for the manager prompt
class AssistantQuery(BaseModel):
    query: str


# 1. AI Supervisor Assistant Route -> URL: /ai/assistant/chat
@router.post("/assistant/chat")
async def chat_with_assistant(payload: AssistantQuery):
    response_text = query_fleet_assistant(payload.query)
    return {"query": payload.query, "response": response_text}


# 2. Telemetry Anomaly Analyzer -> URL: /ai/telemetry/analyze
@router.post("/telemetry/analyze")
async def analyze_telemetry(frame: TelemetryFrame):
    alerts = analyzer.analyze_frame(frame)
    return {"status": "analyzed", "alerts": alerts}


# 3. Predictive Maintenance -> URL: /ai/maintenance/predict
@router.post("/maintenance/predict")
async def predict_maintenance(profile: VehicleHealthProfile):
    return evaluate_maintenance_risk(profile)


# 4. Route Risk Assessment -> URL: /ai/routes/check-risk
@router.post("/routes/check-risk")
async def check_route_risk(waypoints: list[tuple[float, float]]):
    return evaluate_route_safety(waypoints)