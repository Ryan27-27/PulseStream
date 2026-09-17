from locust import HttpUser, between, task


class IngestionUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def send_event(self):
        self.client.post(
            "/events",
            json={
                "event_id": f"load-{self.environment.runner.user_count}",
                "customer_id": "load-customer",
                "message_type": "sms",
                "region": "ap-south-1",
                "event_timestamp": "2026-09-17T10:30:00Z",
                "status": "delivered",
                "latency_ms": 120,
                "payload_bytes": 512,
            },
        )
