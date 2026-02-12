from functools import lru_cache
from foundation.events.bus import InMemoryEventBus
from chapters.connectors.gmail.client import GmailClient # Use mocked in test, real in prod
from chapters.connectors.gmail.service import GmailService
from chapters.work.manager import WorkManager
from chapters.brain.service import BrainService

class Container:
    """Simple DI Container for the Vertical Slice."""
    bus = InMemoryEventBus()
    gmail_service = GmailService(bus)
    work_manager = WorkManager(bus)
    brain_service = BrainService() 
    # Brain ideally would use real LLM provider, defaulting to Mock for now per UMP-03
    
    # In a real app, we'd inject config here.

@lru_cache()
def get_work_manager() -> WorkManager:
    return Container.work_manager

@lru_cache()
def get_brain_service() -> BrainService:
    return Container.brain_service

@lru_cache()
def get_gmail_service() -> GmailService:
    return Container.gmail_service

# For testing override
def get_container():
    return Container
