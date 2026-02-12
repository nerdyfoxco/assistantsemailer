import pytest
from foundation.config.settings import GlobalSettings
from foundation.events.bus import InMemoryEventBus

@pytest.fixture
def foundation_config():
    """
    Returns a fresh GlobalSettings instance for testing.
    Resets environment variable overrides after use implicitly by being function-scoped objects,
    though purely relying on Pydantic's environment reading happens at instantiation.
    """
    return GlobalSettings()

@pytest.fixture
def in_memory_bus():
    """
    Returns a fresh InMemoryEventBus.
    """
    return InMemoryEventBus()
