
import asyncio
from unittest.mock import MagicMock, AsyncMock
from spine.chapters.action.vault import Vault
from spine.db.models import UserVault

async def repro():
    # Setup Mock
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result
    
    # Mock Add (Sync)
    mock_db.add = MagicMock()
    
    vault = Vault(mock_db)
    
    try:
        await vault.stored_set("u1", "k1", "val")
        print("Success!")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(repro())
