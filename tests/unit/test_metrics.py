from src.pulsestream.metrics import delivery_rate, latency_summary
from src.pulsestream.storage import latency_bucket


def test_delivery_rate():
    assert delivery_rate(["delivered", "failed", "delivered"]) == 2 / 3


def test_latency_summary():
    result = latency_summary([100, 200, 300, 400, 500])
    assert result["p50"] == 300
    assert result["p95"] == 480


def test_latency_buckets():
    assert latency_bucket(50) == "0-100ms"
    assert latency_bucket(500) == "101-500ms"
    assert latency_bucket(5001) == "5000ms+"
