from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from foundation.lib.logging import StructuredLogger

logger = StructuredLogger.get_logger("gmail.client")

class GmailClient:
    """
    Low-level wrapper for Gmail API interactions.
    Handles token refreshing and API error handling.
    """
    def __init__(self, tenant_id: str, token_data: dict):
        self.tenant_id = tenant_id
        self.creds = Credentials(
            token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=token_data.get("client_id"), # Should come from Config ideally if consistent
            client_secret=token_data.get("client_secret"),
            scopes=["https://www.googleapis.com/auth/gmail.modify"]
        )
        self.service = build('gmail', 'v1', credentials=self.creds)

    def list_messages(self, query: str = "label:INBOX is:unread", max_results: int = 10):
        """Fetch list of message IDs matching query."""
        try:
            results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            logger.info("Fetched messages", count=len(messages), tenant_id=self.tenant_id)
            return messages
        except Exception as e:
            logger.error("Failed to list messages", exception=str(e), tenant_id=self.tenant_id)
            raise

    def get_message(self, msg_id: str):
        """Fetch full message details."""
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            return message
        except Exception as e:
            logger.error(f"Failed to get message {msg_id}", exception=str(e), tenant_id=self.tenant_id)
            raise

    def send_message(self, raw_message: str):
        """Send a raw base64 encoded email."""
        try:
            message = {'raw': raw_message}
            sent_message = self.service.users().messages().send(userId='me', body=message).execute()
            logger.info("Message sent", message_id=sent_message['id'], tenant_id=self.tenant_id)
            return sent_message
        except Exception as e:
            logger.error("Failed to send message", exception=str(e), tenant_id=self.tenant_id)
            raise
