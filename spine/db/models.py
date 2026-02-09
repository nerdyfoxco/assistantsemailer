from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from spine.db.base import Base
import enum

# Enums
class TenantPlan(str, enum.Enum):
    FREE = "FREE"
    PRO = "PRO"
    TEAM = "TEAM"
    ENTERPRISE = "ENTERPRISE"

class Role(str, enum.Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"

class EmailProvider(str, enum.Enum):
    GMAIL = "GMAIL"
    OUTLOOK = "OUTLOOK"

class Direction(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"

class WorkItemState(str, enum.Enum):
    NEEDS_REPLY = "NEEDS_REPLY"
    WAITING = "WAITING"
    FYI = "FYI"
    DONE = "DONE"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"

class ConfidenceBand(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# PHASE 1.1 — CORE IDENTITY & TENANCY
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Tenant(Base):
    __tablename__ = "tenants"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    plan: Mapped[TenantPlan] = mapped_column(SAEnum(TenantPlan), default=TenantPlan.FREE)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class TenantMembership(Base):
    __tablename__ = "tenant_memberships"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    role: Mapped[Role] = mapped_column(SAEnum(Role), default=Role.MEMBER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# PHASE 1.2 — EMAIL + WORK CORE
class EmailAccount(Base):
    __tablename__ = "email_accounts"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    provider: Mapped[EmailProvider] = mapped_column(SAEnum(EmailProvider))
    oauth_token_ref: Mapped[str] = mapped_column(String) # Encrypted ref
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Email(Base):
    __tablename__ = "emails"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    provider_message_id: Mapped[str] = mapped_column(String, index=True)
    thread_id: Mapped[str] = mapped_column(String, index=True)
    from_email: Mapped[str] = mapped_column(String)
    # Using JSON for arrays in SQLite/Generic compatibility, or specific PG Arrays
    # For now, simplistic string or JSON
    to_emails: Mapped[Optional[str]] = mapped_column(String) # Comma sep or JSON
    cc_emails: Mapped[Optional[str]] = mapped_column(String)
    subject: Mapped[Optional[str]] = mapped_column(String)
    received_at: Mapped[datetime] = mapped_column(DateTime)
    direction: Mapped[Direction] = mapped_column(SAEnum(Direction))

class WorkItem(Base):
    __tablename__ = "work_items"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"))
    email_id: Mapped[str] = mapped_column(ForeignKey("emails.id"))
    state: Mapped[WorkItemState] = mapped_column(SAEnum(WorkItemState), default=WorkItemState.NEEDS_REPLY)
    owner_type: Mapped[str] = mapped_column(String) # USER | TEAM_MEMBER
    owner_id: Mapped[Optional[str]] = mapped_column(String)
    confidence_band: Mapped[ConfidenceBand] = mapped_column(SAEnum(ConfidenceBand))
    resolution_lock: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
