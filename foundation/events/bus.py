from abc import ABC, abstractmethod
from typing import Callable, Awaitable, List, Dict
from foundation.events.base import DomainEvent
import asyncio

# Type definition for event handlers
EventHandler = Callable[[DomainEvent], Awaitable[None]]

class EventBus(ABC):
    """
    Abstract contract for the Event Bus.
    Allows swapping InMemory for Redis/RabbitMQ later.
    """
    @abstractmethod
    async def publish(self, event: DomainEvent):
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler: EventHandler):
        pass

class InMemoryEventBus(EventBus):
    """
    Simple in-memory bus for Phase 0 and Unit Tests.
    WARNING: Not suitable for multi-process deployments.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[EventHandler]] = {}

    async def publish(self, event: DomainEvent):
        # 1. Get handlers for this event type
        handlers = self._subscribers.get(event.event_type, [])
        
        # 2. Also notify generic "*" listeners if we had them (YAGNI for now)
        
        # 3. Execute handlers asynchronously (but awaited here for simplicity in Phase 0)
        # In a real async bus, this might just push to a queue.
        # Here we await to ensure deterministic tests.
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                print(f"ERROR handling event {event.event_id}: {e}")
                # We do NOT re-raise to prevent blocking other handlers
                # In production, this goes to DLQ

    async def subscribe(self, event_type: str, handler: EventHandler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
