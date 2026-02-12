from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from spine.db.base import Base
from spine.chapters.hitl.states import HitlState

class HitlRequest(Base):
    __tablename__ = "hitl_requests"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String, index=True)
    work_item_id: Mapped[str] = mapped_column(String, index=True) # Soft link to WorkItem
    
    # Why is this here?
    reason: Mapped[str] = mapped_column(String) # "Ambiguity", "Policy Conflict", "Low Confidence"
    context_json: Mapped[str] = mapped_column(String) # JSON dump of relevant context
    
    # State tracking
    state: Mapped[HitlState] = mapped_column(SAEnum(HitlState), default=HitlState.PENDING)
    
    # Who is working on it?
    claimed_by_agent_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class HitlDecision(Base):
    __tablename__ = "hitl_decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    request_id: Mapped[str] = mapped_column(ForeignKey("hitl_requests.id"))
    
    agent_id: Mapped[str] = mapped_column(String)
    outcome: Mapped[HitlState] = mapped_column(SAEnum(HitlState)) # RESOLVED | REJECTED
    
    # The output
    modified_draft: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    feedback_notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
