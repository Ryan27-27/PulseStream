import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

MESSAGE_TYPES = ["sms", "whatsapp", "email", "voice", "push"]
REGIONS = ["ap-south-1", "us-east-1", "eu-west-1"]
STATUSES = ["queued", "sent", "delivered", "failed"]


def generate_event(index: int) -> dict:
    status = random.choices(STATUSES, weights=[5, 10, 80, 5])[0]
    latency = random.randint(20, 5000)
    return {
        "event_id": f"evt_{index:08d}",
        "customer_id": f"cust_{random.randint(1, 1000):05d}",
        "message_type": random.choice(MESSAGE_TYPES),
        "region": random.choice(REGIONS),
        "event_timestamp": (
            datetime.now(timezone.utc) - timedelta(seconds=random.randint(0, 86400))
        ).isoformat(),
        "status": status,
        "latency_ms": latency,
        "payload_bytes": random.randint(100, 5000),
        "error_code": random.choice([None, None, None, "TIMEOUT", "PROVIDER_5XX"])
        if status == "failed"
        else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--output", default="data/raw/events.jsonl")
    args = parser.parse_args()

    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for index in range(args.count):
            handle.write(json.dumps(generate_event(index)) + "\n")

    print(f"Generated {args.count} events at {path}")


if __name__ == "__main__":
    main()
