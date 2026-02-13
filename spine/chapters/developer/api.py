from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import uuid
from pydantic import BaseModel

from spine.db.database import get_db
from .service import ApiKeyService, APIKey

router = APIRouter(prefix="/developer/keys", tags=["developer"])

# DTOs
class KeyCreateRequest(BaseModel):
    name: str
    scopes: List[str] = []

class KeyResponse(BaseModel):
    id: uuid.UUID
    name: str
    prefix: str
    created_at: str
    scopes: List[str]

class KeyCreatedResponse(KeyResponse):
    raw_key: str

# Endpoints
@router.post("/", response_model=KeyCreatedResponse)
async def create_api_key(
    req: KeyCreateRequest, 
    session: AsyncSession = Depends(get_db)
):
    # TODO: Get real user/tenant from Auth Middleware
    # Mocking for Vertical Slice Phase 12
    mock_user_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    mock_tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    service = ApiKeyService(session)
    db_key, raw_key = await service.create_key(mock_user_id, mock_tenant_id, req.name, req.scopes)
    
    return KeyCreatedResponse(
        id=db_key.id,
        name=db_key.name,
        prefix=db_key.prefix,
        created_at=db_key.created_at.isoformat(),
        scopes=db_key.scopes,
        raw_key=raw_key
    )

@router.get("/", response_model=List[KeyResponse])
async def list_api_keys(
    session: AsyncSession = Depends(get_db)
):
    mock_tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    service = ApiKeyService(session)
    keys = await service.list_keys(mock_tenant_id)
    
    return [
        KeyResponse(
            id=k.id,
            name=k.name,
            prefix=k.prefix,
            created_at=k.created_at.isoformat(),
            scopes=k.scopes
        ) for k in keys
    ]

@router.delete("/{key_id}")
async def revoke_api_key(
    key_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    mock_tenant_id = uuid.UUID("00000000-0000-0000-0000-000000000001")
    
    service = ApiKeyService(session)
    success = await service.revoke_key(key_id, mock_tenant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"status": "revoked"}
