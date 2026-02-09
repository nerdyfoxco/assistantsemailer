import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from spine.main import app
from spine.core.config import settings

# E2E Tests hitting the actual API endpoints (using AsyncClient)

@pytest.mark.asyncio
async def test_create_user_api():
    uid = str(uuid.uuid4())
    email = f"test_{uid}@example.com"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        user_data = {
            "email": email,
            "name": "API Test User",
            "id": f"api_{uid}"
        }
        response = await ac.post(f"{settings.API_V1_STR}/users/", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["id"] == f"api_{uid}"

@pytest.mark.asyncio
async def test_get_user_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create
        user_data = {
            "email": "api_get@example.com",
            "name": "API Get User",
            "id": "api_u2"
        }
        await ac.post(f"{settings.API_V1_STR}/users/", json=user_data)
        
        # Get
        response = await ac.get(f"{settings.API_V1_STR}/users/api_u2")
        
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Get User"

@pytest.mark.asyncio
async def test_update_user_api():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create
        user_data = {
            "email": "api_update@example.com",
            "name": "Old Name",
            "id": "api_u3"
        }
        await ac.post(f"{settings.API_V1_STR}/users/", json=user_data)
        
        # Update
        update_data = {"name": "New Name"}
        response = await ac.patch(f"{settings.API_V1_STR}/users/api_u3", json=update_data)
        
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
