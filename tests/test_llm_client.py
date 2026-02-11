
import pytest
from spine.chapters.mind.llm_client import LLMClient, MockLLMProvider

@pytest.mark.asyncio
async def test_synapse_mock_response():
    """Test that the Synapse returns mock data correctly."""
    mock_provider = MockLLMProvider(predefined_responses={
        "Hello": "Hi there, human.",
        "Solve": "The answer is 42."
    })
    client = LLMClient(mock_provider)
    
    response = await client.think("Hello, computer.")
    assert response == "Hi there, human."
    
    response2 = await client.think("Solve this math problem.")
    assert response2 == "The answer is 42."

@pytest.mark.asyncio
async def test_synapse_default_response():
    """Test fallback response."""
    mock_provider = MockLLMProvider()
    client = LLMClient(mock_provider)
    
    response = await client.think("Unknown prompt")
    assert "Mock LLM" in response
