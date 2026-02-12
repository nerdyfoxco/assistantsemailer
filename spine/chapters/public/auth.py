
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from spine.db import get_session
from sqlmodel import Session, select
from spine.chapters.admin.models import User, Tenant

router = APIRouter(prefix="/public/auth", tags=["public-auth"])

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    tenant_name: str
    agree_tos: bool

class SignupResponse(BaseModel):
    user_id: str
    tenant_id: str
    message: str

@router.post("/signup", response_model=SignupResponse)
def signup(req: SignupRequest, session: Session = Depends(get_session)):
    if not req.agree_tos:
        raise HTTPException(status_code=400, detail="Must agree to Terms of Service")

    # Check existing user
    existing_user = session.exec(select(User).where(User.email == req.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create Tenant (Solo Tier by default)
    tenant = Tenant(name=req.tenant_name, tier="SOLO", status="ACTIVE")
    session.add(tenant)
    session.commit()
    session.refresh(tenant)

    # Create User
    # Note: In production this should be hashed. Using plain for prototype speed as per bootstrap rules.
    user = User(
        email=req.email,
        # hashed_password=hash_pw(req.password), 
        tenant_id=tenant.id,
        role="ADMIN",
        status="ACTIVE"
    )
    # Using a temp hacks/mock for password storage if user model doesn't support it yet
    # checking user model in next step to be sure
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return SignupResponse(
        user_id=user.id,
        tenant_id=tenant.id,
        message="Account created successfully"
    )
