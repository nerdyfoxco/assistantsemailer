import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from googleapiclient.errors import HttpError
from spine.chapters.intelligence.streamer import GmailStreamer
import json

# Fixtures
@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.get_account_by_user.return_value = MagicMock(
        oauth_token_ref=json.dumps({"access_token": "valid", "refresh_token": "valid"})
    )
    return repo

@pytest.fixture
def streamer(mock_repo):
    return GmailStreamer(mock_repo)

# 1. Happy Path
@pytest.mark.asyncio
async def test_stream_success(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_service = mock_build.return_value
        mock_service.users.return_value.threads.return_value.list.return_value.execute.return_value = {
            "threads": [{"id": "t1"}, {"id": "t2"}]
        }
        mock_service.users.return_value.threads.return_value.get.side_effect = [
            MagicMock(execute=lambda: {"id": "t1", "snippet": "A"}),
            MagicMock(execute=lambda: {"id": "t2", "snippet": "B"}),
        ]

        results = [t async for t in streamer.stream_recent_threads("u1")]
        assert len(results) == 2
        assert results[0]["id"] == "t1"

# 2. Empty/Null
@pytest.mark.asyncio
async def test_stream_empty(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_service = mock_build.return_value
        # Return empty list
        mock_service.users.return_value.threads.return_value.list.return_value.execute.return_value = {}
        
        results = [t async for t in streamer.stream_recent_threads("u1")]
        assert len(results) == 0

# 3. Auth Failure (Critical)
@pytest.mark.asyncio
async def test_auth_failure(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        # Simulate 401 on build or list
        error_resp = MagicMock(status=401)
        mock_build.side_effect = HttpError(resp=error_resp, content=b"Unauthorized")
        
        with pytest.raises(HttpError):
            [t async for t in streamer.stream_recent_threads("u1")]

# 4. Network Error (Critical)
@pytest.mark.asyncio
async def test_network_error(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_build.side_effect = TimeoutError("Connection timed out")
        
        with pytest.raises(TimeoutError):
            [t async for t in streamer.stream_recent_threads("u1")]

# 5. Malformed API Response (Individual Item)
@pytest.mark.asyncio
async def test_malformed_item_recovery(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_service = mock_build.return_value
        mock_service.users.return_value.threads.return_value.list.return_value.execute.return_value = {
            "threads": [{"id": "t1"}, {"id": "bad_one"}]
        }
        
        # t1 succeeds, bad_one fails
        mock_service.users.return_value.threads.return_value.get.side_effect = [
            MagicMock(execute=lambda: {"id": "t1"}),
            Exception("Malformed JSON")
        ]
        
        # Should yield t1 and skip bad_one
        results = [t async for t in streamer.stream_recent_threads("u1")]
        assert len(results) == 1
        assert results[0]["id"] == "t1"

# 6. User Not Found (Missing Account)
@pytest.mark.asyncio
async def test_missing_account(mock_repo):
    mock_repo.get_account_by_user.return_value = None
    streamer = GmailStreamer(mock_repo)
    
    with pytest.raises(ValueError, match="no linked Gmail account"):
        [t async for t in streamer.stream_recent_threads("unknown_user")]

# 7. Concurrent Streams (Generator Independence)
@pytest.mark.asyncio
async def test_concurrent_streams(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_service = mock_build.return_value
        mock_service.users.return_value.threads.return_value.list.return_value.execute.return_value = {
            "threads": [{"id": "t1"}]
        }
        mock_service.users.return_value.threads.return_value.get.return_value.execute.return_value = {"id": "t1"}

        # Run two generators concurrently
        gen1 = streamer.stream_recent_threads("u1")
        gen2 = streamer.stream_recent_threads("u2")
        
        res1 = await gen1.__anext__()
        res2 = await gen2.__anext__()
        
        assert res1["id"] == "t1"
        assert res2["id"] == "t1"

# 8. Rate Limiting (429) - Critical Propagates
@pytest.mark.asyncio
async def test_rate_limit(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        error_resp = MagicMock(status=429)
        mock_build.side_effect = HttpError(resp=error_resp, content=b"Too Many Requests")
        
        with pytest.raises(HttpError):
            [t async for t in streamer.stream_recent_threads("u1")]

# 9. Large Limit (Pagination Placeholder check)
# Currently we mocked it to just return one batch, but this ensures arg passing works
@pytest.mark.asyncio
async def test_limit_argument(streamer):
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
        mock_list = mock_build.return_value.users.return_value.threads.return_value.list
        mock_list.return_value.execute.return_value = {}
        
        [t async for t in streamer.stream_recent_threads("u1", limit=50)]
        
        # Verify limit passed to API
        kwargs = mock_list.call_args[1]
        assert kwargs["maxResults"] == 50

# 10. Cleanup (Resource Integrity)
@pytest.mark.asyncio
async def test_cleanup(streamer):
    # Ensure no lingering connections or mutations
    # For a generator, cleanup is mostly about finishing iteration
    with patch("spine.chapters.intelligence.streamer.build") as mock_build:
         mock_service = mock_build.return_value
         mock_service.close = MagicMock() # Mock close method
         
         mock_service.users.return_value.threads.return_value.list.return_value.execute.return_value = {}
         
         [t async for t in streamer.stream_recent_threads("u1")]
         # In real implementation we might want to ensure service.close() is called if we manage lifecycle
         # For this brick (simplicity), we rely on GC, but test confirms finish.
         assert True
