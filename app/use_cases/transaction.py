from app.models.transaction import Transaction


def put_transaction(repo, transaction: Transaction) -> dict:
    return repo.put_item(transaction.model_dump())


def get_transaction(repo, month: str, transaction_id: str) -> dict:
    return repo.pull_item({"month": month, "transaction_id": transaction_id})


def query_transactions(repo, month: str) -> list:
    return repo.query_items("month", month)
