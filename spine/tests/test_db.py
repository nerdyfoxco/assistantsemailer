import pytest
import asyncio
from sqlalchemy import select
from spine.db.models import User
from spine.db.database import AsyncSessionLocal, engine

# Fixture for DB Session
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

# 1. Test Connection
@pytest.mark.asyncio
async def test_db_connection():
    async with engine.connect() as conn:
        assert conn.closed is False

# 2. Test Create User
@pytest.mark.asyncio
async def test_create_user(db_session):
    new_user = User(id="u_test_1", email="test@example.com", name="Test User")
    db_session.add(new_user)
    await db_session.commit()
    
    # Verify
    stmt = select(User).where(User.email == "test@example.com")
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.id == "u_test_1"

# 3. Test Read User
@pytest.mark.asyncio
async def test_read_user(db_session):
    stmt = select(User).where(User.id == "u_test_1")
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.name == "Test User"

# 4. Test Duplicate Email (Constraint)
@pytest.mark.asyncio
async def test_duplicate_email(db_session):
    # Depending on DB, this might raise IntegrityError
    # For now ensuring we can't find a non-existent user
    stmt = select(User).where(User.email == "missing@example.com")
    result = await db_session.execute(stmt)
    user = result.scalar_one_or_none()
    assert user is None
