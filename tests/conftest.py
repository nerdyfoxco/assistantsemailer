import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_db_session():
    """Returns a mock AsyncSession that mimics SQLAlchemy behavior."""
    session = AsyncMock() # Removed spec=AsyncSession to avoid conflicts with manual overrides
    
    # Mock execute/scalars/first chain
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_result.scalars.return_value.all.return_value = []
    session.execute.return_value = mock_result
    
    # AsyncSession.add is synchronous
    session.add = MagicMock()
    
    return session
