import json
from pathlib import Path

import pytest

pyspark = pytest.importorskip("pyspark")


def test_sample_data_file_can_be_read():
    path = Path("data/raw/events.jsonl")
    if not path.exists():
        pytest.skip("Generate data first with scripts/generate_events.py")
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines
    assert "event_id" in json.loads(lines[0])
