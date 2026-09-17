def deduplicate_events(events):
    """Keep the first event for each event_id while preserving order."""
    seen = set()
    unique = []

    for event in events:
        if event.event_id in seen:
            continue
        seen.add(event.event_id)
        unique.append(event)

    return unique
