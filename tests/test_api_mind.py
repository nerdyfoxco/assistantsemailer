
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, AsyncMock
from spine.main import app
from spine.db.models import User, Email, EmailAccount
from spine.chapters.mind.strategist import Decision, ActionType

# We need to mock dependencies to avoid real DB/Gmail/LLM calls
# FastAPIs dependency overrides are perfect for this.

@pytest.fixture
def mock_params():
    return {
        "user_id": "test_user_id",
        "email_id": "msg_123", 
        "gmail_id": "g_123"
    }

@pytest.mark.asyncio
async def test_think_endpoint_success(mock_params):
    """Test POST /mind/think/{id} returns a valid Decision."""
    
    # 1. Mock Dependencies
    mock_strategist = MagicMock()
    mock_decision = Decision(
        action=ActionType.REPLY, 
        reasoning="Test Reasoning", 
        draft_body="Test Draft",
        tags=["test"]
    )
    mock_strategist.decide = AsyncMock(return_value=mock_decision)
    
    mock_email = Email(id=mock_params["email_id"], gmail_id=mock_params["gmail_id"], subject="Test Subject")
    
    mock_service = MagicMock()
    mock_service.email_repo.get_by_gmail_id = AsyncMock(return_value=mock_email)
    mock_service.get_user_credentials = AsyncMock(return_value="fake_creds")
    
    mock_user = User(id=mock_params["user_id"], email="me@test.com")

    # 2. Override Dependencies
    from spine.api.v1.endpoints.mind import get_strategist, get_gmail_service, get_current_user
    
    app.dependency_overrides[get_strategist] = lambda: mock_strategist
    app.dependency_overrides[get_gmail_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: mock_user

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 3. Call Endpoint
        response = await ac.post(f"/api/v1/mind/think/{mock_params['gmail_id']}")
        
    # 4. Verify
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "REPLY"
    assert data["reasoning"] == "Test Reasoning"
    
    # Cleanup
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_think_endpoint_not_found():
    """Test 404 behavior."""
    mock_service = MagicMock()
    mock_service.email_repo.get_by_gmail_id = AsyncMock(return_value=None)
    mock_service.email_repo.get = AsyncMock(return_value=None) # DB ID lookup fail too
    
    mock_user = User(id="u", email="me@test.com")
    
    from spine.api.v1.endpoints.mind import get_gmail_service, get_current_user
    app.dependency_overrides[get_gmail_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/mind/think/missing_id")
        
    assert response.status_code == 404
    app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_execute_endpoint():
    """Test POST /mind/execute."""
    mock_user = User(id="u", email="me@test.com")
    from spine.api.v1.endpoints.mind import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_user

    payload = {
        "message_id": "123",
        "decision": {
            "action": "ARCHIVE",
            "reasoning": "Spam",
            "tags": []
        }
    }
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/v1/mind/execute", json=payload)
        
    assert response.status_code == 202
    app.dependency_overrides = {}
