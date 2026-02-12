from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Any, Dict

class DomainEvent(BaseModel):
    """
    Base class for ALL system events.
    Ensures standard envelope for traceability and routing.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    tenant_id: str = "default"
    producer: str # e.g., "spine.core", "brain.triage"
    payload: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        frozen = True # Events are immutable once created
