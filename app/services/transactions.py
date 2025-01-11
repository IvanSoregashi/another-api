from app.repository.repository import AbstractRepository
from app.core.models import Transaction, TransactionQuery


class TransactionService:
    """
    Is this even neccessary?
    Service class that accepts repository and calls its CRUD methods.
    """
    def __init__(self, transactions_repo: AbstractRepository):
        self.transactions_repo: AbstractRepository = transactions_repo

    async def scan(self, filters: TransactionQuery) -> list[Transaction]:
        filters_dict = {k: v for k, v in filters.model_dump().items() if v}
        return await self.transactions_repo.scan_table(filters_dict)

    async def query(self, month: str) -> list:
        return await self.transactions_repo.query_items("month", month)

    async def post(self, transaction: Transaction) -> dict:
        transaction = transaction.model_dump()
        return await self.transactions_repo.post_item(transaction)

    async def put(self, transaction: Transaction) -> dict:
        transaction = transaction.model_dump()
        return await self.transactions_repo.put_item(transaction)

    async def get(self, month: str, transaction_id: str) -> dict:
        return await self.transactions_repo.get_item({"month": month, "transaction_id": transaction_id})

    async def delete(self, month: str, transaction_id: str) -> None:
        return await self.transactions_repo.delete_item({"month": month, "transaction_id": transaction_id})
