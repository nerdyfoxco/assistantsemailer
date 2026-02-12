
from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict, Any

class PlanTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class PlanLimits(BaseModel):
    emails_per_day: int
    ai_invocations_per_day: int
    storage_mb: int
    can_use_safe_browsing: bool
    can_use_kill_switch: bool # Only admins/custom plans might change this, but good to track

class Plan(BaseModel):
    id: str
    name: str
    tier: PlanTier
    limits: PlanLimits
    stripe_price_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

# Define Standard Plans
PLANS = {
    PlanTier.FREE: Plan(
        id="plan_free",
        name="Solo",
        tier=PlanTier.FREE,
        limits=PlanLimits(
            emails_per_day=50,
            ai_invocations_per_day=100,
            storage_mb=500,
            can_use_safe_browsing=False,
            can_use_kill_switch=False
        )
    ),
    PlanTier.PRO: Plan(
        id="plan_pro",
        name="Professional",
        tier=PlanTier.PRO,
        limits=PlanLimits(
            emails_per_day=1000,
            ai_invocations_per_day=5000,
            storage_mb=5000,
            can_use_safe_browsing=True,
            can_use_kill_switch=False
        ),
        stripe_price_id="price_H5ggYJ..." # Placeholder
    ),
    PlanTier.ENTERPRISE: Plan(
        id="plan_ent",
        name="Enterprise",
        tier=PlanTier.ENTERPRISE,
        limits=PlanLimits(
            emails_per_day=100000,
            ai_invocations_per_day=100000,
            storage_mb=50000,
            can_use_safe_browsing=True,
            can_use_kill_switch=True
        )
    )
}

def get_plan(tier: str) -> Plan:
    try:
        return PLANS[PlanTier(tier)]
    except ValueError:
        return PLANS[PlanTier.FREE]
