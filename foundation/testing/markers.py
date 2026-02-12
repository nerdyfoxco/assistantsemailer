import pytest

# Define standard markers to be used across the foundation and future modules
# These ensure consistent filtering (e.g., run only unit tests in fast CI)

unit = pytest.mark.unit
integration = pytest.mark.integration
e2e = pytest.mark.e2e
slow = pytest.mark.slow
contract = pytest.mark.contract
