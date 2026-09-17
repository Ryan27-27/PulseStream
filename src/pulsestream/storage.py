from pathlib import Path
import json
import pandas as pd


def event_to_record(event) -> dict:
    record = event.model_dump(mode="json")
    record["event_date"] = event.event_timestamp.date().isoformat()
    record["is_successful"] = event.status.value == "delivered"
    record["latency_bucket"] = latency_bucket(event.latency_ms)
    return record


def latency_bucket(latency_ms: int) -> str:
    if latency_ms <= 100:
        return "0-100ms"
    if latency_ms <= 500:
        return "101-500ms"
    if latency_ms <= 1000:
        return "501-1000ms"
    if latency_ms <= 5000:
        return "1001-5000ms"
    return "5000ms+"


def write_jsonl(records: list[dict], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, default=str) + "\n")


def write_parquet(records: list[dict], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_parquet(path, index=False)
