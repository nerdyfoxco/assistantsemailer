from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from spine.db.database import get_db
from spine.contracts.auth_dto import Token, LoginRequest
from spine.services.auth_service import AuthService
from spine.repositories.user_repo import UserRepository
from spine.core import config

router = APIRouter()

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

@router.post("/login", response_model=Token)
async def login_access_token(
    form_data: LoginRequest, # Using JSON body instead of Form for easier API testing/consistency with modern SPAs
    service: AuthService = Depends(get_auth_service)
) -> Any:
    try:
        user = await service.authenticate_user(form_data.email, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise e
    
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_user_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
