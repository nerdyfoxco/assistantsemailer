from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from spine.db.database import get_db
from spine.chapters.hitl.models import HitlRequest, HitlDecision, HitlState
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/hitl", tags=["hitl"])

class HitlRequestRead(BaseModel):
    id: str
    tenant_id: str
    work_item_id: str
    reason: str
    state: HitlState
    created_at: datetime
    claimed_by_agent_id: Optional[str]

    class Config:
        orm_mode = True

class HitlDecisionCreate(BaseModel):
    request_id: str
    agent_id: str
    outcome: HitlState
    modified_draft: Optional[str] = None
    feedback_notes: Optional[str] = None

@router.get("/queue", response_model=List[HitlRequestRead])
async def get_queue(tenant_id: str, db: AsyncSession = Depends(get_db)):
    # In real auth, tenant_id comes from token
    stmt = select(HitlRequest).where(
        HitlRequest.tenant_id == tenant_id,
        HitlRequest.state == HitlState.PENDING
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/claim/{request_id}")
async def claim_request(request_id: str, agent_id: str, db: AsyncSession = Depends(get_db)):
    # Check if exists
    stmt = select(HitlRequest).where(HitlRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalars().first()
    
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if req.state != HitlState.PENDING:
        raise HTTPException(status_code=409, detail=f"Request is {req.state}")
        
    req.state = HitlState.CLAIMED
    req.claimed_by_agent_id = agent_id
    req.claimed_at = datetime.utcnow()
    await db.commit()
    await db.refresh(req)
    return {"status": "claimed", "request_id": req.id}

@router.post("/resolve")
async def resolve_request(decision: HitlDecisionCreate, db: AsyncSession = Depends(get_db)):
    # 1. Validate Request State
    stmt = select(HitlRequest).where(HitlRequest.id == decision.request_id)
    result = await db.execute(stmt)
    req = result.scalars().first()
    
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
        
    if req.state != HitlState.CLAIMED:
        raise HTTPException(status_code=409, detail="Request must be CLAIMED before resolution")
        
    # 2. Create Decision Record
    dec = HitlDecision(
        id=f"dec_{datetime.utcnow().timestamp()}",
        request_id=decision.request_id,
        agent_id=decision.agent_id,
        outcome=decision.outcome,
        modified_draft=decision.modified_draft,
        feedback_notes=decision.feedback_notes
    )
    db.add(dec)
    await db.flush() # Get ID if needed, ensure constraint
    
    # 3. Update Request State
    req.state = decision.outcome
    req.resolved_at = datetime.utcnow()
    
    # 4. Resolve WorkItem via Resolver
    from spine.chapters.hitl.resolver import HitlResolver
    resolver = HitlResolver(db)
    await resolver.apply_decision(dec)
    
    await db.commit()
    return {"status": "resolved"}
