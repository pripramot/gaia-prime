"""Data schemas for GAIA PRIME processing pipeline."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ProcessingStatus(str, Enum):
    raw = "raw"
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class DataRecord(BaseModel):
    id: Optional[int] = None
    source: str = Field(..., description="Origin service/system identifier")
    record_type: str = Field(..., description="Semantic type of the record")
    payload: dict[str, Any] = Field(..., description="Raw payload data")
    checksum: Optional[str] = None
    status: ProcessingStatus = ProcessingStatus.raw
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None


class ProcessingJob(BaseModel):
    id: Optional[int] = None
    job_id: str = Field(..., description="UUID of the processing job")
    pipeline: str = Field(..., description="Pipeline name to execute")
    status: ProcessingStatus = ProcessingStatus.pending
    records_in: int = 0
    records_out: int = 0
    error: Optional[str] = None
    created_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


class ProcessingResult(BaseModel):
    job_id: str
    pipeline: str
    status: ProcessingStatus
    records_in: int
    records_out: int
    duration_ms: float
    error: Optional[str] = None
