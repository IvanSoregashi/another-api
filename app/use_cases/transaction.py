from app.models.transaction import Transaction


def put_transaction(repo, transaction: Transaction) -> dict:
    return repo.put_item(transaction.model_dump())


def get_transaction(repo, datetime: str) -> dict:
    return repo.get_item({"datetime": datetime})


def get_dates_transactions(repo, date: str) -> dict:
    return repo.get_items_that_start_with("datetime", date)
