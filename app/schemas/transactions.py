from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.sqlalchemy_base import Base


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(primary_key=True)
    month: Mapped[str]
    datetime: Mapped[str]
    type: Mapped[str]
    account: Mapped[str]
    currency: Mapped[str]
    amount: Mapped[float]
    category: Mapped[str]
    point: Mapped[str]
    item: Mapped[str | None]
    comment: Mapped[str | None]
