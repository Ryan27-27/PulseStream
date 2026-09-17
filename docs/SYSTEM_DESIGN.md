# System Design

## Requirements

### Functional

1. Accept communication events.
2. Validate event structure and values.
3. Process events asynchronously.
4. Avoid duplicate processing.
5. Persist valid and rejected records separately.
6. Produce analytical metrics.
7. Expose metrics through an API.

### Non-functional

- Low ingestion latency
- Horizontal worker scalability
- At-least-once message delivery with idempotent processing
- Observability
- Testability
- Failure isolation
- Local developer reproducibility

## Reliability model

PulseStream uses an **at-least-once processing model**:

1. RabbitMQ may redeliver a message.
2. The worker deduplicates by `event_id`.
3. The message is acknowledged after processing.
4. Temporary failures can be retried.
5. Permanent failures should be routed to a dead-letter queue.

This is more realistic than claiming exactly-once processing without a transactional sink.

## Scaling strategy

- Scale ingestion API instances horizontally.
- Increase worker count based on queue depth.
- Partition Parquet by event date and region.
- Tune Spark shuffle partitions according to data size.
- Cache frequently requested aggregate results in Redis.
- Move from local Parquet to HDFS or object storage for multi-node deployment.

## Failure scenarios

| Failure | Expected behavior |
|---|---|
| Invalid event | Reject and record quality reason |
| Duplicate event | Ignore duplicate after first successful processing |
| Worker exception | Retry with bounded attempts |
| Persistent failure | Route to dead-letter queue |
| Spark job failure | Preserve previous report and alert operator |
| Database unavailable | Retry analytics sink or serve stale report |
