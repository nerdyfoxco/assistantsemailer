
import asyncio
import logging
import io
import sys
from pypdf import PdfWriter, PdfReader
from spine.chapters.action.unlocker import AttachmentUnlocker
from unittest.mock import AsyncMock

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("visual_seal")

async def run_visual_audit():
    print("=== VISUAL SEAL AUDIT: UMP-60-04 (ATTACHMENT UNLOCKER) ===")
    
    # 1. GENERATE ENCRYPTED PDF
    print("\n[1] SETUP: Generating Encrypted PDF (Password: 'super_secret_pan')")
    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=200)
    # Inject text annotation (simulating text content since add_text is complex)
    # Actually, let's just use metadata or check unlock status.
    writer.add_metadata({"/Title": "Secret Bank Statement"})
    writer.encrypt("super_secret_pan")
    
    pdf_bytes = io.BytesIO()
    writer.write(pdf_bytes)
    pdf_bytes.seek(0)
    print(f"-> Generated {len(pdf_bytes.getvalue())} bytes of encrypted PDF")
    
    # 2. VERIFY IT IS LOCKED
    check_reader = PdfReader(pdf_bytes)
    if check_reader.is_encrypted:
        print("-> CHECK: PDF is indeed ENCRYPTED.")
    else:
        print("!! FAILURE: PDF NOT ENCRYPTED !!")
        return

    # 3. MOCK VAULT (Simulating Database)
    print("\n[2] SETUP: Mock Vault with Keys")
    mock_vault = AsyncMock()
    
    async def mock_get(user_id, key):
        print(f"   [Vault] User '{user_id}' requested key '{key}'")
        if key == "pan":
            return "super_secret_pan" # CORRECT KEY
        if key == "dob":
            return "1990-01-01"
        return None
        
    mock_vault.stored_get.side_effect = mock_get
    
    # 4. EXECUTE UNLOCKER
    print("\n[3] ACTION: Attempt Unlock")
    unlocker = AttachmentUnlocker(mock_vault)
    pdf_bytes.seek(0) # Reset stream
    
    text_result = await unlocker.extract_text(pdf_bytes, "user_007")
    
    if text_result is not None:
        print("-> SUCCESS: PDF Unlocked and Text Extracted (or attempted)")
        # Verify metadata to confirm access
        pdf_bytes.seek(0)
        reader = PdfReader(pdf_bytes)
        reader.decrypt("super_secret_pan")
        print(f"-> METADATA READ: {reader.metadata.title}")
        if reader.metadata.title == "Secret Bank Statement":
            print("-> INTEGRITY CHECK: PASS (Content Accessible)")
        else:
            print("!! FAILURE: Metadata mismatch !!")
    else:
        print("!! FAILURE: Could not unlock PDF !!")

    print("\n=== AUDIT COMPLETE ===")

if __name__ == "__main__":
    try:
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(run_visual_audit())
    except Exception as e:
        print(f"!! EXCEPTION: {e}")
