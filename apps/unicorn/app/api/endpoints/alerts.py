"""Cyber security alert endpoints."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AlertSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class CyberAlertRequest(BaseModel):
    source_ip: Optional[str] = None
    target: str
    severity: AlertSeverity
    event_type: str
    details: dict[str, Any] = {}
    timestamp: datetime


class CyberAlertResponse(BaseModel):
    alert_id: str
    status: str
    severity: AlertSeverity


@router.post("", response_model=CyberAlertResponse, status_code=202)
async def submit_alert(body: CyberAlertRequest) -> CyberAlertResponse:
    import uuid
    return CyberAlertResponse(
        alert_id=str(uuid.uuid4()),
        status="received",
        severity=body.severity,
    )
