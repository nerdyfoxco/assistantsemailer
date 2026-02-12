
import pytest
import asyncio
from spine.chapters.hitl.guardrails import validate_url, SafetyViolation
from spine.chapters.hitl.browser_service import SafeBrowserService
import builtins

# --- Guardrail Tests ---

def test_guardrail_valid_https():
    assert validate_url("https://google.com") is True

def test_guardrail_valid_http():
    assert validate_url("http://example.org") is True

def test_guardrail_block_localhost():
    with pytest.raises(SafetyViolation):
        validate_url("http://localhost:8000")

def test_guardrail_block_private_ip():
    with pytest.raises(SafetyViolation) as excinfo:
        validate_url("http://192.168.1.1")
    assert "Resolves to private IP" in str(excinfo.value) or "blocked" in str(excinfo.value)

def test_guardrail_block_scheme():
    with pytest.raises(SafetyViolation):
        validate_url("file:///etc/passwd")

# --- Browser Service Tests ---

@pytest.mark.asyncio
async def test_browser_service_lifecycle():
    service = SafeBrowserService()
    await service.start()
    assert service._browser is not None
    await service.stop()
    assert service._browser is None

@pytest.mark.asyncio
async def test_browser_fetch_example():
    service = SafeBrowserService()
    try:
        data = await service.fetch_page("https://example.com")
        assert data["status"] == 200
        assert "Example Domain" in data["title"]
        assert "More information" in data["text_preview"]
    finally:
        await service.stop()

@pytest.mark.asyncio
async def test_browser_block_bad_url():
    service = SafeBrowserService()
    try:
        with pytest.raises(SafetyViolation):
            await service.fetch_page("http://localhost")
    finally:
        await service.stop()

@pytest.mark.asyncio
async def test_browser_timeout():
    service = SafeBrowserService()
    try:
        # Timeout of 1ms should definitely fail
        with pytest.raises(Exception): 
            await service.fetch_page("https://google.com", timeout_ms=1) 
    finally:
        await service.stop()
