import pytest
from unittest.mock import MagicMock, patch
from chapters.connectors.gmail.client import GmailClient
from chapters.connectors.gmail.service import GmailService, EmailIngested
from foundation.events.bus import InMemoryEventBus

@pytest.fixture
def mock_google_creds():
    with patch('chapters.connectors.gmail.client.Credentials') as MockCreds:
        yield MockCreds

@pytest.fixture
def mock_google_build(mock_google_creds):
    with patch('chapters.connectors.gmail.client.build') as MockBuild:
        yield MockBuild

def test_gmail_client_list_messages(mock_google_build):
    # Setup Mock
    mock_service = MagicMock()
    mock_google_build.return_value = mock_service
    mock_service.users().messages().list().execute.return_value = {
        'messages': [{'id': '123', 'threadId': 't1'}]
    }

    client = GmailClient("tenant_1", {"access_token": "token"})
    msgs = client.list_messages()

    assert len(msgs) == 1
    assert msgs[0]['id'] == '123'

def test_gmail_service_ingest(mock_google_build):
    # Setup Client Mock
    mock_service = MagicMock()
    mock_google_build.return_value = mock_service
    mock_service.users().messages().list().execute.return_value = {
        'messages': [{'id': '123'}]
    }
    mock_service.users().messages().get().execute.return_value = {
        'id': '123', 'snippet': 'Hello'
    }

    bus = InMemoryEventBus()
    service = GmailService(bus)
    client = GmailClient("tenant_1", {"access_token": "token"})

    events = service.ingest_emails(client)
    
    assert len(events) == 1
    assert isinstance(events[0], EmailIngested)
    assert events[0].message_id == '123'
    assert events[0].snippet == 'Hello'
