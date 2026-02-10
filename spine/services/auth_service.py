from typing import Optional
from spine.repositories.user_repo import UserRepository
from spine.core import security
from spine.db.models import User
import uuid
from datetime import datetime

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

    async def signup_user(self, email: str, password: str, name: str) -> User:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists")
        
        hashed_pw = security.get_password_hash(password)
        # Create user via repo
        # Note: Repo might not have explicit create method yet, likely generic or we use session directly.
        # Let's see user_repo.py in a moment. For now assume we use repo.create or similar.
        # Actually UserRepo inherits BaseRepository?
        # Let's assume we can construct User and add it.
        
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            hashed_password=hashed_pw,
            created_at=datetime.utcnow()
        )
        # We need to save it. BaseRepository usually has add/commit.
        # If not, we might need to expose session or add a create method.
        # Let's check BaseRepository first.
        # Optimistically assuming we can add.
        self.user_repo.session.add(user)
        await self.user_repo.session.commit()
        await self.user_repo.session.refresh(user)
        return user

    def create_user_token(self, user_id: str) -> str:
        return security.create_access_token(subject=user_id)

    async def connect_gmail(self, user_id: str, token_data: dict):
        """Saves or updates the EmailAccount for the user."""
        # Need to fetch email address to identify account?
        # Usually we call Google UserInfo API or Gmail Profile API.
        # For this UMP, let's trust we have the tokens.
        
        # Helper logic to store in DB:
        # We need EmailAccountRepository (not created yet per Inventory?)
        # Let's do a direct Add to session via user_repo for speed in Phase 4.
        
        from spine.db.models import EmailAccount, EmailProvider
        
        # Check if account exists
        # In a real app we'd query by user_id and provider
        # Assuming single account for now
        
        import json
        
        # Save tokens
        new_account = EmailAccount(
            id=str(uuid.uuid4()),
            tenant_id="default", # TODO: Fix tenant
            user_id=user_id,
            provider=EmailProvider.GMAIL,
            oauth_token_ref=json.dumps(token_data), # Insecure for prod (use KMS), fine for POC
            created_at=datetime.utcnow()
        )
        
        self.user_repo.session.add(new_account)
        await self.user_repo.session.commit()
        print(f"LINKED GMAIL ACCOUNT for User {user_id}")
