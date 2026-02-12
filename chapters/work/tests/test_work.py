import pytest
from chapters.work.item import WorkItem, WorkItemState
from chapters.work.manager import WorkManager, WorkItemCreated
from chapters.connectors.gmail.service import EmailIngested
from foundation.events.bus import InMemoryEventBus

def test_work_item_state_machine():
    item = WorkItem("t1", "msg1", {})
    assert item.state == WorkItemState.NEW

    item.start_drafting()
    assert item.state == WorkItemState.DRAFTING

    item.draft_complete({"params": "draft"})
    assert item.state == WorkItemState.REVIEW
    assert item.draft_context == {"params": "draft"}

    item.approve_for_sending()
    assert item.state == WorkItemState.SENDING

    item.mark_sent("new_msg_id")
    assert item.state == WorkItemState.CLOSED
    assert item.result_message_id == "new_msg_id"

def test_work_item_invalid_transitions():
    item = WorkItem("t1", "msg1", {})
    with pytest.raises(ValueError):
        item.draft_complete({}) # Skip drafting state

def test_work_manager_ingestion():
    bus = InMemoryEventBus()
    manager = WorkManager(bus)
    
    event = EmailIngested("t1", "msg123", "snippet", {})
    item = manager.handle_email_ingested(event)

    assert item.id is not None
    assert item.state == WorkItemState.NEW
    assert item.source_message_id == "msg123"
    
    # Verify Store
    stored = manager.get_item(item.id)
    assert stored == item
