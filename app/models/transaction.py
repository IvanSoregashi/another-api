from typing import Optional, Literal
from decimal import Decimal
from pydantic import BaseModel, Field
from app.utils import timestamp, current_year_month
from uuid import uuid4


class Transaction(BaseModel):
    month: str = None  # Field(default_factory=current_year_month, description="Date in YYYY-MM format")
    transaction_id: Optional[str] = Field(default_factory=lambda: str(uuid4()),
                                          description="Unique transaction identifier")
    datetime: Optional[str] = Field(default_factory=timestamp, description="Timestamp in ISO format, UTC TimeZone")
    type: str
    account: str
    currency: Optional[str] = None
    amount: Decimal
    category: Optional[str] = None
    point: str
    item: Optional[str] = None
    comment: Optional[str] = None

    def model_post_init(self, __context):
        acc_to_cur = {"Forte": "KZT", "Kaspi": "KZT", "Sber": "RUB"}
        point_to_cat = {"Small": "Groceries", "Magnum": "Groceries"}
        self.month = self.datetime[:7]
        if not self.currency:
            self.currency = acc_to_cur.get(self.account)
        if not self.category:
            self.category = point_to_cat.get(self.point)


class TransactionQuery(BaseModel):
    # TODO Investigate how to make all the fields optional properly
    type: Optional[Literal["Expense", "Income", "Transfer"]] = None
    account: Optional[Literal["Forte", "Kaspi", "Cash", "Sber"]] = None
    category: Optional[Literal["Groceries", "Meal", "Paycheck", "Material Items", "Rent & Utilities", "Services", "Transport"]] = None
    #limit: int = Field(100, gt=0, le=100)
