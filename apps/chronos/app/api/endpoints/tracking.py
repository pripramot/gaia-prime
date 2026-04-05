"""Mobile tracking endpoint — ingest GPS/location points."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class TrackingPoint(BaseModel):
    device_id: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude: Optional[float] = None
    accuracy: Optional[float] = None
    timestamp: datetime


class TrackingResponse(BaseModel):
    device_id: str
    status: str
    timestamp: datetime


@router.post("/point", response_model=TrackingResponse, status_code=202)
async def ingest_point(body: TrackingPoint) -> TrackingResponse:
    return TrackingResponse(
        device_id=body.device_id,
        status="received",
        timestamp=body.timestamp,
    )
