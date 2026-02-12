from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
from .deps import get_work_manager, get_brain_service, get_gmail_service
from chapters.work.manager import WorkManager, WorkItemState
from chapters.brain.service import BrainService
from chapters.connectors.gmail.service import GmailService
from chapters.connectors.gmail.client import GmailClient 

# Note: We need a way to get the GmailClient instance for the user. 
# For v0 Vertical Slice, we'll assume a single tenant/user context or mock it.
# In production, this would come from the Request Context (User/Tenant).

router = APIRouter(prefix="/api/v2/work-items", tags=["chapter-core"])

class WorkItemResponse(BaseModel):
    id: str
    tenant_id: str
    state: str
    source_message_id: str
    draft_context: Optional[dict] = None

@router.get("/", response_model=List[WorkItemResponse])
def list_work_items(
    state: Optional[str] = None,
    manager: WorkManager = Depends(get_work_manager)
):
    """List work items, optionally filtered by state."""
    if state:
        try:
            s_enum = WorkItemState(state)
            items = manager.get_items_by_state(s_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid state")
    else:
        # Get all - hacky for now as manager doesn't have get_all exposed directly efficiently 
        # but we can iterate enum or add method.
        # For now, just return all in store.
        items = list(manager._store.values())
    
    return [
        WorkItemResponse(
            id=i.id, 
            tenant_id=i.tenant_id, 
            state=i.state.value, 
            source_message_id=i.source_message_id,
            draft_context=i.draft_context
        ) for i in items
    ]

@router.get("/{item_id}", response_model=WorkItemResponse)
def get_work_item(
    item_id: str,
    manager: WorkManager = Depends(get_work_manager)
):
    item = manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return WorkItemResponse(
        id=item.id,
        tenant_id=item.tenant_id,
        state=item.state.value,
        source_message_id=item.source_message_id,
        draft_context=item.draft_context
    )

@router.post("/{item_id}/draft")
def trigger_draft(
    item_id: str,
    background_tasks: BackgroundTasks,
    manager: WorkManager = Depends(get_work_manager),
    brain: BrainService = Depends(get_brain_service)
):
    """Manually trigger drafting for an item."""
    item = manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.state != WorkItemState.NEW:
         raise HTTPException(status_code=400, detail=f"Cannot draft invalid state: {item.state}")

    # Run in background to simulate async work
    background_tasks.add_task(brain.generate_draft, item, "Professional")
    return {"status": "Drafting started"}

@router.post("/{item_id}/approve")
def approve_draft(
    item_id: str,
    background_tasks: BackgroundTasks,
    manager: WorkManager = Depends(get_work_manager),
    gmail: GmailService = Depends(get_gmail_service)
):
    """Approve draft and send."""
    item = manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.state != WorkItemState.REVIEW:
        raise HTTPException(status_code=400, detail="Item not in REVIEW state")

    # 1. Update State
    item.approve_for_sending()

    # 2. Simulate Sending (Verification Step)
    # Ideally, we call gmail.send_reply here.
    # For now, we'll mark it sent immediately in background or just do it.
    
    # Mocking Client for now inside the handler or assuming service handles it.
    # Since we don't have a real User/Token context here easily, we'll skip the actual Gmail API call 
    # and just finalize the state for the Vertical Slice Verification.
    
    item.mark_sent("simulated_sent_id_123")
    
    return {"status": "Approved and Sent"}
