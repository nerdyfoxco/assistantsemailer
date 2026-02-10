import pytest
from unittest.mock import MagicMock, patch
from googleapiclient.errors import HttpError
from spine.chapters.intelligence.proxy import LiveProxy

# Fixtures
@pytest.fixture
def mock_service():
    mock_s = MagicMock()
    mock_users = MagicMock()
    mock_messages = MagicMock()
    mock_get = MagicMock()
    
    # Chain: service.users().messages().get().execute()
    mock_s.users.return_value = mock_users
    mock_users.messages.return_value = mock_messages
    mock_messages.get.return_value = mock_get
    
    return mock_s, mock_get

@pytest.fixture
def proxy(mock_service):
    service_mock, _ = mock_service
    # Mock builder to return our service mock
    return LiveProxy(service_builder=MagicMock(return_value=service_mock))

# 1. Fetch Success
@pytest.mark.asyncio
async def test_proxy_fetch_success(proxy, mock_service):
    _, mock_get = mock_service
    mock_get.execute.return_value = {
        "id": "m1",
        "snippet": "Hello",
        "payload": {
            "mimeType": "text/html",
            "body": {"data": "PGI+SGVsbG88L2I+"} # <b>Hello</b> base64
        }
    }
    
    result = await proxy.fetch_body("u1", "m1", "creds")
    assert result["id"] == "m1"
    assert "<b>Hello</b>" in result["html"]

# 2. Not Found (404)
@pytest.mark.asyncio
async def test_proxy_not_found(proxy, mock_service):
    _, mock_get = mock_service
    resp = MagicMock(status=404)
    mock_get.execute.side_effect = HttpError(resp=resp, content=b"Not Found")
    
    with pytest.raises(HttpError) as exc:
        await proxy.fetch_body("u1", "bad_id", "creds")
    assert exc.value.resp.status == 404

# 3. Auth Error (401)
@pytest.mark.asyncio
async def test_proxy_auth_error(proxy, mock_service):
    _, mock_get = mock_service
    resp = MagicMock(status=401)
    mock_get.execute.side_effect = HttpError(resp=resp, content=b"Unauthorized")
    
    with pytest.raises(HttpError):
        await proxy.fetch_body("u1", "m1", "bad_creds")

# 4. Sanitization (Script Stripping)
@pytest.mark.asyncio
async def test_proxy_sanitization(proxy, mock_service):
    _, mock_get = mock_service
    # <script>alert(1)</script><b>Safe</b>
    unsafe_b64 = "PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0PjxiPlNhZmU8L2I+"
    mock_get.execute.return_value = {
        "id": "m1",
        "payload": {
            "mimeType": "text/html",
            "body": {"data": unsafe_b64}
        }
    }
    
    result = await proxy.fetch_body("u1", "m1", "creds")
    assert "<script>" not in result["html"]
    assert "<b>Safe</b>" in result["html"]

# 5. Caching (Test mocked behavior - Logic check)
# The proxy currently relies on Gmail API default caching or manual header control. 
# This test ensures we're not aggressively disabling cache without reason?
# Actually code has `cache_discovery=False`.
# We'll just verify the call arguments.
@pytest.mark.asyncio
async def test_proxy_caching_args(proxy):
    with patch("spine.chapters.intelligence.proxy.build") as mock_build:
         # Need to return a runnable mock
         mock_service = MagicMock()
         mock_build.return_value = mock_service
         mock_service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
             "id": "m1", "snippet": "", "payload": {}
         }
         
         # Re-init is tricky if patching imports, but patching the module global 'build' should work 
         # because LiveProxy uses self.service_builder = service_builder or build
         # But if we instantiate LiveProxy WITHOUT arg, it captures the global 'build' (which is patched)
         
         # However, in logical flow:
         # 1. Patch 'spine.chapters.intelligence.proxy.build'
         # 2. Instantiate LiveProxy() -> self.service_builder = (patched build)
         
         # Let's trust the patch ensures 'build' is the mock
         local_proxy = LiveProxy() 
         
         await local_proxy.fetch_body("u1", "m1", "creds")
         
         # Validate
         args, kwargs = mock_build.call_args
         assert args[0] == 'gmail'
         assert args[1] == 'v1'
         assert kwargs['credentials'] == 'creds'
         assert kwargs['cache_discovery'] is False

# 6. Missing ID
@pytest.mark.asyncio
async def test_proxy_missing_id(proxy):
    with pytest.raises(ValueError):
        await proxy.fetch_body("u1", "", "creds")

# 7. HTML Rendering (Preserve Structure)
@pytest.mark.asyncio
async def test_proxy_html_rendering(proxy, mock_service):
    _, mock_get = mock_service
    # <div><p>Test</p></div>
    html_b64 = "PGRpdj48cD5UZXN0PC9wPjwvZGl2Pg=="
    mock_get.execute.return_value = {
        "id": "m1",
        "payload": {
            "mimeType": "text/html",
            "body": {"data": html_b64}
        }
    }
    result = await proxy.fetch_body("u1", "m1", "creds")
    assert "<div><p>Test</p></div>" in result["html"] # Bleach might reorder attributes but structure remains

# 8. Plain Text Fallback
@pytest.mark.asyncio
async def test_proxy_plain_text(proxy, mock_service):
    _, mock_get = mock_service
    # "Just text"
    text_b64 = "SnVzdCB0ZXh0"
    mock_get.execute.return_value = {
        "id": "m1",
        "payload": {
            "mimeType": "text/plain",
            "body": {"data": text_b64}
        }
    }
    result = await proxy.fetch_body("u1", "m1", "creds")
    assert "<pre>Just text</pre>" in result["html"]

# 9. Attachment Handling (Ignored for now / Metadata only?)
# The code currently only looks for text/html or text/plain parts.
# It effectively ignores attachments by not selecting them.
@pytest.mark.asyncio
async def test_proxy_attachment_handling(proxy, mock_service):
    _, mock_get = mock_service
    mock_get.execute.return_value = {
        "id": "m1",
        "payload": {
            "mimeType": "multipart/mixed",
            "parts": [
                {"mimeType": "text/plain", "body": {"data": "T2s="}}, # Ok
                {"mimeType": "application/pdf", "body": {"attachmentId": "att1"}}
            ]
        }
    }
    result = await proxy.fetch_body("u1", "m1", "creds")
    assert "Ok" in result["html"]
    # We assert no crash on attachment part

# 10. Rate Limit (503/429)
@pytest.mark.asyncio
async def test_proxy_rate_limit(proxy, mock_service):
    _, mock_get = mock_service
    resp = MagicMock(status=429)
    mock_get.execute.side_effect = HttpError(resp=resp, content=b"Too Many Requests")
    
    with pytest.raises(HttpError) as exc:
        await proxy.fetch_body("u1", "m1", "creds")
    assert exc.value.resp.status == 429
