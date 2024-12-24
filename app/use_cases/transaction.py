from app.models.transaction import Transaction


async def query_transactions(repo, month: str) -> list:
    return await repo.query_items("month", month)


async def put_transaction(repo, transaction: Transaction) -> dict:
    return await repo.put_item(transaction.model_dump())


async def get_transaction(repo, month: str, transaction_id: str) -> dict:
    return await repo.pull_item({"month": month, "transaction_id": transaction_id})


async def delete_transaction(repo, month: str, transaction_id: str) -> None:
    return await repo.delete_item({"month": month, "transaction_id": transaction_id})
