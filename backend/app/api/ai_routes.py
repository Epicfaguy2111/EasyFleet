from typing import Any, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_assistant import (
    evaluate_driver_post_trip,
    evaluate_driver_pre_trip,
    query_fleet_assistant,
)

router = APIRouter(prefix="/ai", tags=["AI & Analytics"])


class AssistantQuery(BaseModel):
    query: str


class PreTripScoreRequest(BaseModel):
    driver: Dict[str, Any]
    truck: Dict[str, Any]


class PostTripScoreRequest(BaseModel):
    trip_incidents: List[str]
    base_score: int = 100


@router.post("/assistant/chat")
async def chat_with_assistant(payload: AssistantQuery):
    response_text = query_fleet_assistant(payload.query)
    return {"query": payload.query, "response": response_text}


@router.post("/driver/pre-trip-score")
async def pre_trip_score(payload: PreTripScoreRequest):
    return evaluate_driver_pre_trip(payload.driver, payload.truck)


@router.post("/driver/post-trip-score")
async def post_trip_score(payload: PostTripScoreRequest):
    return evaluate_driver_post_trip(payload.trip_incidents, payload.base_score)