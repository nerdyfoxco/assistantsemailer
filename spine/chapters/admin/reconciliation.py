
import os
import stripe
from datetime import datetime
from sqlmodel import Session, select
from spine.chapters.admin.billing import PlanTier, get_plan
from spine.chapters.admin.models import SystemFlag # Leveraging existing models if needed, or we'll create new ones for Subscriptions
# Assuming we might need a Ledger/Subscription model. For UMP-100-04, focus is on "Stripe Logic".

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class Ledger:
    """
    The Source of Truth for Financial/Usage State.
    In a real system, this would write to an immutable Ledger table.
    """
    def __init__(self, session: Session):
        self.session = session
    
    def record_transaction(self, tenant_id: str, amount: int, description: str, stripe_id: str = None):
        """
        Records a financial transaction.
        amount > 0: Charge/Debit.
        amount < 0: Credit/Refund.
        """
        from spine.chapters.admin.models import LedgerEntry
        entry = LedgerEntry(
            tenant_id=tenant_id,
            amount=amount,
            description=description,
            stripe_charge_id=stripe_id,
            timestamp=datetime.utcnow()
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry

    def get_balance(self, tenant_id: str) -> int:
        """Calculates current balance from ledger history."""
        from spine.chapters.admin.models import LedgerEntry
        stmt = select(LedgerEntry).where(LedgerEntry.tenant_id == tenant_id)
        entries = self.session.exec(stmt).all()
        return sum(e.amount for e in entries)

    def get_history(self, tenant_id: str):
        """Returns full transaction history."""
        from spine.chapters.admin.models import LedgerEntry
        stmt = select(LedgerEntry).where(LedgerEntry.tenant_id == tenant_id).order_by(LedgerEntry.timestamp.desc())
        return self.session.exec(stmt).all()

class SubscriptionManager:
    def __init__(self, session: Session):
        self.session = session
        self.ledger = Ledger(session)

    def create_customer(self, email: str, name: str) -> str:
        """Creates a Stripe Customer and returns ID."""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name
            )
            return customer.id
        except Exception as e:
            # Log error
            print(f"Stripe Error: {e}")
            raise e

    def get_subscription_status(self, stripe_customer_id: str) -> PlanTier:
        """
        Queries Stripe to see active subscription.
        Returns PlanTier.
        """
        # Verification Stub: If we don't have a database of subs, we check Stripe directly.
        # In prod, we'd cache this in a 'Tenant' table column.
        try:
            # List subscriptions for customer, status='active'
            subs = stripe.Subscription.list(customer=stripe_customer_id, status='active', limit=1)
            if not subs.data:
                return PlanTier.FREE
            
            # Simplified Logic: Check price ID against known plans
            # For now, return PRO if any active sub exists (Mock logic)
            return PlanTier.PRO
        except Exception:
            return PlanTier.FREE

    def handle_webhook(self, payload: bytes, sig_header: str):
        endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            raise e
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            raise e

        # Handle specific events
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Fulfill order
            self._handle_checkout_success(session)
        
        return {"status": "success"}

    def _handle_checkout_success(self, session):
        stripe_customer_id = session.get("customer")
        # Logic to upgrade tenant in DB
        print(f"Upgrading customer {stripe_customer_id}")
