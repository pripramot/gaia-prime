"""Data pipeline — orchestrates ingestion → processing → storage."""
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from app.data_processing.ingester import DataIngester
from app.data_processing.processor import DataProcessor
from app.data_processing.schema import (
    DataRecord,
    ProcessingJob,
    ProcessingResult,
    ProcessingStatus,
)
from app.data_processing.storage import DataStorage
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


class DataPipeline:
    """
    GAIA PRIME Ring-Forge data pipeline.

    Executes the full ETL cycle:
        Ingest → Validate → Normalise → Checksum → Persist
    """

    def __init__(self, storage: Optional[DataStorage] = None):
        self._ingester = DataIngester()
        self._processor = DataProcessor()
        self._storage = storage or DataStorage()

    async def run(
        self,
        source: str,
        record_type: str,
        payloads: list[dict[str, Any]],
        pipeline_name: str = "default",
    ) -> ProcessingResult:
        job_id = str(uuid.uuid4())
        started = time.monotonic()

        job = ProcessingJob(
            job_id=job_id,
            pipeline=pipeline_name,
            status=ProcessingStatus.processing,
            records_in=len(payloads),
            created_at=datetime.now(tz=timezone.utc),
        )
        await self._storage.save_job(job)

        try:
            records = self._ingester.ingest_batch(source, record_type, payloads)
            processed = self._processor.process_batch(records)
            await self._storage.save_records(processed)

            successful = [r for r in processed if r.status == ProcessingStatus.completed]
            failed = [r for r in processed if r.status == ProcessingStatus.failed]

            job.status = ProcessingStatus.completed if not failed else ProcessingStatus.failed
            job.records_out = len(successful)
            job.finished_at = datetime.now(tz=timezone.utc)
            await self._storage.update_job(job)

            duration_ms = (time.monotonic() - started) * 1000
            logger.info(
                "Pipeline '%s' job=%s in=%d out=%d failed=%d duration=%.1fms",
                pipeline_name,
                job_id,
                len(payloads),
                len(successful),
                len(failed),
                duration_ms,
            )
            return ProcessingResult(
                job_id=job_id,
                pipeline=pipeline_name,
                status=job.status,
                records_in=len(payloads),
                records_out=len(successful),
                duration_ms=duration_ms,
            )

        except Exception as exc:
            job.status = ProcessingStatus.failed
            job.error = str(exc)
            job.finished_at = datetime.now(tz=timezone.utc)
            await self._storage.update_job(job)
            logger.error("Pipeline '%s' job=%s error=%s", pipeline_name, job_id, exc)
            raise

    async def run_single(
        self,
        source: str,
        record_type: str,
        payload: dict[str, Any],
        pipeline_name: str = "default",
    ) -> ProcessingResult:
        return await self.run(source, record_type, [payload], pipeline_name)
