
import pytest
from unittest.mock import AsyncMock, MagicMock
from spine.chapters.mind.context import ContextBuilder, PromptContext
from spine.db.models import Email

@pytest.mark.asyncio
async def test_context_build_success():
    """Test building context from a mock email + proxy."""
    # Setup
    mock_proxy = AsyncMock()
    mock_proxy.fetch_body.return_value = {
        "id": "msg_123",
        "snippet": "Hello world snippet",
        "html": "<p>Hello world</p>",
        "attachments": [{"filename": "invoice.pdf", "size": 1024}]
    }
    
    builder = ContextBuilder(proxy=mock_proxy)
    
    mock_email = Email(
        provider_message_id="msg_123",
        from_email="boss@company.com",
        subject="Urgent Invoice",
        snippet="Hello...",
        received_at="2026-01-01"
    )
    
    # Execute
    context = await builder.build(user_id="me", email=mock_email, creds="fake_creds")
    
    # Verify
    assert isinstance(context, PromptContext)
    assert context.sender == "boss@company.com"
    assert "invoice.pdf" in context.attachments_summary
    # Since snippet is short (<50 chars), logic falls back to HTML
    assert "<p>Hello world</p>" in context.body_text
    
    # Context Formatting
    prompt_str = context.to_system_prompt_addition()
    assert "--- EMAIL CONTEXT ---" in prompt_str
    assert "From: boss@company.com" in prompt_str

@pytest.mark.asyncio
async def test_context_fallback_on_error():
    """Test that builder doesn't crash if Proxy fails."""
    mock_proxy = AsyncMock()
    mock_proxy.fetch_body.side_effect = RuntimeError("Gmail Down")
    
    builder = ContextBuilder(proxy=mock_proxy)
    mock_email = Email(
        provider_message_id="msg_fail",
        from_email="unknown@void.com",
        subject="Doom",
        snippet="...",
    )
    
    context = await builder.build("me", mock_email, "creds")
    
    assert context.body_text == "[Error fetching body]"
    assert context.subject == "Doom"
