from typing import Literal
from decimal import Decimal
from pydantic import BaseModel, Field

from app.utils import timestamp
from uuid import uuid4


class Month(BaseModel):
    pass
    # TODO


class TransactionId(BaseModel):
    pass
    # TODO


class Transaction(BaseModel):
    transaction_id: str | None = Field(default_factory=lambda: str(uuid4()),
                                         description="Unique transaction identifier")
    month: str | None = None  # Field(default_factory=current_year_month, description="Date in YYYY-MM format")
    datetime: str | None = Field(default_factory=timestamp, description="Timestamp in ISO format, UTC TimeZone")
    type: str
    account: str
    currency: str | None = None
    amount: Decimal
    category: str | None = None
    point: str
    item: str | None = None
    comment: str | None = None

    def model_post_init(self, __context):
        acc_to_cur = {"Forte": "KZT", "Kaspi": "KZT", "Sber": "RUB"}
        point_to_cat = {"Small": "Groceries", "Magnum": "Groceries"}
        self.month = self.datetime[:7]
        if not self.currency:
            self.currency = acc_to_cur.get(self.account)
        if not self.category:
            self.category = point_to_cat.get(self.point)


class TranferTransaction(BaseModel):
    transaction_id: str | None = Field(default_factory=lambda: str(uuid4()),
                                       description="Unique transaction identifier")
    month: str | None = None  # Field(default_factory=current_year_month, description="Date in YYYY-MM format")
    datetime: str | None = Field(default_factory=timestamp, description="Timestamp in ISO format, UTC TimeZone")
    type: str | None = "Transfer"
    from_account: str
    to_account: str
    from_currency: str | None = None
    to_currency: str | None = None
    from_amount: Decimal
    to_amount: Decimal
    category: str | None = None
    point: str
    item: str | None = None
    comment: str | None = None

    def divide(self):
        _from = Transaction(
            month=self.month,
            datetime=self.datetime,
            type=self.type,
            account=self.from_account,
            currency=self.from_currency,
            amount=self.from_amount,
            category=self.category,
            point=self.point,
            item=self.item,
            comment=self.comment,
        )
        _to = Transaction(
            month=self.month,
            datetime=self.datetime,
            type=self.type,
            account=self.to_account,
            currency=self.to_currency,
            amount=self.to_amount,
            category=self.category,
            point=self.point,
            item=self.item,
            comment=self.comment,
        )
        return _from, _to


class TransactionQuery(BaseModel):  # Transaction):
    # TODO Investigate how to make all the fields optional properly
    type: Literal["Expense", "Income", "Transfer"] | None = None
    account: Literal["Forte", "Kaspi", "Cash", "Sber"] | None = None
    category: Literal["Groceries", "Meal", "Paycheck", "Material Items", "Rent & Utilities", "Services", "Transport"] | None = None
    #limit: int = Field(100, gt=0, le=100)
