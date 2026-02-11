import logging
import io
import shutil
import tempfile
import os
from typing import Optional, List, Union, BinaryIO
from pypdf import PdfReader
from pypdf.errors import FileNotDecryptedError

from spine.chapters.action.vault import Vault

logger = logging.getLogger(__name__)

class AttachmentUnlocker:
    """
    UMP-60-04: Attachment Unlocker.
    
    Responsibility: Decrypt password-protected PDF attachments using keys stored in The Vault.
    Flow: 
    1. Check if PDF is encrypted.
    2. detailed_audit: If yes, try keys from Vault (pan, dob, etc.).
    3. If success: Return byte stream of unlocked PDF (or simply confirm it can be read).
    4. If failure: Raise exception for HITL escalation.
    """
    
    def __init__(self, vault: Vault):
        self.vault = vault

    async def attempt_unlock(self, file_stream: Union[BinaryIO, bytes], user_id: str, common_keys: List[str] = ["pan", "dob", "mobile", "customer_id"]) -> bool:
        """
        Attempts to unlock a PDF using keys stored in the user's vault.
        Returns True if successful (or not encrypted), False if all keys fail.
        
        Note: Modifies the file_stream position, but generally works on bytes.
        """
        if isinstance(file_stream, bytes):
            reader_stream = io.BytesIO(file_stream)
        else:
            reader_stream = file_stream
            
        try:
            reader = PdfReader(reader_stream)
            
            if not reader.is_encrypted:
                logger.info("PDF is not encrypted.")
                return True
                
            # It is encrypted. Try keys.
            logger.info("PDF is encrypted. Attempting Vault unlock...")
            
            for key_name in common_keys:
                # 1. Get secret from Vault
                secret_val = await self.vault.stored_get(user_id, key_name)
                
                if not secret_val:
                    continue
                    
                # 2. Try to decrypt
                # pypdf returns: 1=success(user), 2=success(owner), 0=fail
                result = reader.decrypt(secret_val)
                if result > 0:
                    logger.info(f"PDF unlocked successfully with key: {key_name}")
                    return True
            
            logger.warning(f"Failed to unlock PDF with {len(common_keys)} keys.")
            return False
            
        except Exception as e:
            logger.error(f"Error checking/unlocking PDF: {e}")
            return False

    async def extract_text(self, file_stream: Union[BinaryIO, bytes], user_id: str) -> Optional[str]:
        """
        High-level helper: Unlocks and extracts text.
        Returns text if successful, None if failed/locked.
        """
        if isinstance(file_stream, bytes):
            reader_stream = io.BytesIO(file_stream)
        else:
            reader_stream = file_stream
            
        # Ensure we start at 0
        if reader_stream.seekable():
             reader_stream.seek(0)

        try:
            reader = PdfReader(reader_stream)
            
            if reader.is_encrypted:
                logger.info("PDF is encrypted. Attempting Vault unlock...")
                unlocked = False
                
                # Fetch keys from Vault (In real app, this list comes from User config or we iterate known keys)
                # For MVP, we iterate a standard set of keys + maybe a 'default_pdf_password' key
                common_keys = ["pan", "dob", "mobile", "customer_id", "pdf_password"]
                
                for key_name in common_keys:
                    secret_val = await self.vault.stored_get(user_id, key_name)
                    if secret_val:
                        # Try decrypt
                        if reader.decrypt(secret_val) > 0:
                            logger.info(f"PDF unlocked with key: {key_name}")
                            unlocked = True
                            break
                            
                if not unlocked:
                    logger.warning("Failed to unlock PDF with available Vault keys.")
                    return None
            else:
                logger.info("PDF is not encrypted.")
            
            # Extract Text
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
            
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return None
