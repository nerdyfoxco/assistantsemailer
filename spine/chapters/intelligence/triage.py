"""
UMP-50-02: In-Memory Triage (The Logic)
---------------------------------------
Context: Receives raw thread data from Streamer.
Purpose: Analyzes metadata to determine Priority and State WITHOUT storing body.
Rules: Pure function, no DB side effects, strict schema.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
import re

# === Schema Definitions ===
class ConfidenceBand(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class WorkItemState(str, Enum):
    NEEDS_REPLY = "NEEDS_REPLY"
    WAITING = "WAITING"
    FYI = "FYI"
    DONE = "DONE"
    SPAM = "SPAM" 

class TriageResult(BaseModel):
    """Output schema for the Triage process."""
    thread_id: str
    message_id: str
    subject: str
    sender: str
    received_at: datetime
    confidence: ConfidenceBand
    suggested_state: WorkItemState
    is_vip: bool = False
    tags: List[str] = Field(default_factory=list)
    snippet: str

# === Configuration (Could be injected, but keeping simple for Brick) ===
URGENT_KEYWORDS = ["urgent", "asap", "emergency", "immediate", "deadline"]
SPAM_KEYWORDS = ["verify your account", "claim your prize", "lottery", "won"]
VIP_DOMAINS = ["vip.com", "internal.com"]

# === The Logic ===
def triage_thread(thread_data: Dict[str, Any]) -> TriageResult:
    """
    Pure function to analyze a Gmail Thread dict and return Triage Metadata.
    """
    # 1. Extraction (Fail gracefully on malformed data)
    try:
        t_id = thread_data.get("id", "unknown")
        messages = thread_data.get("messages", [])
        if not messages:
            # Handle empty thread (shouldn't happen from API usually, but defensive)
            return TriageResult(
                thread_id=t_id,
                message_id="unknown",
                subject="(No Messages)",
                sender="unknown",
                received_at=datetime.utcnow(),
                confidence=ConfidenceBand.LOW,
                suggested_state=WorkItemState.DONE,
                snippet=""
            )

        # Look at the last message for current state
        last_msg = messages[-1]
        msg_id = last_msg.get("id", "unknown")
        payload = last_msg.get("payload", {})
        headers = payload.get("headers", [])
        
        # Helper to get header
        def get_header(name: str) -> str:
            val = next((h["value"] for h in headers if h["name"].lower() == name.lower()), "")
            return val

        subject = get_header("subject") or "(No Subject)"
        sender = get_header("from") or "unknown"
        
        # internalDate is ms timestamp
        internal_date = int(last_msg.get("internalDate", 0))
        received_at = datetime.utcfromtimestamp(internal_date / 1000.0)
        
        snippet = last_msg.get("snippet", "")

    except Exception as e:
        # Fallback for severe malformed data
        return TriageResult(
            thread_id=thread_data.get("id", "error"),
            message_id="error",
            subject="Error Processing Thread",
            sender="error",
            received_at=datetime.utcnow(),
            confidence=ConfidenceBand.LOW,
            suggested_state=WorkItemState.DONE,
            tags=["error", str(e)],
            snippet=""
        )

    # 2. Analysis
    confidence = ConfidenceBand.MEDIUM
    state = WorkItemState.NEEDS_REPLY
    tags = []
    is_vip = False
    
    # 2.1 Urgent Assessment
    # Handle encoding/special chars implicitly via python strings
    subj_lower = subject.lower()
    if any(k in subj_lower for k in URGENT_KEYWORDS):
        confidence = ConfidenceBand.HIGH
        tags.append("urgent")

    # 2.2 VIP Assessment
    # Simple check on sender email
    if any(d in sender.lower() for d in VIP_DOMAINS):
        is_vip = True
        confidence = ConfidenceBand.HIGH
        tags.append("vip")

    # 2.3 Spam Detection
    if any(k in subj_lower for k in SPAM_KEYWORDS):
        state = WorkItemState.SPAM
        confidence = ConfidenceBand.LOW
    
    # 2.4 Payload/Performance Check (Implicit)
    # If snippet is huge, currently we just pass it through, but we could truncate.
    # Triage is metadata only, so we don't look at body.

    # 3. Construct Result (Schema Compliance)
    return TriageResult(
        thread_id=t_id,
        message_id=msg_id,
        subject=subject,
        sender=sender,
        received_at=received_at,
        confidence=confidence,
        suggested_state=state,
        is_vip=is_vip,
        tags=tags,
        snippet=snippet
    )
