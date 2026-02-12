
import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from spine.chapters.admin.billing import PlanTier, get_plan
from spine.chapters.admin.reconciliation import SubscriptionManager, Ledger
from spine.chapters.admin.models import LedgerEntry

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_plan_definitions():
    free = get_plan("free")
    assert free.tier == PlanTier.FREE
    assert free.limits.emails_per_day == 50
    
    pro = get_plan("pro")
    assert pro.tier == PlanTier.PRO
    assert pro.limits.emails_per_day == 1000

def test_ledger_recording(session: Session):
    ledger = Ledger(session)
    tenant_id = "tenant_123"
    
    # 1. Record a charge
    entry = ledger.record_transaction(tenant_id, 1000, "Initial Charge")
    assert entry.amount == 1000
    assert entry.tenant_id == tenant_id
    
    # 2. Record a usage fee
    ledger.record_transaction(tenant_id, 500, "Usage Fee")
    
    # 3. Check Balance
    balance = ledger.get_balance(tenant_id)
    assert balance == 1500
    
    # 4. Persistence Check
    entries = session.query(LedgerEntry).filter(LedgerEntry.tenant_id == tenant_id).all()
    assert len(entries) == 2

@patch("stripe.Customer.create")
def test_create_customer(mock_create, session: Session):
    mock_create.return_value = MagicMock(id="cus_test_123")
    
    mgr = SubscriptionManager(session)
    cus_id = mgr.create_customer("test@example.com", "Test User")
    
    assert cus_id == "cus_test_123"
    mock_create.assert_called_once_with(email="test@example.com", name="Test User")

@patch("stripe.Subscription.list")
def test_get_subscription_status_active(mock_list, session: Session):
    # Mock return of active subscription
    mock_sub = MagicMock()
    mock_sub.data = [{"id": "sub_123", "status": "active"}]
    mock_list.return_value = mock_sub
    
    mgr = SubscriptionManager(session)
    tier = mgr.get_subscription_status("cus_test_123")
    
    assert tier == PlanTier.PRO # Based on our simplified logic

@patch("stripe.Subscription.list")
def test_get_subscription_status_none(mock_list, session: Session):
    # Mock empty return (no subs)
    mock_sub = MagicMock()
    mock_sub.data = []
    mock_list.return_value = mock_sub
    
    mgr = SubscriptionManager(session)
    tier = mgr.get_subscription_status("cus_test_123")
    
    assert tier == PlanTier.FREE
