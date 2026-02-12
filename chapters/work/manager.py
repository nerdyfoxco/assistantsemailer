from typing import Dict, Literal
from foundation.events.bus import EventBus
from foundation.events.base import DomainEvent 
from chapters.connectors.gmail.service import EmailIngested # Import Event
from .item import WorkItem, WorkItemState

class WorkItemCreated(DomainEvent):
    event_type: Literal["work.item.created"] = "work.item.created"
    producer: Literal["work.manager"] = "work.manager"
    work_item_id: str
    # tenant_id inherited

class WorkManager:
    """
    Orchestrates the creation and processing of WorkItems.
    """
    def __init__(self, bus: EventBus):
        self.bus = bus
        # In-Memory Store for Phase 1 Vertical Slice (Bootstrap)
        self._store: Dict[str, WorkItem] = {}

    def handle_email_ingested(self, event: EmailIngested):
        # Idempotency check (simple)
        exisiting = [w for w in self._store.values() if w.source_message_id == event.message_id]
        if exisiting:
            return exisiting[0]

        # Create WorkItem (Transient - No Body Persistence in DB yet)
        item = WorkItem(
            tenant_id=event.tenant_id,
            source_message_id=event.message_id,
            payload=event.payload # Todo: In V2, scrub this to just metadata to enforce "No Storage"
        )
        self._store[item.id] = item
        
        # Publish Event
        # self.bus.publish(WorkItemCreated(work_item_id=item.id, tenant_id=item.tenant_id))
        
        return item

    def get_items_by_state(self, state: WorkItemState):
        return [w for w in self._store.values() if w.state == state]
    
    def get_item(self, item_id: str):
        return self._store.get(item_id)
