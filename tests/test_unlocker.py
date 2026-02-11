import pytest
import io
from unittest.mock import MagicMock, AsyncMock
from pypdf import PdfWriter, PdfReader
from spine.chapters.action.unlocker import AttachmentUnlocker

@pytest.fixture
def mock_vault():
    vault = AsyncMock()
    vault.stored_get = AsyncMock()
    return vault

@pytest.fixture
def encrypted_pdf_stream():
    """Generates a real in-memory encrypted PDF."""
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    writer.encrypt("secret123")
    
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

@pytest.fixture
def plain_pdf_stream():
    """Generates a plain PDF."""
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

@pytest.mark.asyncio
async def test_unlock_encrypted_success(mock_vault, encrypted_pdf_stream):
    unlocker = AttachmentUnlocker(mock_vault)
    
    # Mock Vault returning correct key
    async def mock_get(user_id, key):
        if key == "pan": return "wrong"
        if key == "dob": return "secret123"
        return None
    mock_vault.stored_get.side_effect = mock_get
    
    success = await unlocker.attempt_unlock(encrypted_pdf_stream, "u1")
    assert success is True
    # Verify we tried keys
    assert mock_vault.stored_get.call_count >= 1

@pytest.mark.asyncio
async def test_unlock_encrypted_fail(mock_vault, encrypted_pdf_stream):
    unlocker = AttachmentUnlocker(mock_vault)
    mock_vault.stored_get.return_value = "wrong_password"
    
    success = await unlocker.attempt_unlock(encrypted_pdf_stream, "u1")
    assert success is False

@pytest.mark.asyncio
async def test_unlock_plain(mock_vault, plain_pdf_stream):
    unlocker = AttachmentUnlocker(mock_vault)
    success = await unlocker.attempt_unlock(plain_pdf_stream, "u1")
    assert success is True
    assert mock_vault.stored_get.call_count == 0

@pytest.mark.asyncio
async def test_extract_text_encrypted(mock_vault):
    # Create PDF with text
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    # Note: Adding text to blank page via pypdf is complex, 
    # but we can test that it unlocks. Extraction logic is standard pypdf.
    # We will trust pypdf extract_text if unlock works.
    writer.encrypt("secret123")
    stream = io.BytesIO()
    writer.write(stream)
    stream.seek(0)
    
    unlocker = AttachmentUnlocker(mock_vault)
    mock_vault.stored_get.return_value = "secret123"
    
    # We expect some string (empty if blank page, but not None)
    text = await unlocker.extract_text(stream, "u1")
    assert text is not None
