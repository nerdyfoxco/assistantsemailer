import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from spine.main import app
from spine.core.config import settings
from spine.db.database import AsyncSessionLocal
from spine.db.models import User
from spine.core.security import get_password_hash

@pytest.mark.asyncio
async def test_login_access_token():
    # 1. Seed User
    uid = str(uuid.uuid4())
    email = f"auth_{uid}@example.com"
    password = "securepassword123"
    hashed = get_password_hash(password)
    
    async with AsyncSessionLocal() as session:
        user = User(
            id=f"u_{uid}",
            email=email,
            name="Auth Test User",
            hashed_password=hashed
        )
        session.add(user)
        await session.commit()

    # 2. Attempt Login
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login_data = {
            "email": email,
            "password": password
        }
        response = await ac.post(f"{settings.API_V1_STR}/auth/login", json=login_data)
        
    # 3. Verify Token
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_fail_wrong_password():
    # 1. Seed User
    uid = str(uuid.uuid4())
    email = f"auth_fail_{uid}@example.com"
    password = "securepassword123"
    hashed = get_password_hash(password)
    
    async with AsyncSessionLocal() as session:
        user = User(
            id=f"u_{uid}",
            email=email,
            name="Auth Fail User",
            hashed_password=hashed
        )
        session.add(user)
        await session.commit()

    # 2. Attempt Login with WRONG password
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login_data = {
            "email": email,
            "password": "wrongpassword"
        }
        response = await ac.post(f"{settings.API_V1_STR}/auth/login", json=login_data)
        
    assert response.status_code == 400
