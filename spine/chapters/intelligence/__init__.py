# UMP: 50-XX (Module Init)
# CONTEXT: Chapter 5: Intelligence & Organization
# PURPOSE: Expose public interface for the chapter.

from .streamer import GmailStreamer

__all__ = ["GmailStreamer"]
