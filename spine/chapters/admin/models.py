
from typing import Optional, List
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class TenantTier(str, Enum):
    SOLO = "SOLO"
    PRO = "PRO"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"

class TenantStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"

class Organization(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tenants: List["Tenant"] = Relationship(back_populates="organization")

class Tenant(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    organization_id: UUID = Field(foreign_key="organization.id")
    name: str = Field(index=True)
    tier: TenantTier = Field(default=TenantTier.SOLO)
    status: TenantStatus = Field(default=TenantStatus.ACTIVE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    organization: Organization = Relationship(back_populates="tenants")

class AdminUser(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    role: str = Field(default="admin")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str] = None
    tenant_id: UUID = Field(foreign_key="tenant.id", index=True)
    role: str = Field(default="USER")
    status: str = Field(default="ACTIVE")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class SystemFlag(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str # JSON/String value
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: str = Field(default="system")

class LedgerEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    amount: int # In cents
    currency: str = Field(default="usd")
    description: str
    stripe_charge_id: Optional[str] = None
    # Ledger should be append-only. No updates allowed in logic.
