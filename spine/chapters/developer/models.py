from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, JSON
import uuid

class APIKey(SQLModel, table=True):
    __tablename__ = "api_keys"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(index=True)
    user_id: uuid.UUID = Field(index=True)
    
    name: str
    prefix: str = Field(index=True) # First 8 chars for display/lookup
    key_hash: str # Hashed secret
    
    scopes: List[str] = Field(default=[], sa_type=JSON)
    
    is_active: bool = Field(default=True)
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used_at: Optional[datetime] = None
