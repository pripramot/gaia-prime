"""Unit tests for DataProcessor."""
import pytest

from app.data_processing.processor import DataProcessor
from app.data_processing.schema import DataRecord, ProcessingStatus


@pytest.fixture
def processor() -> DataProcessor:
    return DataProcessor()


def make_record(**kwargs) -> DataRecord:
    defaults = dict(
        source="test-service",
        record_type="audit_log",
        payload={"event": "login", "user": "admin"},
    )
    defaults.update(kwargs)
    return DataRecord(**defaults)


class TestDataProcessorValidation:
    def test_rejects_empty_source(self, processor):
        with pytest.raises(ValueError, match="source"):
            processor.process(make_record(source=""))

    def test_rejects_unknown_record_type(self, processor):
        with pytest.raises(ValueError, match="Unsupported record_type"):
            processor.process(make_record(record_type="unknown_type"))

    def test_rejects_empty_payload(self, processor):
        with pytest.raises(ValueError, match="payload must not be empty"):
            processor.process(make_record(payload={}))

    def test_rejects_non_dict_payload(self, processor):
        record = make_record()
        record.payload = "not-a-dict"  # type: ignore[assignment]
        with pytest.raises(TypeError, match="payload must be a dict"):
            processor.process(record)


class TestDataProcessorProcessing:
    def test_successful_processing_sets_status_completed(self, processor):
        record = processor.process(make_record())
        assert record.status == ProcessingStatus.completed

    def test_checksum_is_sha256_hex(self, processor):
        record = processor.process(make_record())
        assert record.checksum is not None
        assert len(record.checksum) == 64
        assert all(c in "0123456789abcdef" for c in record.checksum)

    def test_checksum_is_deterministic(self, processor):
        r1 = processor.process(make_record(payload={"a": "1"}))
        r2 = processor.process(make_record(payload={"a": "1"}))
        assert r1.checksum == r2.checksum

    def test_checksum_differs_for_different_payloads(self, processor):
        r1 = processor.process(make_record(payload={"a": "1"}))
        r2 = processor.process(make_record(payload={"a": "2"}))
        assert r1.checksum != r2.checksum

    def test_normalisation_strips_whitespace(self, processor):
        record = processor.process(make_record(payload={"key": "  value  "}))
        assert record.payload["key"] == "value"

    def test_processed_at_is_set(self, processor):
        record = processor.process(make_record())
        assert record.processed_at is not None

    @pytest.mark.parametrize("record_type", list(DataProcessor.SUPPORTED_TYPES))
    def test_all_supported_types_accepted(self, processor, record_type):
        record = processor.process(make_record(record_type=record_type))
        assert record.status == ProcessingStatus.completed


class TestDataProcessorBatch:
    def test_batch_returns_all_records(self, processor):
        records = [make_record(payload={"n": i}) for i in range(5)]
        results = processor.process_batch(records)
        assert len(results) == 5

    def test_batch_marks_failed_on_invalid(self, processor):
        records = [
            make_record(payload={"n": 1}),
            make_record(record_type="bad_type", payload={"n": 2}),
            make_record(payload={"n": 3}),
        ]
        results = processor.process_batch(records)
        statuses = [r.status for r in results]
        assert statuses[0] == ProcessingStatus.completed
        assert statuses[1] == ProcessingStatus.failed
        assert statuses[2] == ProcessingStatus.completed
