
import logging
import re
from typing import List, Optional, Union, BinaryIO, Any
from spine.chapters.intelligence.proxy import LiveProxy
from spine.chapters.action.unlocker import AttachmentUnlocker
from spine.db.models import User

logger = logging.getLogger(__name__)

class AttachmentService:
    """
    UMP-60-05: Smart Attachment Service.
    
    Orchestrates:
    1. Fetching body ephemerally (LiveProxy).
    2. Extracting password hints (Context Awareness).
    3. Unlocking attachments (Unlocker).
    """
    
    def __init__(self, unlocker: AttachmentUnlocker):
        self.unlocker = unlocker
        self.proxy = LiveProxy() 

    async def smart_unlock(self, user_id: str, message_id: str, file_bytes: bytes, creds: Any) -> bool:
        """
        Attempts to unlock an attachment using both Vault keys AND context from the email body.
        Requires Gmail Credentials to fetch the body for context.
        """
        # 1. First, try "Fast Unlock" with standard Vault keys (Cheapest)
        # This checks the usual suspects: PAN, DOB, etc.
        is_unlocked = await self.unlocker.attempt_unlock(file_bytes, user_id)
        if is_unlocked:
            return True
            
        # 2. If failed, perform "Deep Read" (Fetch Body)
        logger.info(f"Fast unlock failed for {message_id}. Attempting Context-Aware Unlock...")
        
        try:
            # Ephemeral Read: Fetch body into memory
            body_data = await self.proxy.fetch_body("me", message_id, creds)
            
            # Combine snippet + body text (if available) for analysis
            full_text = (body_data.get("snippet", "") + " " + body_data.get("body_text", "")).lower()
            
            # 3. Extract Hints (Intelligent Context)
            hints = self.extract_hints(full_text)
            
            if not hints:
                logger.info("No new context hints found in body.")
                return False
                
            logger.info(f"Found context hints: {hints}")
            
            # 4. Retry Unlock with Specific Hints
            # The unlocker accepts a list of keys to try from the Vault.
            # We pass the hints as the keys to try.
            is_unlocked_smart = await self.unlocker.attempt_unlock(file_bytes, user_id, common_keys=hints)
            
            return is_unlocked_smart

        except Exception as e:
            logger.error(f"Context awareness failed: {e}")
            return False

    def extract_hints(self, text: str) -> List[str]:
        """
        Analyzes text for common password patterns and maps them to Vault Keys.
        """
        hints = []
        
        # Mapping: Trigger Word -> Vault Key
        # If the email says "Enter your PAN", we should try the 'pan' key from Vault.
        triggers = {
            "pan": "pan",
            "permanent account number": "pan",
            "date of birth": "dob",
            "dob": "dob",
            "birth date": "dob",
            "mobile": "mobile",
            "phone": "mobile",
            "customer id": "customer_id",
            "cust id": "customer_id",
            "client id": "client_id"
        }
        
        for phrase, vault_key in triggers.items():
            if phrase in text:
                hints.append(vault_key)
            
        return list(set(hints))
