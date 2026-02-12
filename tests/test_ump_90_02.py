import pytest
import pytest_asyncio
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.base import Base
from spine.chapters.hitl.resolver import HitlResolver
from spine.chapters.hitl.models import HitlRequest, HitlDecision, HitlState
from spine.chapters.hitl.api import resolve_request, HitlDecisionCreate
from spine.db.models import WorkItem, WorkItemState, Tenant, User, Email, EmailProvider, Direction, ConfidenceBand, TenantPlan

# Reuse setup
@pytest_asyncio.fixture(scope="function")
async def hitl_test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest_asyncio.fixture
async def setup_data(hitl_test_db):
    tenant = Tenant(id="t1", name="Test Tenant", plan=TenantPlan.FREE)
    user = User(id="u1", email="test@test.com")
    email = Email(id="e1", provider_message_id="m1", thread_id="th1", from_email="x@y.com", direction=Direction.INBOUND, received_at=datetime.utcnow(), gmail_id="g1", body_text="body")
    hitl_test_db.add(tenant)
    hitl_test_db.add(user)
    hitl_test_db.add(email)
    
    wi = WorkItem(id="wi1", tenant_id="t1", email_id="e1", state=WorkItemState.NEEDS_REVIEW, owner_type="USER", owner_id="u1", confidence_band=ConfidenceBand.LOW)
    hitl_test_db.add(wi)
    
    req = HitlRequest(id="req1", tenant_id="t1", work_item_id="wi1", reason="Ambiguity", context_json="{}", state=HitlState.CLAIMED, claimed_by_agent_id="agent1")
    hitl_test_db.add(req)
    
    await hitl_test_db.commit()
    return wi, req

@pytest.mark.asyncio
async def test_01_resolve_approved(hitl_test_db, setup_data):
    """Test resolving as RESOLVED (Approved) moves WorkItem to NEEDS_REPLY."""
    wi, req = setup_data
    resolver = HitlResolver(hitl_test_db)
    
    dec = HitlDecision(id="d1", request_id=req.id, agent_id="agent1", outcome=HitlState.RESOLVED)
    hitl_test_db.add(dec)
    
    updated_wi = await resolver.apply_decision(dec)
    await hitl_test_db.commit()
    
    assert updated_wi.state == WorkItemState.NEEDS_REPLY
    assert updated_wi.confidence_band == ConfidenceBand.HIGH
    assert updated_wi.resolution_lock is True

@pytest.mark.asyncio
async def test_02_resolve_rejected(hitl_test_db, setup_data):
    """Test resolving as REJECTED moves WorkItem to DONE."""
    wi, req = setup_data
    resolver = HitlResolver(hitl_test_db)
    
    dec = HitlDecision(id="d2", request_id=req.id, agent_id="agent1", outcome=HitlState.REJECTED)
    hitl_test_db.add(dec)
    
    updated_wi = await resolver.apply_decision(dec)
    await hitl_test_db.commit()
    
    assert updated_wi.state == WorkItemState.DONE
    assert updated_wi.closed_at is not None

@pytest.mark.asyncio
async def test_03_api_resolve_flow(hitl_test_db, setup_data):
    """Test the full API flow for resolution."""
    wi, req = setup_data
    
    payload = HitlDecisionCreate(
        request_id=req.id,
        agent_id="agent1",
        outcome=HitlState.RESOLVED,
        modified_draft="New Body",
        feedback_notes="Looks good"
    )
    
    # Call API function directly (mocking dependency injection)
    await resolve_request(payload, db=hitl_test_db)
    
    # Reload WI
    await hitl_test_db.refresh(wi)
    assert wi.state == WorkItemState.NEEDS_REPLY
    
    # Check Request updated
    await hitl_test_db.refresh(req)
    assert req.state == HitlState.RESOLVED
    assert req.resolved_at is not None

