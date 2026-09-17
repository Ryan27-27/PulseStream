from statistics import mean


def delivery_rate(statuses) -> float:
    statuses = list(statuses)
    if not statuses:
        return 0.0
    return sum(status == "delivered" for status in statuses) / len(statuses)


def percentile(values, percentile_value: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    index = (len(values) - 1) * percentile_value
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    fraction = index - lower
    return values[lower] + (values[upper] - values[lower]) * fraction


def latency_summary(values) -> dict:
    values = list(values)
    return {
        "average": mean(values) if values else 0.0,
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "p99": percentile(values, 0.99),
    }
