# UMP: 50-XX (Module Init)
# CONTEXT: Chapter 5: Intelligence & Organization
# PURPOSE: Expose public interface for the chapter.

from .streamer import GmailStreamer
from .triage import triage_thread, TriageResult
from .processor import IntelligenceProcessor

__all__ = [
    "GmailStreamer",
    "triage_thread",
    "TriageResult",
    "IntelligenceProcessor"
]
