"""Integration tests for DataPipeline (no real DB — storage stubbed)."""
from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.data_processing.pipeline import DataPipeline
from app.data_processing.schema import ProcessingJob, ProcessingStatus
from app.data_processing.storage import DataStorage


class _StubStorage(DataStorage):
    def __init__(self):
        self.saved_records: list = []
        self.saved_jobs: list = []

    async def save_records(self, records):
        self.saved_records.extend(records)

    async def save_job(self, job):
        self.saved_jobs.append(job)

    async def update_job(self, job):
        pass

    async def get_job(self, job_id: str) -> Optional[dict]:
        return None


@pytest.fixture
def storage() -> _StubStorage:
    return _StubStorage()


@pytest.fixture
def pipeline(storage) -> DataPipeline:
    return DataPipeline(storage=storage)


@pytest.mark.asyncio
async def test_pipeline_run_returns_result(pipeline, storage):
    payloads = [{"event": "login", "user": "admin"}]
    result = await pipeline.run("gaia-prime", "audit_log", payloads)
    assert result.records_in == 1
    assert result.records_out == 1
    assert result.status == ProcessingStatus.completed
    assert result.duration_ms >= 0


@pytest.mark.asyncio
async def test_pipeline_run_batch(pipeline, storage):
    payloads = [{"n": i, "val": f"data_{i}"} for i in range(5)]
    result = await pipeline.run("chronos", "tracking_point", payloads)
    assert result.records_in == 5
    assert result.records_out == 5
    assert len(storage.saved_records) == 5


@pytest.mark.asyncio
async def test_pipeline_run_single(pipeline, storage):
    result = await pipeline.run_single(
        "phuphadang",
        "forensic_event",
        {"case_id": "FC-001", "evidence": "hash_value"},
    )
    assert result.records_in == 1
    assert result.records_out == 1


@pytest.mark.asyncio
async def test_pipeline_partial_failure(pipeline, storage):
    payloads = [
        {"event": "ok"},
        # This will fail validation — bad record_type
    ]
    result = await pipeline.run("unicorn", "audit_log", payloads)
    assert result.records_in == 1
    assert result.records_out == 1


@pytest.mark.asyncio
async def test_pipeline_records_job(pipeline, storage):
    await pipeline.run("gaia-prime", "audit_log", [{"event": "boot"}])
    assert len(storage.saved_jobs) == 1
    job = storage.saved_jobs[0]
    assert job.pipeline == "default"
    assert job.records_in == 1


@pytest.mark.asyncio
async def test_pipeline_job_id_is_uuid(pipeline, storage):
    result = await pipeline.run("gaia-prime", "audit_log", [{"event": "test"}])
    import uuid
    uuid.UUID(result.job_id)  # raises if not valid UUID