@pytest.mark.asyncio
async def test_04_resolver_invalid_request(hitl_test_db):
    """Resolver raises error if request not found."""
    resolver = HitlResolver(hitl_test_db)
    dec = HitlDecision(id="d3", request_id="bad_id", agent_id="a1", outcome=HitlState.RESOLVED)
    
    with pytest.raises(ValueError, match="not found"):
        await resolver.apply_decision(dec)

@pytest.mark.asyncio
async def test_05_api_must_be_claimed(hitl_test_db, setup_data):
    """API raises 409 if request is PENDING (not CLAIMED)."""
    wi, req = setup_data
    req.state = HitlState.PENDING
    await hitl_test_db.commit()
    
    payload = HitlDecisionCreate(request_id=req.id, agent_id="a1", outcome=HitlState.RESOLVED)
    
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as e:
        await resolve_request(payload, db=hitl_test_db)
    assert e.value.status_code == 409

@pytest.mark.asyncio
async def test_06_resolver_missing_workitem(hitl_test_db):
    """Resolver raises error if WorkItem missing."""
    # Orphaned request
    req = HitlRequest(id="orph", tenant_id="t1", work_item_id="missing_wi", state=HitlState.CLAIMED, reason="r", context_json="{}")
    hitl_test_db.add(req)
    await hitl_test_db.commit()
    
    dec = HitlDecision(id="d4", request_id="orph", agent_id="a1", outcome=HitlState.RESOLVED)
    
    resolver = HitlResolver(hitl_test_db)
    with pytest.raises(ValueError, match="WorkItem .* not found"):
        await resolver.apply_decision(dec)

@pytest.mark.asyncio
async def test_07_api_update_request_state(hitl_test_db, setup_data):
    """API ensures Request state matches Decision outcome."""
    wi, req = setup_data
    payload = HitlDecisionCreate(request_id=req.id, agent_id="a1", outcome=HitlState.REJECTED)
    
    await resolve_request(payload, db=hitl_test_db)
    await hitl_test_db.refresh(req)
    assert req.state == HitlState.REJECTED

@pytest.mark.asyncio
async def test_08_resolver_locking(hitl_test_db, setup_data):
    """Ensure resolution lock is applied to WorkItem."""
    wi, req = setup_data
    resolver = HitlResolver(hitl_test_db)
    dec = HitlDecision(id="d5", request_id=req.id, agent_id="a1", outcome=HitlState.RESOLVED)
    
    await resolver.apply_decision(dec)
    await hitl_test_db.refresh(wi)
    assert wi.resolution_lock is True

@pytest.mark.asyncio
async def test_09_api_persistence(hitl_test_db, setup_data):
    """API checks that Decision runs are persisted."""
    wi, req = setup_data
    payload = HitlDecisionCreate(request_id=req.id, agent_id="a1", outcome=HitlState.RESOLVED)
    await resolve_request(payload, db=hitl_test_db)
    
    # Check decision count
    from sqlalchemy import func, select
    res = await hitl_test_db.execute(select(func.count(HitlDecision.id)))
    assert res.scalar() == 1

@pytest.mark.asyncio
async def test_10_invalid_decision_outcome(hitl_test_db, setup_data):
    """Technically handled by Pydantic validation, but let's check logic doesn't break on unexpected enum."""
    # If we manually pass an enum that logic doesn't cover (e.g. CLAIMED as outcome), it should prob do nothing or raise?
    # Resolver checks if RESOLVED or REJECTED.
    wi, req = setup_data
    resolver = HitlResolver(hitl_test_db)
    dec = HitlDecision(id="d6", request_id=req.id, agent_id="a1", outcome=HitlState.PENDING) # Invalid outcome conceptually
    
    # Current implementation does nothing if not RESOLVED/REJECTED
    await resolver.apply_decision(dec)
    await hitl_test_db.refresh(wi)
    assert wi.state == WorkItemState.NEEDS_REVIEW # Unchanged
