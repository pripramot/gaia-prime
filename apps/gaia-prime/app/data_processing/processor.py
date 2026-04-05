"""Core data processor — transform, validate, normalise records."""
import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from app.data_processing.schema import DataRecord, ProcessingStatus
from gaia_shared.logging import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """
    Stateless data processor for GAIA PRIME Ring-Forge.

    Responsibilities:
    - Validate incoming raw records
    - Normalise field values
    - Compute SHA-256 checksums
    - Classify record types
    """

    SUPPORTED_TYPES: set[str] = {
        "forensic_event",
        "tactical_intel",
        "tracking_point",
        "cyber_alert",
        "vehicle_event",
        "audit_log",
    }

    def process(self, record: DataRecord) -> DataRecord:
        """Validate, normalise, and checksum a single DataRecord."""
        self._validate(record)
        normalised_payload = self._normalise(record.payload)
        record.payload = normalised_payload
        record.checksum = self._compute_checksum(normalised_payload)
        record.status = ProcessingStatus.completed
        record.processed_at = datetime.now(tz=timezone.utc)
        logger.info("Processed record source=%s type=%s", record.source, record.record_type)
        return record

    def process_batch(self, records: list[DataRecord]) -> list[DataRecord]:
        """Process a batch of DataRecords, skipping failures."""
        results: list[DataRecord] = []
        for record in records:
            try:
                results.append(self.process(record))
            except Exception as exc:
                logger.warning(
                    "Skipping record source=%s reason=%s", record.source, exc
                )
                record.status = ProcessingStatus.failed
                results.append(record)
        return results

    def _validate(self, record: DataRecord) -> None:
        if not record.source:
            raise ValueError("DataRecord.source must not be empty")
        if record.record_type not in self.SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported record_type '{record.record_type}'. "
                f"Allowed: {sorted(self.SUPPORTED_TYPES)}"
            )
        if not isinstance(record.payload, dict):
            raise TypeError("DataRecord.payload must be a dict")
        if not record.payload:
            raise ValueError("DataRecord.payload must not be empty")

    def _normalise(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Normalise payload: strip whitespace from string values."""
        return {
            k: (v.strip() if isinstance(v, str) else v)
            for k, v in payload.items()
        }

    def _compute_checksum(self, payload: dict[str, Any]) -> str:
        """Compute deterministic SHA-256 checksum of a payload dict."""
        serialised = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(serialised.encode("utf-8")).hexdigest()
