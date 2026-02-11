
import pytest
from unittest.mock import MagicMock, Mock
from spine.chapters.action.composer import Composer

@pytest.fixture
def mock_service_builder():
    service = MagicMock()
    drafts = MagicMock()
    drafts.create.return_value.execute.return_value = {"id": "draft_123", "message": {"id": "msg_123"}}
    service.users.return_value.drafts.return_value = drafts
    
    builder = MagicMock(return_value=service)
    return builder

@pytest.fixture
def composer(mock_service_builder):
    return Composer(mock_service_builder)

@pytest.mark.asyncio
async def test_create_draft_success(composer, mock_service_builder):
    """Test successful draft creation."""
    result = await composer.create_draft(
        user_id="user1",
        creds="mock_creds",
        to_email="test@example.com",
        subject="Hello",
        body_text="Hi there"
    )
    
    assert result["id"] == "draft_123"
    
    # Verify API call structure
    service = mock_service_builder.return_value
    service.users.return_value.drafts.return_value.create.assert_called_once()
    
    call_args = service.users.return_value.drafts.return_value.create.call_args
    assert call_args.kwargs["userId"] == "me"
    assert "raw" in call_args.kwargs["body"]["message"]

@pytest.mark.asyncio
async def test_create_draft_html(composer, mock_service_builder):
    """Test draft with HTML content."""
    await composer.create_draft(
        user_id="user1",
        creds="mock_creds",
        to_email="test@example.com",
        subject="HTML Test",
        body_text="Plain",
        body_html="<b>Bold</b>"
    )
    # Just verifying no error and proper call
    service = mock_service_builder.return_value
    service.users.return_value.drafts.return_value.create.assert_called_once()

@pytest.mark.asyncio
async def test_create_draft_failure(composer, mock_service_builder):
    """Test error handling."""
    service = mock_service_builder.return_value
    service.users.return_value.drafts.return_value.create.side_effect = Exception("API Error")
    
    with pytest.raises(RuntimeError) as exc:
        await composer.create_draft(
            user_id="user1",
            creds="mock_creds",
            to_email="test@example.com",
            subject="Fail",
            body_text="Fail"
        )
    assert "Draft creation failed" in str(exc.value)
