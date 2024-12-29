from sqlalchemy.orm import Mapped, mapped_column

from app.db.aiosqlite_sqlalchemy import Base


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
    item: Mapped[str]
    comment: Mapped[str]
