import uuid
import json
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from spine.chapters.hitl.models import HitlRequest, HitlState
from spine.db.models import WorkItem, WorkItemState

class EscalationQueue:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_for_review(self, work_item: WorkItem, reason: str, context: dict) -> HitlRequest:
        """
        Moves a WorkItem to NEEDS_REVIEW and creates a HitlRequest.
        """
        # 1. Update WorkItem state
        work_item.state = WorkItemState.NEEDS_REVIEW
        
        # 2. Create Request
        request_id = f"hitl_{uuid.uuid4().hex[:12]}"
        req = HitlRequest(
            id=request_id,
            tenant_id=work_item.tenant_id,
            work_item_id=work_item.id,
            reason=reason,
            context_json=json.dumps(context),
            state=HitlState.PENDING
        )
        
        self.db.add(req)
        # We flush to ensure ID generation/constraints, but commit is usually caller's job.
        # However, for this specific flow, we might want to ensure it's persisted.
        await self.db.flush()
        return req

    async def get_pending_requests(self, tenant_id: str) -> List[HitlRequest]:
        stmt = select(HitlRequest).where(
            HitlRequest.tenant_id == tenant_id,
            HitlRequest.state == HitlState.PENDING
        ).order_by(HitlRequest.created_at.asc())
        
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def claim_request(self, request_id: str, agent_id: str) -> Optional[HitlRequest]:
        stmt = select(HitlRequest).where(HitlRequest.id == request_id)
        result = await self.db.execute(stmt)
        req = result.scalars().first()
        
        if not req:
            return None
            
        if req.state != HitlState.PENDING:
            raise ValueError(f"Request is {req.state}, cannot claim.")
            
        req.state = HitlState.CLAIMED
        req.claimed_by_agent_id = agent_id
        req.claimed_at = datetime.utcnow()
        await self.db.flush()
        return req
