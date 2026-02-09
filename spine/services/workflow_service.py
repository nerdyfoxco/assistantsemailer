from datetime import datetime
from typing import Optional
from spine.db.models import WorkItem, WorkItemState, ConfidenceBand
from spine.repositories.work_item_repo import WorkItemRepository

class WorkflowService:
    def __init__(self, work_item_repo: WorkItemRepository):
        self.repo = work_item_repo

    async def create_work_item(
        self,
        id: str,
        tenant_id: str,
        email_id: str,
        confidence: ConfidenceBand
    ) -> WorkItem:
        # Initial State Logic
        initial_state = WorkItemState.NEEDS_REPLY
        # If very low confidence, maybe NEEDS_REVIEW? (Logic for later)
        
        item = await self.repo.create(
            id=id,
            tenant_id=tenant_id,
            email_id=email_id,
            state=initial_state,
            owner_type="SYSTEM",
            confidence_band=confidence,
            created_at=datetime.utcnow()
        )
        return item

    async def transition_state(self, item_id: str, new_state: WorkItemState, actor_id: str) -> Optional[WorkItem]:
        item = await self.repo.get_by_id(item_id)
        if not item:
            return None
            
        # State Machine Validation (Simplistic for Phase 2)
        # e.g. Cannot go from DONE back to NEEDS_REPLY without verify
        
        item.state = new_state
        if new_state == WorkItemState.DONE:
            item.closed_at = datetime.utcnow()
            
        # Lock handling
        if new_state in [WorkItemState.WAITING, WorkItemState.DONE]:
             item.resolution_lock = True
        else:
             item.resolution_lock = False

        self.repo.session.add(item)
        # Session commit managed by caller/controller usually
        return item
