import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.orm import Session
from datetime import datetime

from spine.chapters.intelligence.processor import IntelligenceProcessor
from spine.chapters.intelligence.triage import TriageResult, ConfidenceBand, WorkItemState
from spine.db.models import Email, WorkItem, EmailAccount

# Mock data
MOCK_USER_ID = "user_123"
MOCK_TENANT_ID = "tenant_456"

@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)

@pytest.fixture
def processor(mock_db):
    # Patch the repo/streamer inside the init
    with patch("spine.chapters.intelligence.processor.EmailRepository") as MockRepo, \
         patch("spine.chapters.intelligence.processor.GmailStreamer") as MockStreamer:
        
        p = IntelligenceProcessor(mock_db)
        # Setup Repo Mock
        p.email_repo.get_account_by_user = AsyncMock()
        p.email_repo.get_account_by_user.return_value = EmailAccount(
            tenant_id=MOCK_TENANT_ID, user_id=MOCK_USER_ID
        )
        # Setup Streamer Mock
        p.streamer.stream_recent_threads = MagicMock()
        
        return p

@pytest.mark.asyncio
async def test_processor_run_success(processor, mock_db):
    # 1. Mock Stream Yield
    async def mock_stream(*args, **kwargs):
        yield {"id": "thread_1", "messages": [{"id": "msg_1", "snippet": "test"}]}
        yield {"id": "thread_2", "messages": [{"id": "msg_2", "snippet": "test2"}]}

    processor.streamer.stream_recent_threads.side_effect = mock_stream

    # 2. Mock Triage (so we don't rely on real logic/parsing)
    with patch("spine.chapters.intelligence.processor.triage_thread") as mock_triage:
        mock_triage.return_value = TriageResult(
            thread_id="t1",
            message_id="m1", # Will change for each call if needed, but let's assume same structure
            subject="Test Subject",
            sender="me@test.com",
            received_at=datetime.utcnow(),
            confidence=ConfidenceBand.MEDIUM,
            suggested_state=WorkItemState.NEEDS_REPLY,
            snippet="snippet"
        )
        
        # 3. Mock DB Query (No existing email)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Run
        metrics = await processor.process_user_stream(MOCK_USER_ID, limit=2)

        # Assertions
        assert metrics["scanned"] == 2
        assert metrics["processed"] == 2
        assert metrics["errors"] == 0
        
        # Check DB Adds
        assert mock_db.add.call_count == 4 # 2 Emails + 2 WorkItems
        assert mock_db.commit.call_count == 2

@pytest.mark.asyncio
async def test_processor_deduplication(processor, mock_db):
    # 1. Mock Stream Yield (1 item)
    async def mock_stream(*args, **kwargs):
        yield {"id": "thread_1"}

    processor.streamer.stream_recent_threads.side_effect = mock_stream

    # 2. Mock DB Query (Email EXISTS)
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock(spec=Email)

    with patch("spine.chapters.intelligence.processor.triage_thread"):
        metrics = await processor.process_user_stream(MOCK_USER_ID, limit=1)

        assert metrics["scanned"] == 1
        assert metrics["processed"] == 0
        assert metrics["skipped_existing"] == 1
        assert mock_db.add.call_count == 0

@pytest.mark.asyncio
async def test_processor_no_account(processor):
    # Simulate missing account
    processor.email_repo.get_account_by_user.return_value = None
    
    metrics = await processor.process_user_stream(MOCK_USER_ID)
    
    assert metrics["scanned"] == 0
    assert metrics["processed"] == 0

@pytest.mark.asyncio
async def test_processor_db_error_handling(processor, mock_db):
    # 1. Mock Stream
    async def mock_stream(*args, **kwargs):
        yield {"id": "thread_1"}

    processor.streamer.stream_recent_threads.side_effect = mock_stream

    # 2. Mock DB Query (None)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # 3. Raise Error on Commit
    mock_db.commit.side_effect = Exception("DB Boom")

    with patch("spine.chapters.intelligence.processor.triage_thread"):
        metrics = await processor.process_user_stream(MOCK_USER_ID)

        assert metrics["scanned"] == 1
        assert metrics["processed"] == 0
        assert metrics["errors"] == 1 # Caught and counted
        mock_db.rollback.assert_called()
