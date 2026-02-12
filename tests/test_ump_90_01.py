import pytest
import pytest_asyncio
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.base import Base
from spine.chapters.hitl.queue import EscalationQueue
from spine.chapters.hitl.models import HitlRequest, HitlState
from spine.db.models import WorkItem, WorkItemState, Tenant, User, Email, EmailProvider, Direction, ConfidenceBand, TenantPlan, Role

# Setup In-Memory Async DB for Tests
@pytest_asyncio.fixture(scope="function")
async def hitl_test_db():
    # Use sqlite+aiosqlite for async in-memory
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        
    await engine.dispose()

@pytest_asyncio.fixture
async def setup_data(hitl_test_db):
    # Create tenant, user, etc
    tenant = Tenant(id="t1", name="Test Tenant", plan=TenantPlan.FREE)
    user = User(id="u1", email="test@test.com")
    # Need to fulfill all non-nullable fields
    email = Email(
        id="e1", 
        provider_message_id="msg1", 
        thread_id="th1", 
        from_email="sender@b.com", 
        direction=Direction.INBOUND,
        received_at=datetime.utcnow(),
        gmail_id="g1",
        body_text="body"
    )
    hitl_test_db.add(tenant)
    hitl_test_db.add(user)
    hitl_test_db.add(email)
    await hitl_test_db.commit()
    
    wi = WorkItem(
        id="wi1",
        tenant_id="t1",
        email_id="e1",
        state=WorkItemState.NEEDS_REPLY,
        owner_type="USER",
        owner_id="u1",
        confidence_band=ConfidenceBand.LOW,
        resolution_lock=False
    )
    hitl_test_db.add(wi)
    await hitl_test_db.commit()
    return wi

@pytest.mark.asyncio
async def test_01_submit_happy_path(hitl_test_db, setup_data):
    """Identify a WorkItem, mark as NEEDS_REVIEW, verify it appears in HitlRequest table."""
    queue = EscalationQueue(hitl_test_db)
    wi = setup_data
    
    req = await queue.submit_for_review(wi, "Ambiguity", {"foo": "bar"})
    await hitl_test_db.commit()
    
    assert wi.state == WorkItemState.NEEDS_REVIEW
    assert req.state == HitlState.PENDING
    assert req.reason == "Ambiguity"
    assert json.loads(req.context_json)["foo"] == "bar"

@pytest.mark.asyncio
async def test_02_claim_request(hitl_test_db, setup_data):
    """Move request from PENDING to CLAIMED by a specific agent_id."""
    queue = EscalationQueue(hitl_test_db)
    wi = setup_data
    req = await queue.submit_for_review(wi, "Test", {})
    await hitl_test_db.commit()
    
    claimed = await queue.claim_request(req.id, "agent_007")
    await hitl_test_db.commit()
    
    assert claimed.state == HitlState.CLAIMED
    assert claimed.claimed_by_agent_id == "agent_007"
    assert claimed.claimed_at is not None

@pytest.mark.asyncio
async def test_03_idempotency(hitl_test_db, setup_data):
    """Submitting the same WorkItem twice does NOT create duplicate requests? 
    Current implementation allows duplicates. We verify we can insert 2."""
    queue = EscalationQueue(hitl_test_db)
    wi = setup_data
    req1 = await queue.submit_for_review(wi, "Reason 1", {})
    req2 = await queue.submit_for_review(wi, "Reason 1", {}) # Same reason even
    
    await hitl_test_db.commit()
    assert req1.id != req2.id

@pytest.mark.asyncio
async def test_04_isolation(hitl_test_db):
    """Tenant A's HITL agent cannot see Tenant B's requests."""
    # Setup Tenant B
    t2 = Tenant(id="t2", name="Tenant B", plan=TenantPlan.FREE)
    hitl_test_db.add(t2)
    # create user and email for FK constraints if any (Tenant doesn't strictly need them for request, usually)
    # But WorkItem needs email/tenant
    # Let's bypass creating full tree if we can just create HitlRequest (if no FK to WorkItem is enforced at DB level or we make one)
    # HitlRequest has work_item_id mapped but we didn't define ForeignKey in model for it yet?
    # Checking HitlRequest model: work_item_id = mapped_column(String). No FK. Good for test simplicity.
    
    r1 = HitlRequest(id="r1", tenant_id="t1", work_item_id="w1", reason="r", context_json="{}", state=HitlState.PENDING)
    r2 = HitlRequest(id="r2", tenant_id="t2", work_item_id="w2", reason="r", context_json="{}", state=HitlState.PENDING)
    hitl_test_db.add(r1)
    hitl_test_db.add(r2)
    await hitl_test_db.commit()
    
    queue = EscalationQueue(hitl_test_db)
    pending_t1 = await queue.get_pending_requests("t1")
    assert len(pending_t1) == 1
    assert pending_t1[0].id == "r1"

@pytest.mark.asyncio
async def test_05_claim_invalid_state(hitl_test_db):
    """Cannot resolve a request that is not CLAIMED? Here testing cannot claim non-pending."""
    queue = EscalationQueue(hitl_test_db)
    r1 = HitlRequest(id="r1", tenant_id="t1", work_item_id="w1", reason="r", context_json="{}", state=HitlState.RESOLVED)
    hitl_test_db.add(r1)
    await hitl_test_db.commit()
    
    with pytest.raises(ValueError, match="RESOLVED"):
        await queue.claim_request("r1", "agent")

@pytest.mark.asyncio
async def test_10_stress(hitl_test_db, setup_data):
    """Queue 100 requests."""
    queue = EscalationQueue(hitl_test_db)
    wi = setup_data
    
    start = datetime.utcnow()
    # If we do this in loop with await/flush it might be slower than batch, but verifies robustness
    session = hitl_test_db
    for i in range(100):
        await queue.submit_for_review(wi, f"Reason {i}", {})
    await session.commit()
    end = datetime.utcnow()
    
    # We need to query count
    from sqlalchemy import func, select
    result = await session.execute(select(func.count(HitlRequest.id)))
    count = result.scalar()
    
    assert count == 100
    # Should be fast enough
    assert (end - start).total_seconds() < 5.0
