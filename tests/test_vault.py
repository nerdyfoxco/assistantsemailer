import pytest
import uuid
from unittest.mock import MagicMock
from sqlalchemy import select
from spine.chapters.action.vault import Vault
from spine.db.models import User, UserVault

# Mocks
class MockSettings:
    SECRET_KEY = "test_secret_key_must_be_32_bytes_base64_url_safe"

@pytest.fixture
def vault(mock_db_session):
    return Vault(mock_db_session)

@pytest.mark.asyncio
async def test_vault_encryption_roundtrip(vault):
    """Test that we can encrypt and decrypt a string."""
    original = "secret_password_123"
    encrypted = vault.encrypt(original)
    
    assert encrypted != original
    assert len(encrypted) > len(original)
    
    decrypted = vault.decrypt(encrypted)
    assert decrypted == original

@pytest.mark.asyncio
async def test_vault_set(vault, mock_db_session):
    """Test storing a value."""
    user_id = "user_123"
    key = "pan_number"
    value = "ABCDE1234F"
    
    # 1. Store
    await vault.stored_set(user_id, key, value)
    
    # Verify DB was called to check existence
    assert mock_db_session.execute.call_count >= 1
    
    # Verify DB Add was called (since mock execute returns None by default)
    assert mock_db_session.add.called
    args, _ = mock_db_session.add.call_args
    stored_obj = args[0]
    
    assert isinstance(stored_obj, UserVault)
    assert stored_obj.user_id == user_id
    assert stored_obj.key_name == key
    assert stored_obj.encrypted_value != value # Encrypted!
    assert vault.decrypt(stored_obj.encrypted_value) == value

@pytest.mark.asyncio
async def test_vault_get(vault, mock_db_session):
    """Test retrieving a value."""
    user_id = "user_123"
    key = "pan_number"
    value = "ABCDE1234F"
    encrypted = vault.encrypt(value)
    
    # Mock the DB query return
    mock_record = UserVault(user_id=user_id, key_name=key, encrypted_value=encrypted)
    
    # Setup the mock chain: execute() -> result -> scalars() -> first() -> mock_record
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_record
    mock_db_session.execute.return_value = mock_result
    
    # Retrieve
    retrieved = await vault.stored_get(user_id, key)
    assert retrieved == value

@pytest.mark.asyncio
async def test_vault_update(vault, mock_db_session):
    """Test updating an existing key."""
    user_id = "user_123"
    key = "api_key"
    value = "v2"
    encrypted = vault.encrypt(value)
    
    # Mock existing record
    existing_record = UserVault(user_id=user_id, key_name=key, encrypted_value="old_enc")
    
    mock_result = MagicMock()
    # First call (check existence) returns existing_record
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_db_session.execute.return_value = mock_result
    
    # Update
    await vault.stored_set(user_id, key, value)
    
    # Verify DB record updated in place
    assert existing_record.encrypted_value != "old_enc"
    assert vault.decrypt(existing_record.encrypted_value) == value
    assert mock_db_session.add.call_count == 0 # Should not add new record
    assert mock_db_session.commit.called

@pytest.mark.asyncio
async def test_vault_delete(vault, mock_db_session):
    """Test deleting a key."""
    user_id = "user_123"
    key = "temp_secret"
    
    # Mock existing
    existing_record = UserVault(user_id=user_id, key_name=key, encrypted_value="ghost")
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = existing_record
    mock_db_session.execute.return_value = mock_result
    
    await vault.stored_delete(user_id, key)
    
    mock_db_session.delete.assert_called_with(existing_record)
    mock_db_session.commit.assert_called()
