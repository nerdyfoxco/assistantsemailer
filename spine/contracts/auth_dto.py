from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None

class LoginRequest(BaseModel):
    email: str
    password: str # For Phase 1 we might just use Email-Only login via Magic Link, but for now Standard PW or Mock
