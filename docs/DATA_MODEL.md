# Data Model

## CommunicationEvent

| Field | Type | Rules |
|---|---|---|
| event_id | string | Required, unique logical identifier |
| customer_id | string | Required |
| message_type | enum | sms, whatsapp, email, voice, push |
| region | string | Normalized lowercase |
| event_timestamp | timestamp | Required |
| status | enum | queued, sent, delivered, failed |
| latency_ms | integer | Must be non-negative |
| payload_bytes | integer | Must be non-negative |
| error_code | string/null | Usually populated for failures |

## Derived fields

- `event_date`
- `is_successful`
- `latency_bucket`

## Storage layout

```text
data/curated/events/
  event_date=YYYY-MM-DD/
    region=REGION/
      part-*.parquet
```
