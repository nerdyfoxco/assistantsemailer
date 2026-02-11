
import pytest
from unittest.mock import MagicMock
from spine.chapters.action.valve import Valve

@pytest.fixture
def mock_service_builder():
    service = MagicMock()
    messages = MagicMock()
    messages.send.return_value.execute.return_value = {"id": "sent_123"}
    service.users.return_value.messages.return_value = messages
    
    builder = MagicMock(return_value=service)
    return builder

@pytest.mark.asyncio
async def test_valve_send_success(mock_service_builder):
    """Test successful send."""
    valve = Valve(mock_service_builder)
    result = await valve.send_email("user1", "creds", "base64_raw", "test@example.com")
    
    assert result is True
    mock_service_builder.return_value.users.return_value.messages.return_value.send.assert_called_once()

@pytest.mark.asyncio
async def test_valve_whitelist_block(mock_service_builder):
    """Test whitelist blocking."""
    valve = Valve(mock_service_builder, dev_mode_whitelist=["allowed.com"])
    
    # Blocked
    result = await valve.send_email("user1", "creds", "raw", "bad@blocked.com")
    assert result is False
    mock_service_builder.return_value.users.return_value.messages.return_value.send.assert_not_called()
    
    # Allowed
    result_allowed = await valve.send_email("user1", "creds", "raw", "friend@allowed.com")
    assert result_allowed is True
