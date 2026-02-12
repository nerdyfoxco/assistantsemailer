from enum import Enum, auto
from typing import Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

class WorkItemState(Enum):
    NEW = "NEW"
    DRAFTING = "DRAFTING"
    REVIEW = "REVIEW"
    SENDING = "SENDING"
    CLOSED = "CLOSED"

class WorkItem:
    """
    Represents a unit of work (an email needing a reply).
    Manages state transitions.
    """
    def __init__(self, tenant_id: str, source_message_id: str, payload: Dict[str, Any]):
        self.id = str(uuid4())
        self.tenant_id = tenant_id
        self.source_message_id = source_message_id
        self.payload = payload
        self.state = WorkItemState.NEW
        self.created_at = datetime.utcnow()
        self.draft_context: Optional[Dict[str, Any]] = None
        self.result_message_id: Optional[str] = None

    def start_drafting(self):
        if self.state != WorkItemState.NEW:
            raise ValueError(f"Cannot draft from state {self.state}")
        self.state = WorkItemState.DRAFTING

    def draft_complete(self, draft: Dict[str, Any]):
        if self.state != WorkItemState.DRAFTING:
            raise ValueError(f"Cannot complete draft from state {self.state}")
        self.draft_context = draft
        self.state = WorkItemState.REVIEW

    def approve_for_sending(self):
        if self.state != WorkItemState.REVIEW:
            raise ValueError(f"Cannot send from state {self.state}")
        self.state = WorkItemState.SENDING

    def mark_sent(self, result_message_id: str):
        if self.state != WorkItemState.SENDING:
            raise ValueError(f"Cannot mark sent from state {self.state}")
        self.result_message_id = result_message_id
        self.state = WorkItemState.CLOSED
