from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from enum import StrEnum, auto

class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"

class Money(BaseModel):
    """
    Value object preventing float precision errors for currency.
    """
    amount: Decimal = Field(decimal_places=2) # Enforce scale if validator checked it, otherwise default Decimal
    currency: Currency = Currency.USD

    model_config = ConfigDict(frozen=True)

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money and {type(other)}")
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
        
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError(f"Cannot subtract {type(other)} from Money")
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
            
        return Money(amount=self.amount - other.amount, currency=self.currency)

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
