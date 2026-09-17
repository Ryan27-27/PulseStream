import json
import os
from typing import Any

from fastapi import FastAPI, HTTPException, status

from src.pulsestream.models import CommunicationEvent

app = FastAPI(title="PulseStream Ingestion API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ingestion"}


@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
def ingest_event(event: CommunicationEvent) -> dict[str, Any]:
    """
    Development-mode ingestion endpoint.

    In the full deployment, this function publishes the serialized event
    to RabbitMQ before returning 202 Accepted. Keeping the broker boundary
    isolated makes the API testable without requiring infrastructure.
    """
    return {
        "accepted": True,
        "event_id": event.event_id,
        "message": "Event accepted for asynchronous processing",
    }


@app.post("/events/batch", status_code=status.HTTP_202_ACCEPTED)
def ingest_batch(events: list[CommunicationEvent]) -> dict[str, Any]:
    if not events:
        raise HTTPException(status_code=400, detail="Batch cannot be empty")

    return {
        "accepted": True,
        "count": len(events),
        "event_ids": [event.event_id for event in events],
    }
