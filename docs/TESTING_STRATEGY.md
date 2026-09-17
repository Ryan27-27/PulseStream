# Testing Strategy

## Test pyramid

```text
             /\
            /  \
           /Load\
          /------\
         / Integ. \
        /----------\
       / Unit Tests \
      /--------------\
```

## Unit tests

Fast deterministic tests validate pure logic:

- Pydantic schema constraints
- Region normalization
- Deduplication
- Latency buckets
- Delivery-rate calculation
- Percentile calculations

## Integration tests

Integration tests should run against:

- RabbitMQ test container
- PostgreSQL test container
- Local Spark session
- Temporary Parquet directories

## Performance tests

Measure:

- API p50/p95/p99 latency
- Events per second
- Worker throughput
- Queue backlog
- Spark runtime
- Input size versus runtime
- Partitioning strategy

Record every benchmark with:

- Commit hash
- Dataset size
- Hardware
- Python version
- Spark version
- Configuration
- Runtime
- Peak memory
