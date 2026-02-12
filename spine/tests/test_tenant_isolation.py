
import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlmodel import select
from spine.db.models import User, Tenant, Email, WorkItem, Direction
from spine.chapters.intelligence.processor import IntelligenceProcessor
from spine.chapters.intelligence.triage import TriageResult, ConfidenceBand, WorkItemState
from datetime import datetime
import uuid

# Mock the Streamer and Triage since we are testing the Processor logic
@pytest.fixture
def mock_streamer():
    streamer = MagicMock()
    streamer.stream_recent_threads = MagicMock()
    return streamer


@pytest.mark.asyncio
async def test_tenant_isolation_starvation(mock_db_session):
    """
    CRITICAL SECURITY TEST: Tenant Isolation Starvation.
    Uses generic Mock session to prove logic flaw.
    """
    processor = IntelligenceProcessor(mock_db_session)
    processor.email_repo.get_account_by_user = AsyncMock()
    
    # 1. Setup Mock Accounts
    account_a = MagicMock()
    account_a.tenant_id = "tenant_a"
    account_b = MagicMock()
    account_b.tenant_id = "tenant_b"
    processor.email_repo.get_account_by_user.side_effect = lambda uid: account_a if uid == "user_a" else account_b

    # 2. Setup Triage result (Shared Message ID)
    shared_message_id = "msg_123_shared"
    triage_result = TriageResult(
        message_id=shared_message_id,
        thread_id="thread_123",
        sender="sender@external.com",
        subject="Shared Email",
        snippet="Hello",
        received_at=datetime.utcnow(),
        suggested_state=WorkItemState.NEEDS_REPLY,
        confidence=ConfidenceBand.HIGH,
        tags=["urgent"]
    )

    # 3. Execution - Tenant A (First Run)
    # Mock: Email NOT found
    mock_result_empty = MagicMock()
    mock_result_empty.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result_empty
    
    # Run Processor logic for Tenant A (simulated via _save_work_item check? Or full stream)
    # Let's verify the QUERY being made.
    
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("spine.chapters.intelligence.processor.triage_thread", lambda x: triage_result)
        
        # ACT 1: Tenant A
        # Simulating streamer
        async def mock_stream_gen(uid, limit):
             yield {"id": "thread_123"}
        processor.streamer.stream_recent_threads = mock_stream_gen
        
        await processor.process_user_stream("user_a")
        
        # Verify Session.add was called (Email + WorkItem created)
        assert mock_db_session.add.call_count == 2, "Tenant A should create Email + WorkItem"
        # Reset Mock
        mock_db_session.add.reset_mock()
        
        # 4. Execution - Tenant B (Second Run)
        # BUG SIMULATION: Processor queries by Provider Message ID. 
        # Since Tenant A inserted it, the DB would return it.
        # We Mock the DB returning Tenant A's Email.
        
        existing_email_from_a = Email(
            id="email_id_from_a",
            provider_message_id=shared_message_id,
            tenant_id="tenant_a"  
        )
        
        # FIX VERIFICATION:
        # The PROPER behavior is that the query includes `tenant_id == 'tenant_b'`.
        # Therefore, the DB should return None (because email_from_a has tenant_id='tenant_a').
        
        # We assume the code is fixed, so we Mock "None" (Not Found) for Tenant B's query.
        mock_db_session.execute.return_value = mock_result_empty
        
        # ACT 2: Tenant B
        await processor.process_user_stream("user_b")
        
        # 5. Assetions
        
        # A. Verify Result
        assert mock_db_session.add.call_count == 2, "Tenant B should create a WorkItem (Isolation Success)"
        
        # B. Verify Query Logic (The Core Fix)
        # We inspect the calls to execute to ensure tenant_id was in the WHERE clause.
        # This is tricky with SQLAlchemy statement objects, but we can check the string compilation or params.
        # To be strict: We can inspect the last `execute` call.
        call_args = mock_db_session.execute.call_args
        stmt = call_args[0][0]
        compiled = str(stmt.compile(compile_kwargs={"literal_binds": True}))
        
        assert "emails.tenant_id = 'tenant_b'" in compiled, "Security Violation: Query did not restrict by tenant_id!"

@pytest.mark.asyncio
async def test_tenant_constraint_integrity(db_session):
    """
    Verify Database Constraints:
    1. tenant_id cannot be NULL.
    2. (tenant_id, provider_message_id) must be UNIQUE.
    """
    from sqlalchemy.exc import IntegrityError
    
    # 1. NOT NULL Check
    try:
        async with db_session.begin_nested():
            email_null = Email(
                id="null_tenant",
                provider_message_id="msg_null",
                tenant_id=None 
            )
            db_session.add(email_null)
            await db_session.commit() # Trigger constraint check
        pytest.fail("Should have raised IntegrityError for NULL tenant_id")
    except IntegrityError:
        # Constraint caught, transaction rolled back to savepoint
        pass 
    
    # 2. UNIQUE Constraint Check
    tenant_id = "t_constraint"
    msg_id = "msg_unique"
    
    # First Insert (Commited to outer transaction)
    # We use a nested block to ensure it's safe, or just add it to session
    e1 = Email(id="e1", tenant_id=tenant_id, provider_message_id=msg_id, thread_id="th1", from_email="a", received_at=datetime.utcnow(), direction=Direction.INBOUND)
    db_session.add(e1)
    await db_session.flush() # Flush to DB
    
    # Duplicate Insert (Should fail)
    try:
        async with db_session.begin_nested():
            e2 = Email(id="e2", tenant_id=tenant_id, provider_message_id=msg_id, thread_id="th1", from_email="b", received_at=datetime.utcnow(), direction=Direction.INBOUND)
            db_session.add(e2)
            await db_session.commit() # Trigger check
        pytest.fail("Should have raised IntegrityError for Duplicate (tenant_id, provider_message_id)")
    except IntegrityError:
        pass # Success
        
    # Same Message ID, Different Tenant -> SUCCESS
    # We can just add it, no need for nested if we expect success
    e3 = Email(id="e3", tenant_id="t_other", provider_message_id=msg_id, thread_id="th1", from_email="c", received_at=datetime.utcnow(), direction=Direction.INBOUND)
    db_session.add(e3)
    await db_session.flush() # Should succeed

