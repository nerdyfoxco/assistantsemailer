from enum import StrEnum, auto

class ExecutionAuthority(StrEnum):
    """
    Defines which system has the authority to execute a specific capability.
    This is the core primitive for the Strangler Fig Pattern.
    """
    LEGACY = auto()      # Old system owns it (Default)
    CANONICAL = auto()   # New system owns it
    DUAL = auto()        # Both run (Shadow mode), Canonical result ignored/logged
    DISABLED = auto()    # Feature turned off
