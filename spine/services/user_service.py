from typing import Optional, List
from spine.repositories.user_repo import UserRepository
from spine.contracts.user_dto import UserCreate, UserUpdate
from spine.db.models import User

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_in: UserCreate) -> User:
        # Business Logic: Check if user exists?
        existing = await self.user_repo.get_by_email(user_in.email)
        if existing:
            raise ValueError("User with this email already exists")
        
        # Mapping DTO to Model
        user_data = user_in.model_dump()
        return await self.user_repo.create(**user_data)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.user_repo.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.user_repo.get_by_email(email)

    async def update_user(self, user_id: str, user_in: UserUpdate) -> Optional[User]:
        update_data = user_in.model_dump(exclude_unset=True)
        return await self.user_repo.update(user_id, **update_data)
