from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, Any
import re

class EmailAddress(BaseModel):
    """
    Value object representing an email address.
    Enforces basic formatting and case normalization (lowercase).
    """
    address: str
    name: Optional[str] = None
    
    model_config = ConfigDict(frozen=True) # Value Objects must be immutable

    @field_validator("address")
    @classmethod
    def validate_and_normalize(cls, v: Any) -> str:
        if not isinstance(v, str):
            raise ValueError("Email address must be a string")
        
        # Simple regex for structure check (not perfect, but sufficient for strict typing)
        # We rely on sender validation downstream or strict parsing library if needed.
        # This is primarily to block "obviously wrong" strings.
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
            
        return v.lower().strip()

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} <{self.address}>"
        return self.address

    def __repr__(self) -> str:
        return f"EmailAddress(address='{self.address}', name={repr(self.name)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.address == other.lower().strip()
        if isinstance(other, EmailAddress):
            return self.address == other.address
        return False
