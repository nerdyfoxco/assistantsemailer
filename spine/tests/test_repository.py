import pytest
import pytest_asyncio
from spine.db.database import AsyncSessionLocal, engine
from spine.repositories.user_repo import UserRepository
from spine.db.models import User

@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_repo_create_user(db_session):
    repo = UserRepository(db_session)
    user = await repo.create(id="repo_u1", email="repo1@example.com", name="Repo User")
    assert user.id == "repo_u1"
    assert user.email == "repo1@example.com"

@pytest.mark.asyncio
async def test_repo_get_user(db_session):
    repo = UserRepository(db_session)
    user = await repo.get("repo_u1")
    assert user is not None
    assert user.name == "Repo User"

@pytest.mark.asyncio
async def test_repo_get_by_email(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_by_email("repo1@example.com")
    assert user is not None
    assert user.id == "repo_u1"

@pytest.mark.asyncio
async def test_repo_update_user(db_session):
    repo = UserRepository(db_session)
    user = await repo.update("repo_u1", name="Updated Name")
    assert user.name == "Updated Name"

@pytest.mark.asyncio
async def test_repo_delete_user(db_session):
    repo = UserRepository(db_session)
    deleted = await repo.delete("repo_u1")
    assert deleted is True
    
    # Verify gone
    user = await repo.get("repo_u1")
    assert user is None
