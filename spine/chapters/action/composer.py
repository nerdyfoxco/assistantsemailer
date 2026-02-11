
import logging
import base64
from typing import List, Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class Composer:
    """
    UMP-60-01: The Composer (Drafting).
    
    Responsibilities:
    1. Construct MIME email messages.
    2. Create DRAFTS in Gmail (Safety First: Never Send directly).
    3. Handle templating (Future).
    """
    
    def __init__(self, service_builder: Any):
        """
        :param service_builder: Function to build Gmail Service (See GmailService).
        """
        self.service_builder = service_builder

    async def create_draft(
        self, 
        user_id: str, 
        creds: Any,
        to_email: str, 
        subject: str, 
        body_text: str, 
        body_html: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Creates a draft in Gmail.
        """
        try:
            # 1. Construct MIME Message
            message = MIMEMultipart("alternative")
            message["to"] = to_email
            message["subject"] = subject
            
            # Plain text part (Required)
            part1 = MIMEText(body_text, "plain")
            message.attach(part1)
            
            # HTML part (Optional)
            if body_html:
                part2 = MIMEText(body_html, "html")
                message.attach(part2)
                
            # 2. Encode
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            
            # 3. Create Draft via API
            service = self.service_builder('gmail', 'v1', credentials=creds, cache_discovery=False)
            
            draft_body = {
                "message": {
                    "raw": raw_message
                }
            }
            
            draft = service.users().drafts().create(userId="me", body=draft_body).execute()
            
            logger.info(f"Draft created successfully: {draft.get('id')}")
            return draft
            
        except Exception as e:
            logger.error(f"Failed to create draft: {e}")
            raise RuntimeError(f"Draft creation failed: {str(e)}")
