import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from spine.services.gmail_service import GmailService
from spine.db.models import EmailAccount, EmailProvider

@pytest.mark.asyncio
async def test_fetch_recent_threads_integration():
    # Mock Repo
    mock_repo = AsyncMock()
    
    # Mock Account
    mock_account = EmailAccount(
        id="123",
        user_id="user1",
        provider=EmailProvider.GMAIL,
        oauth_token_ref='{"access_token": "fake", "refresh_token": "fake", "scope": "email"}'
    )
    mock_repo.get_account_by_user.return_value = mock_account
    
    service = GmailService(mock_repo)
    
    # Mock Google API
    with patch('spine.services.gmail_service.build') as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Mock Threads List
        mock_threads_resource = mock_service.users().threads()
        mock_threads_resource.list.return_value.execute.return_value = {
            'threads': [{'id': 't1', 'snippet': 'Hello'}]
        }
        
        # Mock Thread Get
        mock_threads_resource.get.return_value.execute.return_value = {
            'id': 't1',
            'messages': [
                {
                    'id': 'm1', 
                    'threadId': 't1', 
                    'snippet': 'Hello world',
                    'internalDate': '1600000000000',
                    'payload': {
                        'headers': [
                            {'name': 'Subject', 'value': 'Test Email'},
                            {'name': 'From', 'value': 'sender@example.com'}
                        ]
                    }
                }
            ]
        }
        
        count = await service.fetch_recent_threads("user1")
        
        assert count == 1
        mock_repo.create_or_update.assert_called_once()
        # Verify call args
        call_args = mock_repo.create_or_update.call_args[0][0]
        assert call_args['subject'] == 'Test Email'
        assert call_args['snippet'] == 'Hello world'
