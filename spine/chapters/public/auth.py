
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from spine.db import get_session
from sqlmodel import Session, select
from spine.chapters.admin.models import User, Tenant, Organization

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

    # 1. Create Organization (1-to-1 Mapping for now for simplicity, or could be shared)
    # Using tenant name as org name for solo signups
    org = Organization(name=req.tenant_name)
    session.add(org)
    session.commit()
    session.refresh(org)

    # 2. Create Tenant (Solo Tier by default) linked to Organization
    tenant = Tenant(
        name=req.tenant_name, 
        tier="SOLO", 
        status="ACTIVE",
        organization_id=org.id
    )
    session.add(tenant)
    session.commit()
    session.refresh(tenant)

    # 3. Create User
    # In a real app, hash the password here.
    # For Vertical Slice, we store it plainly or mock-hashed to satisfy the model if strict.
    # The model has Optional[str], so we can store it.
    user = User(
        email=req.email,
        hashed_password=req.password, # Plaintext for prototype speed/debugging
        tenant_id=tenant.id,
        role="ADMIN",
        status="ACTIVE"
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return SignupResponse(
        user_id=user.id,
        tenant_id=tenant.id,
        message="Account created successfully"
    )
