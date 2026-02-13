from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List, Optional
import uuid
import secrets
from foundation.lib.security import PasswordManager
from .models import APIKey

class ApiKeyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_key(self, user_id: uuid.UUID, tenant_id: uuid.UUID, name: str, scopes: List[str] = []) -> tuple[APIKey, str]:
        """
        Generates a new API Key.
        Returns (APIKey Object, Raw Key String).
        RAW KEY IS SHOWN ONLY ONCE.
        """
        token = secrets.token_urlsafe(32)
        raw_secret = f"sk_live_{token}"
        prefix = raw_secret[:16] # sk_live_ + 8 chars
        key_hash = PasswordManager.get_password_hash(raw_secret)
        
        db_key = APIKey(
            tenant_id=tenant_id,
            user_id=user_id,
            name=name,
            prefix=prefix,
            key_hash=key_hash,
            scopes=scopes
        )
        self.session.add(db_key)
        await self.session.commit()
        await self.session.refresh(db_key)
        
        return db_key, raw_secret

    async def list_keys(self, tenant_id: uuid.UUID) -> List[APIKey]:
        statement = select(APIKey).where(APIKey.tenant_id == tenant_id, APIKey.is_active == True)
        results = await self.session.exec(statement)
        return results.all()

    async def revoke_key(self, key_id: uuid.UUID, tenant_id: uuid.UUID) -> bool:
        db_key = await self.session.get(APIKey, key_id)
        if not db_key or db_key.tenant_id != tenant_id:
            return False
            
        db_key.is_active = False
        self.session.add(db_key)
        await self.session.commit()
        return True

        # Standard: Look up by Prefix (which is plain), then verify hash.
        
        prefix = raw_key[:16]
        statement = select(APIKey).where(APIKey.prefix == prefix, APIKey.is_active == True)
        results = await self.session.exec(statement)
        candidates = results.all()
        
        for key in candidates:
            if PasswordManager.verify_password(raw_key, key.key_hash):
                # Update last used
                # key.last_used_at = datetime.utcnow()
                # await self.session.commit()
                return key
                
        return None
