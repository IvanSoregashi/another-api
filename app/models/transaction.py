from typing import Optional
from decimal import Decimal
from pydantic import BaseModel


class Transaction(BaseModel):
    datetime: str
    type: str
    account: str
    currency: Optional[str] = None
    amount: Decimal
    category: Optional[str] = None
    comment: Optional[str] = None

