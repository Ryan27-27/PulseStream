import pytest
from pydantic import ValidationError

from src.pulsestream.models import CommunicationEvent
from src.pulsestream.validation import validate_events


def valid_payload():
    return {
        "event_id": "evt_1",
        "customer_id": "cust_1",
        "message_type": "sms",
        "region": "AP-SOUTH-1",
        "event_timestamp": "2026-09-17T10:30:00Z",
        "status": "delivered",
        "latency_ms": 120,
        "payload_bytes": 500,
    }


def test_valid_event_is_accepted():
    event = CommunicationEvent.model_validate(valid_payload())
    assert event.event_id == "evt_1"
    assert event.region == "ap-south-1"


def test_negative_latency_is_rejected():
    payload = valid_payload()
    payload["latency_ms"] = -1

    with pytest.raises(ValidationError):
        CommunicationEvent.model_validate(payload)


def test_invalid_status_is_rejected():
    payload = valid_payload()
    payload["status"] = "unknown"

    with pytest.raises(ValidationError):
        CommunicationEvent.model_validate(payload)


def test_validation_report_counts_rejected_records():
    payload = valid_payload()
    invalid = {**payload, "latency_ms": -10}

    valid, rejected, report = validate_events([payload, invalid])

    assert len(valid) == 1
    assert len(rejected) == 1
    assert report["invalid_records"] == 1
