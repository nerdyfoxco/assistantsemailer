from cryptography.fernet import Fernet
from typing import Optional, Dict
import json
import logging
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

# Use core config for SECRET_KEY
from spine.core.config import settings
from spine.db.models import User

logger = logging.getLogger(__name__)

class Vault:
    """
    UMP-60-03: The Vault (Secrets Manager)
    
    Responsible for securely encrypting and decrypting sensitive user data 
    (e.g., PAN, DOB, external API keys) before persistence.
    
    Encryption: Fernet (Symmetric) using App SECRET_KEY.
    Storage: In 'User.vault_data' column (JSONB or Encrypted Text Blob).
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        # Derive key from settings (ensure 32 url-safe base64-encoded bytes)
        # For simplicity in this prototype, we assume SECRET_KEY is valid or we hash it.
        # In prod, use a proper KMS or strict key management.
        key = settings.SECRET_KEY
        
        # Valid Fernet key must be 32 url-safe base64-encoded bytes.
        # If our SECRET_KEY is just a random string, we might need to adjust.
        # For this implementation, we'll try to use it directly or fall back to a derivation if needed.
        # A robust way is to use a KDF, but let's assume valid key if provided, else generate for dev.
        try:
            self.cipher = Fernet(key.encode() if isinstance(key, str) else key)
        except Exception:
            # Fallback for dev/test if key format is wrong (Warning: Not for Prod)
            # In a real app, strict failure is better.
            logger.warning("Invalid Fernet key in settings. Using ephemeral key (DATA LOSS ON RESTART).")
            self.cipher = Fernet(Fernet.generate_key())

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a string value."""
        if not plaintext:
            return ""
        return self.cipher.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> Optional[str]:
        """Decrypts a string value."""
        if not ciphertext:
            return None
        try:
            return self.cipher.decrypt(ciphertext.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None

    # --- Database Operations ---

    async def stored_get(self, user_id: str, key_name: str) -> Optional[str]:
        """Retrieves and decrypts a value from the user's vault."""
        from spine.db.models import UserVault
        
        stmt = select(UserVault).where(
            UserVault.user_id == user_id,
            UserVault.key_name == key_name
        )
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        
        if not record:
            return None
            
        return self.decrypt(record.encrypted_value)

    async def stored_set(self, user_id: str, key_name: str, value: str):
        """Encrypts and stores (upserts) a value in the user's vault."""
        from spine.db.models import UserVault
        import uuid
        
        encrypted_val = self.encrypt(value)
        
        # Check existing
        stmt = select(UserVault).where(
            UserVault.user_id == user_id,
            UserVault.key_name == key_name
        )
        result = await self.db.execute(stmt)
        existing = result.scalars().first()
        
        if existing:
            existing.encrypted_value = encrypted_val
            existing.updated_at = datetime.utcnow()
        else:
            new_record = UserVault(
                id=str(uuid.uuid4()),
                user_id=user_id,
                key_name=key_name,
                encrypted_value=encrypted_val
            )
            self.db.add(new_record)
        
        await self.db.commit()

    async def stored_delete(self, user_id: str, key_name: str):
        """Removes a key from the user's vault."""
        from spine.db.models import UserVault
        
        stmt = select(UserVault).where(
            UserVault.user_id == user_id,
            UserVault.key_name == key_name
        )
        result = await self.db.execute(stmt)
        record = result.scalars().first()
        
        if record:
            await self.db.delete(record)
            await self.db.commit()

