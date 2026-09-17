from collections import Counter
from typing import Iterable

from .models import CommunicationEvent


def validate_events(events: Iterable[dict]) -> tuple[list[CommunicationEvent], list[dict], dict]:
    valid = []
    rejected = []
    reasons = Counter()

    for index, raw in enumerate(events):
        try:
            event = CommunicationEvent.model_validate(raw)
            valid.append(event)
        except Exception as exc:
            reason = type(exc).__name__
            reasons[reason] += 1
            rejected.append({"row": index, "raw": raw, "reason": reason})

    report = {
        "total_records": len(valid) + len(rejected),
        "valid_records": len(valid),
        "invalid_records": len(rejected),
        "rejection_reasons": dict(reasons),
    }
    return valid, rejected, report
