from enum import Enum

class HitlState(str, Enum):
    PENDING = "PENDING"      # Waiting in queue
    CLAIMED = "CLAIMED"      # Human is looking at it
    RESOLVED = "RESOLVED"    # Decision made (Approved/Edited)
    REJECTED = "REJECTED"    # Decision made (Rejected/Escalated)
