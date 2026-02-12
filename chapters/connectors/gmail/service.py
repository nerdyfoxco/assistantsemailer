from foundation.events.bus import EventBus
from foundation.events.base import DomainEvent
from foundation.vo.email import EmailAddress # Future use
from .client import GmailClient
import base64
from email.mime.text import MIMEText
from typing import Literal

class EmailIngested(DomainEvent):
    """Event triggered when a new email is fetched."""
    event_type: Literal["email.ingested"] = "email.ingested"
    producer: Literal["gmail.connector"] = "gmail.connector"
    message_id: str
    snippet: str
    # tenant_id and payload inherited from DomainEvent

class GmailService:
    def __init__(self, bus: EventBus):
        self.bus = bus

    def ingest_emails(self, client: GmailClient):
        """Polls inbox and emits events for new messages."""
        messages = client.list_messages()
        events = []
        for msg in messages:
            full_msg = client.get_message(msg['id'])
            event = EmailIngested(
                tenant_id=client.tenant_id, 
                message_id=msg['id'], 
                snippet=full_msg.get('snippet', ''),
                payload=full_msg
            )
            # Emit Event
            # self.bus.publish(event) 
            events.append(event)
            
        return events # Return events for now to verify logic in tests easily

    def send_reply(self, client: GmailClient, to: str, subject: str, body: str, thread_id: str = None):
        """Constructs and sends a reply."""
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return client.send_message(raw)
