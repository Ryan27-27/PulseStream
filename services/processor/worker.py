"""
RabbitMQ worker boundary for PulseStream.

This module intentionally keeps broker-specific code small. In a production
deployment, replace `process_message` with a connection/channel lifecycle,
durable exchange and queue declarations, retry headers, and dead-letter
routing.
"""

from src.pulsestream.deduplication import deduplicate_events
from src.pulsestream.models import CommunicationEvent
from src.pulsestream.storage import event_to_record, write_jsonl


def process_message(payload: dict) -> dict:
    event = CommunicationEvent.model_validate(payload)
    return event_to_record(event)


def process_batch(payloads: list[dict]) -> list[dict]:
    events = [CommunicationEvent.model_validate(payload) for payload in payloads]
    return [event_to_record(event) for event in deduplicate_events(events)]


if __name__ == "__main__":
    print("PulseStream worker boundary loaded. Connect this module to RabbitMQ for deployment.")
