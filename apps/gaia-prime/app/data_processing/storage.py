"""Data storage adapter — persists records and jobs to the database."""
import json
from typing import Optional

from app.data_processing.schema import DataRecord, ProcessingJob, ProcessingStatus
from app.core.db import db_manager
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


class DataStorage:
    """Async storage adapter wrapping GaiaDatabaseManager."""

    async def save_records(self, records: list[DataRecord]) -> None:
        async with db_manager.transaction():
            for record in records:
                await db_manager.execute(
                    """
                    INSERT INTO data_records
                        (source, record_type, payload, checksum, status, created_at, processed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.source,
                        record.record_type,
                        json.dumps(record.payload, ensure_ascii=False),
                        record.checksum or "",
                        record.status.value,
                        record.created_at.isoformat() if record.created_at else None,
                        record.processed_at.isoformat() if record.processed_at else None,
                    ),
                )

    async def save_job(self, job: ProcessingJob) -> None:
        await db_manager.execute(
            """
            INSERT INTO processing_jobs
                (job_id, pipeline, status, records_in, records_out, error, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.job_id,
                job.pipeline,
                job.status.value,
                job.records_in,
                job.records_out,
                job.error,
                job.created_at.isoformat() if job.created_at else None,
            ),
        )
        await db_manager.commit()

    async def update_job(self, job: ProcessingJob) -> None:
        await db_manager.execute(
            """
            UPDATE processing_jobs
            SET status=?, records_out=?, error=?, finished_at=?
            WHERE job_id=?
            """,
            (
                job.status.value,
                job.records_out,
                job.error,
                job.finished_at.isoformat() if job.finished_at else None,
                job.job_id,
            ),
        )
        await db_manager.commit()

    async def get_records(
        self,
        source: Optional[str] = None,
        record_type: Optional[str] = None,
        status: Optional[ProcessingStatus] = None,
        limit: int = 100,
    ) -> list[dict]:
        conditions = []
        params: list = []
        if source:
            conditions.append("source = ?")
            params.append(source)
        if record_type:
            conditions.append("record_type = ?")
            params.append(record_type)
        if status:
            conditions.append("status = ?")
            params.append(status.value)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)
        return await db_manager.fetchall(
            f"SELECT * FROM data_records {where} ORDER BY created_at DESC LIMIT ?",
            tuple(params),
        )

    async def get_job(self, job_id: str) -> Optional[dict]:
        return await db_manager.fetchone(
            "SELECT * FROM processing_jobs WHERE job_id = ?",
            (job_id,),
        )
