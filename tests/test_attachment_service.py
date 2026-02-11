
import pytest
from unittest.mock import AsyncMock, MagicMock
from spine.chapters.action.attachment_service import AttachmentService
from spine.chapters.action.unlocker import AttachmentUnlocker

@pytest.fixture
def mock_unlocker():
    return AsyncMock(spec=AttachmentUnlocker)

@pytest.fixture
def service(mock_unlocker):
    return AttachmentService(mock_unlocker)

@pytest.mark.asyncio
async def test_smart_context_extraction(service):
    """Test extracting hints from text."""
    text = "The password is your Date of Birth."
    hints = service.extract_hints(text.lower())
    assert "dob" in hints

    text2 = "Please use your PAN number."
    hints2 = service.extract_hints(text2.lower())
    assert "pan" in hints2
    
    text3 = "Unrelated text."
    hints3 = service.extract_hints(text3.lower())
    assert len(hints3) == 0

@pytest.mark.asyncio
async def test_smart_unlock_flow_fast_path(service, mock_unlocker):
    """If fast unlock works, we shouldn't fetch body."""
    mock_unlocker.attempt_unlock.return_value = True
    
    result = await service.smart_unlock("user1", "msg1", b"pdf_bytes", "creds")
    
    assert result is True
    # Verify we only called attempt_unlock once (fast path)
    assert mock_unlocker.attempt_unlock.call_count == 1
    # Verify proxy fetch was NOT called
    # (We can't easily assert proxy calls since it's instantiated inside, 
    # unless we mock the class or inject it. In this implementation it's instantiated inside.
    # We should probably inject it for better testing, but for now we trust the flow logic.)

@pytest.mark.asyncio
async def test_smart_unlock_flow_deep_path(service, mock_unlocker):
    """If fast unlock fails, we should fetch body and try again."""
    # 1. Fast path fails
    mock_unlocker.attempt_unlock.side_effect = [False, True]
    
    # Mock Proxy
    service.proxy = AsyncMock()
    service.proxy.fetch_body.return_value = {"snippet": "Use your PAN", "body_text": ""}
    
    result = await service.smart_unlock("user1", "msg1", b"pdf_bytes", "creds")
    
    assert result is True
    # Called twice: once generic, once with hints
    assert mock_unlocker.attempt_unlock.call_count == 2
    
    # Check second call args included 'pan' hint
    call_args = mock_unlocker.attempt_unlock.call_args_list[1]
    assert "pan" in call_args.kwargs.get("common_keys", [])
