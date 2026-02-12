import pytest
from foundation.common.types import ExecutionAuthority
from foundation.authority.policy import AuthorityPolicy
from foundation.authority.registry import AuthorityRegistry

def test_enums():
    assert ExecutionAuthority.LEGACY == "legacy"
    assert ExecutionAuthority.CANONICAL == "canonical"

def test_policy_resolution_legacy():
    policy = AuthorityPolicy(feature_id="test", authority=ExecutionAuthority.LEGACY)
    assert policy.resolve("tenant_1") == ExecutionAuthority.LEGACY

def test_policy_resolution_canonical_global():
    policy = AuthorityPolicy(feature_id="test", authority=ExecutionAuthority.CANONICAL)
    assert policy.resolve("tenant_1") == ExecutionAuthority.CANONICAL

def test_policy_resolution_canonical_tenant_allow():
    policy = AuthorityPolicy(
        feature_id="test", 
        authority=ExecutionAuthority.CANONICAL,
        allow_tenants=["tenant_vip"]
    )
    # VIP -> Canonical
    assert policy.resolve("tenant_vip") == ExecutionAuthority.CANONICAL
    # Random -> Legacy (Safe Fallback)
    assert policy.resolve("tenant_random") == ExecutionAuthority.LEGACY

def test_registry_default():
    AuthorityRegistry.reset()
    # Unregistered feature -> Legacy
    auth = AuthorityRegistry.resolve("unknown_feature")
    assert auth == ExecutionAuthority.LEGACY

def test_registry_registration():
    AuthorityRegistry.reset()
    policy = AuthorityPolicy(feature_id="my_feature", authority=ExecutionAuthority.CANONICAL)
    AuthorityRegistry.register(policy)
    
    auth = AuthorityRegistry.resolve("my_feature")
    assert auth == ExecutionAuthority.CANONICAL
