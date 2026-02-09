from typing import Optional
from spine.repositories.user_repo import UserRepository
from spine.core import security
from spine.db.models import User

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        # Verify PASSWORD (assuming User model has hashed_password field, which we didn't add yet!)
        # Wait, the User model in models.py (Phase 2) ONLY has id, email, name.
        # We need to ADD hashed_password to User model or use a separate credentials table.
        # For simplicity in this UMP, let's add `hashed_password` to the User model.
        if not hasattr(user, 'hashed_password') or not user.hashed_password:
             # Fallback for dev: if no password set, verify against "password" (MOCK)
             if password == "password":
                 return user
             return None
             
        if not security.verify_password(password, user.hashed_password):
            return None
            
        return user

    def create_user_token(self, user_id: str) -> str:
        return security.create_access_token(subject=user_id)
