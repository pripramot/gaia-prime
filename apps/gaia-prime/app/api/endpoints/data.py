"""Data ingestion endpoint — accepts records for processing."""
from typing import Any, Optional

from app.data_processing.pipeline import DataPipeline
from app.data_processing.schema import ProcessingResult
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter()
_pipeline = DataPipeline()


class IngestRequest(BaseModel):
    source: str
    record_type: str
    payload: dict[str, Any]
    pipeline: str = "default"


class BatchIngestRequest(BaseModel):
    source: str
    record_type: str
    payloads: list[dict[str, Any]]
    pipeline: str = "default"


@router.post("/ingest", response_model=ProcessingResult, status_code=202)
async def ingest_single(body: IngestRequest) -> ProcessingResult:
    try:
        return await _pipeline.run_single(
            source=body.source,
            record_type=body.record_type,
            payload=body.payload,
            pipeline_name=body.pipeline,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/ingest/batch", response_model=ProcessingResult, status_code=202)
async def ingest_batch(body: BatchIngestRequest) -> ProcessingResult:
    if not body.payloads:
        raise HTTPException(status_code=422, detail="payloads must not be empty")
    try:
        return await _pipeline.run(
            source=body.source,
            record_type=body.record_type,
            payloads=body.payloads,
            pipeline_name=body.pipeline,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/records")
async def list_records(
    source: Optional[str] = Query(None),
    record_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
) -> list[dict]:
    from app.data_processing.storage import DataStorage
    storage = DataStorage()
    return await storage.get_records(source=source, record_type=record_type, limit=limit)
