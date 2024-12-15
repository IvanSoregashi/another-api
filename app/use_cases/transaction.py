from app.models.transaction import Transaction


def put_transaction(repo, transaction: Transaction) -> bool:
    return repo.put_item(transaction.model_dump())
