
import logging
from typing import List, Optional, Any

logger = logging.getLogger(__name__)

class Valve:
    """
    UMP-60-02: The Valve (Sender).
    
    Responsibilities:
    1. FINAL Check before sending.
    2. Rate Limiting (Not fully implemented in MVP, but hook exists).
    3. Whitelisting (Optional Dev Mode).
    4. Execution of Gmail Send API.
    """
    
    def __init__(self, service_builder: Any, dev_mode_whitelist: Optional[List[str]] = None):
        self.service_builder = service_builder
        self.whitelist = dev_mode_whitelist or []

    async def send_email(self, user_id: str, creds: Any, raw_message: str, to_address: str) -> bool:
        """
        Executes the send.
        """
        # 1. Safety Check (Whitelist)
        if self.whitelist:
            if not any(allowed in to_address for allowed in self.whitelist):
                logger.warning(f"BLOCKED: {to_address} is not in whitelist.")
                return False
                
        # 2. Rate Limit Check (Future)
        # if not self.rate_limiter.allow(user_id): return False
        
        try:
            # 3. Send via API
            service = self.service_builder('gmail', 'v1', credentials=creds, cache_discovery=False)
            
            message_body = {"raw": raw_message}
            sent_msg = service.users().messages().send(userId="me", body=message_body).execute()
            
            logger.info(f"Email SENT successfully: {sent_msg.get('id')} to {to_address}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to SEND email: {e}")
            raise RuntimeError(f"Send failed: {str(e)}")
