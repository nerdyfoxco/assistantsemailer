
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.base import Base
from spine.core.config import settings

# Use an in-memory SQLite database for tests to ensure isolation and cleanliness
# OR use a file-based one that we delete?
# In-memory is best, but shared across connections can be tricky in async.
# Use shared-cache in-memory: 'sqlite+aiosqlite:///file:memdb1?mode=memory&cache=shared'
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

from sqlalchemy.pool import StaticPool

engine = create_async_engine(
    TEST_DATABASE_URL, 
    echo=False, 
    poolclass=StaticPool, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create tables once for the session."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session():
    """
    Return an async session for each test, rolled back at the end.
    Isolation Level: SERIALIZABLE provided by SQLite, but we use nested transaction simulation via connection.
    """
    # Connect to the engine (which is :memory: static pool)
    async with engine.connect() as connection:
        # Begin a transaction
        trans = await connection.begin()
        
        # Bind session to this connection
        # We need a new sessionmaker that uses this connection
        # But AsyncSession needs 'bind=connection'
        
        session_factory = sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        async with session_factory() as session:
            yield session
            # We do NOT commit here. We just close.
            # The transaction on the connection will be rolled back.
            
        await trans.rollback()

from spine.main import app
from spine.db.database import get_db

@pytest.fixture(autouse=True)
def override_dependency(db_session):
    """Override the app's get_db dependency to use the test session."""
    async def _get_test_db():
        yield db_session
    
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides = {}

from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db_session():
    """Returns a mock AsyncSession that mimics SQLAlchemy behavior."""
    session = AsyncMock()
    
    # Mock execute/scalars/first chain
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_result.scalars.return_value.all.return_value = []
    session.execute.return_value = mock_result
    
    # AsyncSession.add is synchronous
    session.add = MagicMock()
    
    return session
