from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Form, Body
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from spine.db.database import get_db
from pydantic import BaseModel
from spine.contracts.auth_dto import Token, LoginRequest, SignupRequest
from spine.services.auth_service import AuthService
from spine.repositories.user_repo import UserRepository
from spine.core import config
from spine.api.deps import get_current_user # Ensure this exists
from spine.db.models import User

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

@router.post("/signup", response_model=Token)
async def signup_access_token(
    form_data: SignupRequest,
    service: AuthService = Depends(get_auth_service)
) -> Any:
    try:
        user = await service.signup_user(form_data.email, form_data.password, form_data.name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        print(f"SIGNUP ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Signup failed")
    
    access_token = service.create_user_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# GOOGLE OAUTH
@router.get("/google/login")
async def google_login():
    """Returns the URL to redirect the user to for Google Login/Connect."""
    # Updated scopes based on user request (added userinfo)
    scope = "https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/userinfo.email"
    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={config.settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={config.settings.GOOGLE_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope={scope}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return {"url": url}

@router.get("/google/callback")
async def google_callback_get(
    code: str,
    error: str = None,
    # NOTE: In a pure GET callback initiated by Google, we don't have the Authorization Header from the Frontend.
    # We rely on the Session or we can pass a 'state' param with the user_id encrypted during login.
    # FOR NOW (MVP): We assume the user is 'demo-user' or we fix the flow to be:
    # Frontend -> Opens Popup -> User Logs in -> Google -> Backend.
    # Backend needs to know WHO the user is to link the account.
    
    # STRATEGY:
    # The User Request implies "Log in" (Auth) OR "Connect" (Link).
    # If this is "Connect", we need the user_id.
    # We'll use a hardcoded 'state' or 'cookie' strategy for Phase 4 MVP, 
    # OR we just redirect back to Frontend with the tokens (unsafe but easy) and let Frontend POST them back.
    
    # WAIT: The User provided 'http://localhost:8000/auth/google/callback'.
    # This is normally a Backend endpoint.
    
    # Let's try to Link to the 'current' user. 
    # Since we can't easily get the header in a browser redirect from Google,
    # We will:
    # 1. Exchange Code -> Tokens.
    # 2. Redirect to Frontend with `?google_token=...` (Pass-through).
    # 3. Frontend catches this and calls `POST /connect_gmail` with the token.
    # This keeps the "Link to User" logic secure in the second step.
):
    if error:
        return RedirectResponse(f"http://localhost:3006/dashboard?error={error}")

    try:
        import httpx
        from fastapi.responses import RedirectResponse
        import json
        import urllib.parse
        
        async with httpx.AsyncClient() as client:
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                "client_id": config.settings.GOOGLE_CLIENT_ID,
                "client_secret": config.settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": config.settings.GOOGLE_REDIRECT_URI
            }
            resp = await client.post(token_url, data=data)
            
            if resp.status_code != 200:
                print(f"GOOGLE TOKEN ERROR: {resp.text}")
                return RedirectResponse(f"http://localhost:3006/dashboard?error=token_failed")
            
            token_data = resp.json()
            # Encode tokens to pass to frontend (Validation step)
            # In a real app, we would encrypt this or store in a temp cache and pass a reference ID.
            # For this MVP, we pass the raw JSON (URL encoded).
            
            token_json = json.dumps(token_data)
            token_encoded = urllib.parse.quote(token_json)
            
            # Redirect to Frontend Callback Handler
            # The Frontend will take this payload and enable the "Link" via API.
            return RedirectResponse(f"http://localhost:3006/auth/google/callback?google_tokens={token_encoded}")

    except Exception as e:
        print(f"GOOGLE CALLBACK ERROR: {e}")
        return RedirectResponse(f"http://localhost:3006/dashboard?error=server_error")

class GoogleConnectRequest(BaseModel):
    tokens: str # JSON string of tokens

@router.post("/google/connect")
async def google_connect(
    payload: GoogleConnectRequest,
    current_user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service)
):
    """Finalizes the connection by determining user and saving tokens."""
    try:
        import json
        token_data = json.loads(payload.tokens)
        
        # Verify tokens likely valid (optional, but good practice)
        # Save to DB
        await service.connect_gmail(current_user.id, token_data)
        
        return {"status": "connected", "email": "unknown_yet@gmail.com"}
    except Exception as e:
        print(f"CONNECT ERROR: {e}")
        raise HTTPException(status_code=400, detail="Invalid token data")
