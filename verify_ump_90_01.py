import asyncio
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.base import Base
from spine.chapters.hitl.queue import EscalationQueue
from spine.chapters.hitl.models import HitlRequest, HitlState
from spine.db.models import WorkItem, WorkItemState, Tenant, User, Email, EmailProvider, Direction, ConfidenceBand, TenantPlan, Role

async def verify_hitl_queue():
    print("=== VISUAL VERIFICATION: UMP-90-01 (Escalation Queue) ===")
    
    # 1. Setup In-Memory DB
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # 2. Setup Data
        print("[1/4] Seeding Data...")
        t1 = Tenant(id="t1", name="Visual Tenant", plan=TenantPlan.ENTERPRISE)
        u1 = User(id="u1", email="admin@visual.com")
        e1 = Email(id="e1", provider_message_id="m1", thread_id="th1", from_email="x@y.com", direction=Direction.INBOUND, received_at=datetime.utcnow(), gmail_id="g1")
        session.add(t1)
        session.add(u1)
        session.add(e1)
        await session.commit()
        
        wi = WorkItem(id="wi_visual", tenant_id="t1", email_id="e1", state=WorkItemState.NEEDS_REPLY, owner_type="USER", owner_id="u1", confidence_band=ConfidenceBand.LOW)
        session.add(wi)
        await session.commit()
        print(f"   Created WorkItem: {wi.id} (State: {wi.state})")
        
        # 3. Submit Escalation
        print("[2/4] Submitting Escalation...")
        queue = EscalationQueue(session)
        req = await queue.submit_for_review(wi, "Visual Verification Reason", {"context": "visual"})
        await session.commit()
        print(f"   Created HitlRequest: {req.id}")
        print(f"   WorkItem State Updated To: {wi.state}")
        
        # 4. Verify Persistence
        print("[3/4] Verifying Persistence...")
        pending = await queue.get_pending_requests("t1")
        if len(pending) == 1 and pending[0].id == req.id:
            print(f"   SUCCESS: Found pending request {pending[0].id}")
            print(f"   Reason: {pending[0].reason}")
        else:
            print("   FAILURE: Request not found in queue.")
            
        # 5. Claim
        print("[4/4] Claiming Request...")
        claimed = await queue.claim_request(req.id, "visual_agent")
        if claimed and claimed.state == HitlState.CLAIMED:
             print(f"   SUCCESS: Request claimed by {claimed.claimed_by_agent_id}")
        else:
             print("   FAILURE: Claim failed.")

    await engine.dispose()
    print("=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(verify_hitl_queue())
