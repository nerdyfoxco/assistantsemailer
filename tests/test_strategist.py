
import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from spine.chapters.mind.strategist import Strategist, Decision, ActionType
from spine.chapters.mind.llm_client import LLMClient
from spine.chapters.mind.context import ContextBuilder, PromptContext
from spine.db.models import Email

@pytest.mark.asyncio
async def test_strategist_reply_flow():
    """Test full decision flow resulting in a Reply."""
    # Mocks
    mock_llm = MagicMock(spec=LLMClient)
    mock_builder = MagicMock(spec=ContextBuilder)
    
    # Setup Context Return
    mock_ctx = PromptContext(
        message_id="1", sender="mom@home.com", subject="Hi",
        snippet="Hi", body_text="Hi son", attachments_summary="None"
    )
    mock_builder.build = AsyncMock(return_value=mock_ctx)
    
    # Setup LLM Return (Valid JSON)
    mock_llm_response = json.dumps({
        "action": "REPLY",
        "reasoning": "It is your mother.",
        "draft_body": "Hi Mom, love you.",
        "tags": ["personal"]
    })
    mock_llm.think = AsyncMock(return_value=mock_llm_response)
    
    strategist = Strategist(mock_llm, mock_builder)
    email = Email(provider_message_id="1", from_email="mom@home.com", subject="Hi")
    
    # Execute
    decision = await strategist.decide("me", email, "creds")
    
    # Verify
    assert isinstance(decision, Decision)
    assert decision.action == ActionType.REPLY
    assert decision.draft_body == "Hi Mom, love you."
    assert "personal" in decision.tags

@pytest.mark.asyncio
async def test_strategist_json_recovery():
    """Test that strategist cleans markdown blocks from JSON."""
    mock_llm = MagicMock(spec=LLMClient)
    mock_builder = MagicMock(spec=ContextBuilder)
    mock_builder.build = AsyncMock(return_value=PromptContext(
        message_id="1", sender="a", subject="b", snippet="c", body_text="d", attachments_summary="e"
    ))
    
    # Badly formatted response (Markdown blocks)
    bad_response = """
    ```json
    {
        "action": "ARCHIVE",
        "reasoning": "Spam",
        "draft_body": null,
        "tags": []
    }
    ```
    """
    mock_llm.think = AsyncMock(return_value=bad_response)
    
    strategist = Strategist(mock_llm, mock_builder)
    email = Email(provider_message_id="1", from_email="spam", subject="spam")
    
    decision = await strategist.decide("me", email, "creds")
    
    assert decision.action == ActionType.ARCHIVE

@pytest.mark.asyncio
async def test_strategist_error_handling():
    """Test fail-safe escalation."""
    mock_llm = MagicMock(spec=LLMClient)
    mock_llm.think.side_effect = RuntimeError("API Dead")
    
    mock_builder = MagicMock(spec=ContextBuilder)
    mock_builder.build = AsyncMock(return_value=PromptContext(
        message_id="1", sender="a", subject="b", snippet="c", body_text="d", attachments_summary="e"
    ))
    
    strategist = Strategist(mock_llm, mock_builder)
    email = Email(provider_message_id="1", from_email="x", subject="x")
    
    decision = await strategist.decide("me", email, "creds")
    
    assert decision.action == ActionType.ESCALATE
    assert "Internal Error" in decision.reasoning
