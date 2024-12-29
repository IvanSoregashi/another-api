from copy import deepcopy
from typing import Optional, Literal, Type, Any
from decimal import Decimal
from pydantic import BaseModel, UUID4, Field, create_model
from pydantic.fields import FieldInfo

from app.utils import timestamp, current_year_month
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


def partial_model(model: Type[BaseModel]):
    """
    Decorator, to make existing models, all optional, not too useul here.
    :param model:
    :return:
    """
    def make_field_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
    )


#@partial_model
class TransactionQuery(BaseModel):  # Transaction):
    # TODO Investigate how to make all the fields optional properly
    type: Literal["Expense", "Income", "Transfer"] | None = None
    account: Literal["Forte", "Kaspi", "Cash", "Sber"] | None = None
    category: Literal["Groceries", "Meal", "Paycheck", "Material Items", "Rent & Utilities", "Services", "Transport"] | None = None
    #limit: int = Field(100, gt=0, le=100)
