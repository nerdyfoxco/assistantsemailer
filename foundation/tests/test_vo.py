import pytest
from foundation.vo.email import EmailAddress
from foundation.vo.finance import Money, Currency
from decimal import Decimal

# Email Tests
def test_email_normalization():
    e = EmailAddress(address="  TEST@Example.com ")
    assert e.address == "test@example.com"
    assert str(e) == "test@example.com"

def test_email_with_name():
    e = EmailAddress(address="jane@example.com", name="Jane Doe")
    assert str(e) == "Jane Doe <jane@example.com>"

def test_email_validation_failure():
    with pytest.raises(ValueError):
        EmailAddress(address="not-an-email")

def test_email_equality():
    e1 = EmailAddress(address="foo@bar.com")
    e2 = EmailAddress(address="FOO@bar.com") # Case insensitive creation
    assert e1 == e2
    assert e1 == "foo@bar.com" # String equality convenience

# Money Tests
def test_money_creation():
    m = Money(amount=Decimal("10.50"), currency=Currency.USD)
    assert m.amount == Decimal("10.50")
    assert str(m) == "USD 10.50"

def test_money_addition():
    m1 = Money(amount=Decimal("10.00"), currency=Currency.USD)
    m2 = Money(amount=Decimal("5.50"), currency=Currency.USD)
    result = m1 + m2
    assert result.amount == Decimal("15.50")
    assert result.currency == Currency.USD

def test_money_currency_mismatch():
    m1 = Money(amount=Decimal("10.00"), currency=Currency.USD)
    m2 = Money(amount=Decimal("5.50"), currency=Currency.EUR)
    with pytest.raises(ValueError):
        _ = m1 + m2

def test_money_immutability():
    m = Money(amount=Decimal("10.00"))
    with pytest.raises(Exception): # Pydantic Frozen
        m.amount = Decimal("20.00")
