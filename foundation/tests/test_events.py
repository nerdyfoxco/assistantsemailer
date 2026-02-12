import pytest
from foundation.events.base import DomainEvent
from foundation.events.bus import InMemoryEventBus
from datetime import datetime

# Mock event for testing
class UserSignedUp(DomainEvent):
    event_type: str = "user.signed_up"
    producer: str = "auth.service"

@pytest.mark.asyncio
async def test_domain_event_structure():
    event = DomainEvent(
        event_type="test.event",
        producer="test.producer",
        payload={"foo": "bar"}
    )
    assert event.event_id is not None
    assert isinstance(event.timestamp, datetime)
    assert event.payload["foo"] == "bar"

@pytest.mark.asyncio
async def test_in_memory_bus_pub_sub():
    bus = InMemoryEventBus()
    received_events = []

    async def handler(event: DomainEvent):
        received_events.append(event)

    # Subscribe
    await bus.subscribe("user.signed_up", handler)

    # Publish
    event = UserSignedUp(payload={"user_id": "123"})
    await bus.publish(event)

    # Verify
    assert len(received_events) == 1
    assert received_events[0].event_type == "user.signed_up"
    assert received_events[0].payload["user_id"] == "123"

@pytest.mark.asyncio
async def test_bus_handler_exception_isolation():
    bus = InMemoryEventBus()
    ack = []

    async def faulty_handler(event: DomainEvent):
        raise ValueError("Boom")

    async def working_handler(event: DomainEvent):
        ack.append("ok")

    # Subscribe both
    await bus.subscribe("test.error", faulty_handler)
    await bus.subscribe("test.error", working_handler)

    # Publish
    event = DomainEvent(event_type="test.error", producer="test", payload={})
    await bus.publish(event)

    # Verify working handler still ran despite faulty handler crashing
    assert len(ack) == 1
    assert ack[0] == "ok"
