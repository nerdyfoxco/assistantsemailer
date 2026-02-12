import pytest
from foundation.testing import markers
from foundation.testing.fixtures import foundation_config, in_memory_bus
from foundation.events.bus import InMemoryEventBus
from foundation.config.settings import GlobalSettings

# Test Markers
@markers.unit
def test_unit_marker():
    """This test ensures the unit marker is importable and usable."""
    assert True

@markers.integration
def test_integration_marker():
    """This test ensures the integration marker is importable and usable."""
    assert True

# Test Fixtures (by using them)
def test_foundation_config_fixture(foundation_config):
    assert isinstance(foundation_config, GlobalSettings)
    assert foundation_config.ENV in ["dev", "test", "prod"]

def test_in_memory_bus_fixture(in_memory_bus):
    assert isinstance(in_memory_bus, InMemoryEventBus)
    # Check it's empty
    assert len(in_memory_bus._subscribers) == 0
