from src.pulsestream.deduplication import deduplicate_events
from src.pulsestream.models import CommunicationEvent


def event(event_id):
    return CommunicationEvent.model_validate({
        "event_id": event_id,
        "customer_id": "cust",
        "message_type": "sms",
        "region": "ap-south-1",
        "event_timestamp": "2026-09-17T10:30:00Z",
        "status": "delivered",
        "latency_ms": 100,
        "payload_bytes": 10,
    })


def test_deduplication_preserves_first_event():
    result = deduplicate_events([event("a"), event("a"), event("b")])
    assert [item.event_id for item in result] == ["a", "b"]
