from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from spine.chapters.hitl.models import HitlDecision, HitlState
from spine.db.models import WorkItem, WorkItemState, ConfidenceBand

class HitlResolver:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def apply_decision(self, decision: HitlDecision) -> WorkItem:
        """
        Applies the HITL decision to the associated WorkItem.
        Returns the updated WorkItem.
        """
        # 1. Fetch Request to get WorkItem ID
        # Since HitlDecision is linked to HitlRequest, we need to join or fetch request first.
        # But wait, HitlDecision has request_id. HitlRequest has work_item_id.
        
        # Let's fetch the Request first (we could optimize with a join)
        from spine.chapters.hitl.models import HitlRequest
        req_stmt = select(HitlRequest).where(HitlRequest.id == decision.request_id)
        result = await self.db.execute(req_stmt)
        req = result.scalars().first()
        
        if not req:
            raise ValueError(f"Request {decision.request_id} not found")
            
        # 2. Fetch WorkItem
        wi_stmt = select(WorkItem).where(WorkItem.id == req.work_item_id)
        wi_result = await self.db.execute(wi_stmt)
        work_item = wi_result.scalars().first()
        
        if not work_item:
            raise ValueError(f"WorkItem {req.work_item_id} not found")
            
        # 3. Apply Outcome Logic
        if decision.outcome == HitlState.RESOLVED:
            # Human Approved or Edited. 
            # If draft was modified, we should probably update the draft in the system.
            # But where is the draft stored? WorkItem usually links to generated artifacts or is the artifact container.
            # For now, we update state to NEEDS_REPLY (so Strategist picks it up) 
            # Or if it's fully approved, maybe we mark it ready to send?
            # Let's assume for v0: Moves back to 'NEEDS_REPLY' but with 'HIGH' confidence so it bypasses checks?
            # Or we add a APPROVED_BY_HITL state?
            # Let's stick to existing states. NEEDS_REPLY is good. Strategist will see it's unblocked.
            
            work_item.state = WorkItemState.NEEDS_REPLY
            work_item.confidence_band = ConfidenceBand.HIGH # Boost confidence
            work_item.resolution_lock = True # Prevent AI from overwriting human decision
            
            # If there is a modified draft, we might need to store it.
            # For this UMP, simply unblocking is the key. 
            # In a real system, we'd save the draft to a `Draft` table or `WorkItem.payload`.
            
        elif decision.outcome == HitlState.REJECTED:
             # Human said "No".
             # Could mean "Don't reply" or "Do something else".
             # Let's mark as DONE (Manual Close) or FYI.
             work_item.state = WorkItemState.DONE
             work_item.closed_at = datetime.utcnow()
             
        # 4. Save
        await self.db.flush()
        return work_item
