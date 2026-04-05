"""Digital forensics endpoints."""
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ForensicCaseRequest(BaseModel):
    case_id: str
    evidence_hash: str
    source: str
    metadata: dict[str, Any] = {}


class ForensicCaseResponse(BaseModel):
    case_id: str
    status: str
    evidence_hash: str


@router.post("/case", response_model=ForensicCaseResponse, status_code=202)
async def submit_case(body: ForensicCaseRequest) -> ForensicCaseResponse:
    return ForensicCaseResponse(
        case_id=body.case_id,
        status="received",
        evidence_hash=body.evidence_hash,
    )
