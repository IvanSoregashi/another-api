from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field
from app.utils import timestamp


class Transaction(BaseModel):
    datetime: Optional[str] = Field(default_factory=timestamp, description="Timestamp in ISO format, UTC TimeZone")
    type: str
    account: str
    currency: Optional[str] = None
    amount: Decimal
    category: Optional[str] = None
    comment: Optional[str] = None

