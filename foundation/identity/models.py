from dataclasses import dataclass, field
from typing import List, Optional
import uuid
import datetime

def generate_id():
    return str(uuid.uuid4())

@dataclass
class Tenant:
    id: str = field(default_factory=generate_id)
    name: str = "Default Tenant"
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    plan: str = "TRIAL"

@dataclass
class User:
    id: str = field(default_factory=generate_id)
    email: str = ""
    tenant_id: str = ""
    role: str = "MEMBER"  # OWNER, ADMIN, MEMBER
    is_active: bool = True

@dataclass
class Resource:
    """Base class for any resource that belongs to a tenant."""
    id: str
    tenant_id: str
