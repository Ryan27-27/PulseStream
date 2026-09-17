from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MessageType(str, Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    VOICE = "voice"
    PUSH = "push"


class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class CommunicationEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    customer_id: str = Field(min_length=1, max_length=128)
    message_type: MessageType
    region: str = Field(min_length=1, max_length=64)
    event_timestamp: datetime
    status: DeliveryStatus
    latency_ms: int = Field(ge=0)
    payload_bytes: int = Field(ge=0)
    error_code: Optional[str] = None

    @field_validator("region")
    @classmethod
    def normalize_region(cls, value: str) -> str:
        return value.strip().lower()
