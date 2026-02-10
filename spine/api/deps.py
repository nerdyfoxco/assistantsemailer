from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from spine.core.config import settings
from spine.db.database import get_db
from spine.db.models import User
from spine.db.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    try:
        user_repo = UserRepository(db)
        # The token subject is the user ID (see auth.py)
        print(f"DEBUG: Looking up user ID: {token_data}")
        user = await user_repo.get(id=token_data)
        print(f"DEBUG: User found: {user}")
        if not user:
            print("DEBUG: User not found in DB")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print(f"DEBUG: Error in get_current_user: {e}")
        import traceback
        traceback.print_exc()
        raise e

async def get_workflow_service(
    db: AsyncSession = Depends(get_db)
):
    from spine.services.workflow_service import WorkflowService
    return WorkflowService(db)
