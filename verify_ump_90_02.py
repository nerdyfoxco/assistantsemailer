import asyncio
import uuid
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.base import Base
from spine.chapters.hitl.models import HitlRequest, HitlDecision, HitlState
from spine.db.models import WorkItem, WorkItemState, Tenant, User, Email, EmailProvider, Direction, ConfidenceBand, TenantPlan
from spine.chapters.hitl.resolver import HitlResolver

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verifier")

async def verify_ump_90_02():
    logger.info("=== Verifying UMP-90-02: Decision Pipe ===")
    
    # 1. Setup DB
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # 2. Seed Data
        tenant = Tenant(id="t1", name="Test Tenant", plan=TenantPlan.FREE)
        user = User(id="u1", email="test@test.com")
        email = Email(id="e1", provider_message_id="m1", thread_id="th1", from_email="x@y.com", direction=Direction.INBOUND, received_at=datetime.utcnow(), gmail_id="g1", body_text="body")
        
        wi = WorkItem(id="wi1", tenant_id="t1", email_id="e1", state=WorkItemState.NEEDS_REVIEW, owner_type="USER", owner_id="u1", confidence_band=ConfidenceBand.LOW)
        
        req = HitlRequest(id="req1", tenant_id="t1", work_item_id="wi1", reason="Ambiguity", context_json="{}", state=HitlState.CLAIMED, claimed_by_agent_id="agent1")
        
        db.add_all([tenant, user, email, wi, req])
        await db.commit()
        logger.info("[OK] Seeded Initial State: WorkItem=NEEDS_REVIEW, Request=CLAIMED")
        
        # 3. Simulate Agent Decision (RESOLVED)
        logger.info("--- Step 1: Agent Resolves Request ---")
        dec = HitlDecision(id="d1", request_id=req.id, agent_id="agent1", outcome=HitlState.RESOLVED, feedback_notes="Proceed")
        db.add(dec)
        await db.commit() # Save decision
        logger.info("[OK] Decision Saved")
        
        # 4. Run Resolver
        logger.info("--- Step 2: Resolver Applies Decision ---")
        resolver = HitlResolver(db)
        updated_wi = await resolver.apply_decision(dec)
        
        # 5. Verify Results
        logger.info("--- Step 3: Verification ---")
        if updated_wi.state == WorkItemState.NEEDS_REPLY:
            logger.info(f"[PASS] WorkItem State: {updated_wi.state}")
        else:
            logger.error(f"[FAIL] WorkItem State: {updated_wi.state}")
            
        if updated_wi.resolution_lock:
             logger.info("[PASS] Resolution Lock: Active")
        else:
             logger.error("[FAIL] Resolution Lock: Inactive")

        if updated_wi.confidence_band == ConfidenceBand.HIGH:
            logger.info("[PASS] Confidence Band: HIGH")
        else:
            logger.error(f"[FAIL] Confidence Band: {updated_wi.confidence_band}")

    await engine.dispose()
    logger.info("=== Verification Complete ===")

if __name__ == "__main__":
    asyncio.run(verify_ump_90_02())
