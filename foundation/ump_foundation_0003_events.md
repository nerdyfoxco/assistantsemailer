
# UMP-FOUNDATION-0003: Domain Events & Bus

**Module**: `foundation.events`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: `foundation.common`

## 1. Objective
Establish the **Event-Driven Architecture** primitives. All inter-module communication ("Pipes") that is not a direct function call must be an Event. This ensures decoupling between Spine and Organs.

## 2. Proposed Interface

### A. Domain Event (`foundation.events.base`)
```python
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class DomainEvent(BaseModel):
    """
    Base class for ALL system events.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    tenant_id: str = "default"
    producer: str # e.g., "spine.core", "brain.triage"
    payload: dict # or specific Pydantic models in subclasses
```

### B. Event Bus Contract (`foundation.events.bus`)
```python
from abc import ABC, abstractmethod
from typing import Callable, Awaitable

EventHandler = Callable[[DomainEvent], Awaitable[None]]

class EventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent):
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler: EventHandler):
        pass

class InMemoryEventBus(EventBus):
    """
    Simple in-memory bus for Phase 0 and Unit Tests.
    """
    ...
```

## 3. Implementation Plan
1.  **Create** `foundation/events/base.py`.
2.  **Create** `foundation/events/bus.py`.
3.  **Test** `foundation/tests/test_events.py`.

## 4. Verification
*   **Unit Test**: Publish an event and verify subscriber receives it.
*   **Constraint**: `event_type` must be present.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
