import json
from datetime import datetime
from typing import List, Optional
from spine.repositories.email_repo import EmailRepository
from spine.core import config
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from spine.db.models import Direction

class GmailService:
    def __init__(self, email_repo: EmailRepository):
        self.email_repo = email_repo

    async def get_user_credentials(self, user_id: str) -> Optional[Credentials]:
        """Retrieves Google OAuth Credentials for a user."""
        account = await self.email_repo.get_account_by_user(user_id)
        if not account:
            return None
        token_data = json.loads(account.oauth_token_ref)
        return self._get_credentials(token_data)

    def _get_credentials(self, token_data: dict) -> Credentials:
        return Credentials(
            token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=config.settings.GOOGLE_CLIENT_ID,
            client_secret=config.settings.GOOGLE_CLIENT_SECRET,
            scopes=token_data.get("scope", "").split(" ")
        )

    async def fetch_recent_threads(self, user_id: str, limit: int = 10) -> int:
        """
        Fetches recent X threads for the user and saves them.
        Returns count of new emails processed.
        """
        account = await self.email_repo.get_account_by_user(user_id)
        if not account:
            raise ValueError("No linked Gmail account found for user.")

        token_data = json.loads(account.oauth_token_ref)
        creds = self._get_credentials(token_data)
        
        # Build service
        service = build('gmail', 'v1', credentials=creds)
        
        # List threads
        results = service.users().threads().list(userId='me', maxResults=limit).execute()
        threads = results.get('threads', [])
        
        count = 0
        for thread_meta in threads:
            t_id = thread_meta['id']
            # Get full thread details
            thread_details = service.users().threads().get(userId='me', id=t_id).execute()
            messages = thread_details.get('messages', [])
            
            for msg in messages:
                # Process each message
                email_data = self._parse_message(msg)
                await self.email_repo.create_or_update(email_data)
                count += 1
                
        await self.email_repo.session.commit()
        return count

    def _parse_message(self, msg: dict) -> dict:
        """Parses raw Gmail message dict into Email model compatible dict."""
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        
        snippet = msg.get('snippet', '')
        internal_date = int(msg['internalDate']) / 1000.0
        received_at = datetime.fromtimestamp(internal_date)
        
        subject = headers.get('Subject', '(No Subject)')
        from_email = headers.get('From', '')
        to_emails = headers.get('To', '') # Keep as string for now
        cc_emails = headers.get('Cc', '')
        
        # Determine direction (simplified check)
        # If 'me' is in From, it's OUTBOUND. But we don't know 'me' email easily here without profile.
        # Check labelIds for 'SENT'
        label_ids = msg.get('labelIds', [])
        direction = Direction.OUTBOUND if 'SENT' in label_ids else Direction.INBOUND
        
        # Body extraction (simplified)
        body_text = snippet # Fallback
        # TODO: Deep payload parsing for text/plain parts
        
        return {
            "gmail_id": msg['id'],
            "thread_id": msg['threadId'],
            "provider_message_id": headers.get('Message-ID', msg['id']),
            "subject": subject,
            "from_email": from_email,
            "to_emails": to_emails,
            "cc_emails": cc_emails,
            "snippet": snippet,
            "body_text": body_text,
            "received_at": received_at,
            "direction": direction,
            "is_read": 'UNREAD' not in label_ids
        }
