from foundation.common.types import ExecutionAuthority
from foundation.authority.policy import AuthorityPolicy

class AuthorityRegistry:
    """
    Static registry of Authority Policies.
    For Phase 0, this is Code-as-Config.
    For Phase 2+, this will read from DB/Redis.
    """
    _registry: dict[str, AuthorityPolicy] = {}

    @classmethod
    def register(cls, policy: AuthorityPolicy):
        cls._registry[policy.feature_id] = policy

    @classmethod
    def get_policy(cls, feature_id: str) -> AuthorityPolicy:
        return cls._registry.get(feature_id, AuthorityPolicy(
            feature_id=feature_id,
            authority=ExecutionAuthority.LEGACY # DEFAULT SAFERY NET
        ))

    @classmethod
    def resolve(cls, feature_id: str, tenant_id: str = "default") -> ExecutionAuthority:
        policy = cls.get_policy(feature_id)
        return policy.resolve(tenant_id)

    @classmethod
    def reset(cls):
        cls._registry = {}
