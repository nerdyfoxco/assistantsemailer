"""
UMP-50-03: Live Body Proxy
--------------------------
Context: Endpoint to fetch email body on-demand.
Purpose: Ephemeral visualization (Zero-Storage).
Security: MUST sanitize HTML (Bleach).
"""

from typing import Dict, Any, Optional
import bleach
import base64
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

# Allowed Tags for Bleach (Safe HTML)
ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul',
    'p', 'br', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table', 'tbody', 'tr', 'td', 'th', 'thead',
    'img', 'hr', 'pre'
]

ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'width', 'height']
}

class LiveProxy:
    def __init__(self, service_builder=None):
        self.service_builder = service_builder or build

    async def fetch_body(self, user_id: str, message_id: str, creds: Any) -> Dict[str, Any]:
        """
        Fetches the full email body from Gmail API and sanitizes it.
        Returns: { "html": str, "snippet": str, "attachments": [] }
        """
        if not user_id or not message_id:
             raise ValueError("Missing user_id or message_id")

        try:
            service = self.service_builder('gmail', 'v1', credentials=creds, cache_discovery=False)
            message = service.users().messages().get(userId=user_id, id=message_id, format='full').execute()
        except HttpError as e:
            # Propagate specific google errors
            raise e
        except Exception as e:
            raise RuntimeError(f"Failed to fetch message: {str(e)}")

        payload = message.get("payload", {})
        parts = payload.get("parts", [])
        
        attachments = []
        
        # Helper to traverse parts
        def traverse(parts_list):
            best_html = None
            best_text = None
            
            for part in parts_list:
                # 1. Collect Attachments (Present if filename + attachmentId)
                fname = part.get("filename")
                body = part.get("body", {})
                att_id = body.get("attachmentId")
                
                if fname and att_id:
                    attachments.append({
                        "filename": fname,
                        "mime_type": part.get("mimeType"),
                        "size": body.get("size"),
                        "attachment_id": att_id
                    })
                
                # 2. Identify Body Candidates
                mime = part.get("mimeType")
                if mime == "text/html":
                    best_html = part
                elif mime == "text/plain":
                    best_text = part
                
                # 3. Recurse (handle multipart/alternative etc)
                if part.get("parts"):
                    sub_html, sub_text = traverse(part["parts"])
                    # Prefer inner match if found
                    if sub_html and not best_html: best_html = sub_html
                    if sub_text and not best_text: best_text = sub_text
            
            return best_html, best_text

        target_html, target_text = traverse(parts)
        
        # Fallback if no parts (root payload is body)
        if not target_html and not target_text:
            mime = payload.get("mimeType")
            if mime == "text/html": target_html = payload
            elif mime == "text/plain": target_text = payload

        target_part = target_html or target_text
        
        body_data = ""
        mime_type = "text/plain"

        if target_part and "body" in target_part and "data" in target_part["body"]:
            raw_data = target_part["body"]["data"]
            # Decode URL-safe Base64
            cleaned_data = raw_data.replace("-", "+").replace("_", "/")
            body_data = base64.b64decode(cleaned_data).decode("utf-8", errors="replace")
            mime_type = target_part.get("mimeType", "text/plain")

        # Sanitization
        if mime_type == "text/html":
            sanitized_html = bleach.clean(
                body_data,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                strip=True # Strip unsafe tags
            )
        else:
            # Convert plain text to simple HTML
            sanitized_html = f"<pre>{bleach.clean(body_data)}</pre>"

        return {
            "id": message["id"],
            "snippet": message.get("snippet", ""),
            "html": sanitized_html,
            "mime_type": mime_type,
            "attachments": attachments
        }
