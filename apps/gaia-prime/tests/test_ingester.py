"""Unit tests for DataIngester."""
import pytest

from app.data_processing.ingester import DataIngester
from app.data_processing.schema import ProcessingStatus


@pytest.fixture
def ingester() -> DataIngester:
    return DataIngester()


def test_ingest_returns_data_record(ingester):
    record = ingester.ingest("chronos", "tracking_point", {"lat": 17.5, "lon": 102.8})
    assert record.source == "chronos"
    assert record.record_type == "tracking_point"
    assert record.payload == {"lat": 17.5, "lon": 102.8}
    assert record.status == ProcessingStatus.raw
    assert record.created_at is not None


def test_ingest_batch_returns_correct_count(ingester):
    payloads = [{"n": i} for i in range(10)]
    records = ingester.ingest_batch("phuphadang", "forensic_event", payloads)
    assert len(records) == 10
    assert all(r.source == "phuphadang" for r in records)
    assert all(r.record_type == "forensic_event" for r in records)


def test_ingest_batch_empty_returns_empty(ingester):
    records = ingester.ingest_batch("unicorn", "cyber_alert", [])
    assert records == []
