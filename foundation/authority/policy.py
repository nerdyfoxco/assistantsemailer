from pydantic import BaseModel, Field
from typing import List, Optional
from foundation.common.types import ExecutionAuthority

class AuthorityPolicy(BaseModel):
    """
    Defines the policy for who executes a given feature.
    """
    feature_id: str
    authority: ExecutionAuthority
    rollout_percentage: int = 0
    allow_tenants: List[str] = Field(default_factory=list)

    def resolve(self, tenant_id: str = "default") -> ExecutionAuthority:
        """
        Determines the authority for a specific context (tenant).
        Phase 0 Logic: Simple Allowlist + Global Switch.
        """
        # 1. Global Disable
        if self.authority == ExecutionAuthority.DISABLED:
            return ExecutionAuthority.DISABLED

        # 2. Legacy Enforced
        if self.authority == ExecutionAuthority.LEGACY:
            return ExecutionAuthority.LEGACY

        # 3. Canonical / Dual Check
        # If specific tenants are allowed, check them
        if self.allow_tenants:
            if tenant_id in self.allow_tenants:
                return self.authority
            else:
                return ExecutionAuthority.LEGACY

        # 4. Global Rollout (Not implemented yet - strictly 0 or 100 for now)
        # If no allow_tenants set, assumption is it applies to ALL if authority is CANONICAL
        return self.authority
