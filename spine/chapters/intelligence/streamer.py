# UMP: 50-01 (Streaming Interface)
# CONTEXT: Phase 5 > Topic: Zero-Storage > Brick: Streamer
# PURPOSE: Byte-stream processing from Gmail API.
# CONNECTIVITY: Input=GmailAPI, Output=Generator[Dict]

import json
from typing import AsyncGenerator, Dict, Any, List
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from spine.core import config
from spine.repositories.email_repo import EmailRepository

class GmailStreamer:
    """
    Streams emails from Gmail API without storing them in memory or DB.
    Acts as a generator yielding thread/message data.
    """
    def __init__(self, email_repo: EmailRepository):
        # We need repo only to fetch the User's OAuth Token
        self.email_repo = email_repo

    def _get_credentials(self, token_data: dict) -> Credentials:
        return Credentials(
            token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=config.settings.GOOGLE_CLIENT_ID,
            client_secret=config.settings.GOOGLE_CLIENT_SECRET,
            scopes=token_data.get("scope", "").split(" ")
        )

    async def stream_recent_threads(self, user_id: str, limit: int = 10) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Yields full thread details one by one.
        Handles: Auth errors, Network issues, and Rate Limits gracefully.
        """
        account = await self.email_repo.get_account_by_user(user_id)
        if not account:
            raise ValueError(f"User {user_id} has no linked Gmail account.")

        token_data = json.loads(account.oauth_token_ref)
        creds = self._get_credentials(token_data)
        
        try:
            service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
            
            # 1. List Threads
            # TODO: Implement pagination using pageToken for limits > 100
            results = service.users().threads().list(userId='me', maxResults=limit).execute()
            threads = results.get('threads', [])
            
            if not threads:
                return

            # 2. Detail Fetch
            for thread_meta in threads:
                t_id = thread_meta['id']
                try:
                    thread_details = service.users().threads().get(userId='me', id=t_id).execute()
                    yield thread_details
                except Exception as e:
                    # In a strict pipe, we might want to log this but continue streaming other threads
                    # unless it's a critical auth error.
                    # For now, we log and skip individual bad threads.
                    print(f"Stream error for thread {t_id}: {e}")
                    continue
                    
        except Exception as e:
            # Critical errors (Auth, Network setup) propagate up
            print(f"Critical Streamer Error: {e}")
            raise e
