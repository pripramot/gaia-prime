"""Data ingestion module — receive raw data from internal services."""
from datetime import datetime, timezone
from typing import Any

from app.data_processing.schema import DataRecord, ProcessingStatus
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


class DataIngester:
    """
    Accepts raw payloads from internal Ring-Forge services and
    converts them to DataRecord instances for the pipeline.
    """

    def ingest(
        self,
        source: str,
        record_type: str,
        payload: dict[str, Any],
    ) -> DataRecord:
        record = DataRecord(
            source=source,
            record_type=record_type,
            payload=payload,
            status=ProcessingStatus.raw,
            created_at=datetime.now(tz=timezone.utc),
        )
        logger.info("Ingested record source=%s type=%s", source, record_type)
        return record

    def ingest_batch(
        self,
        source: str,
        record_type: str,
        payloads: list[dict[str, Any]],
    ) -> list[DataRecord]:
        return [self.ingest(source, record_type, p) for p in payloads]
