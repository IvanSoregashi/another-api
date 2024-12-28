from unittest.mock import AsyncMock

import pytest

from app.models.transactions import Transaction, TransactionQuery
from app.use_cases.transactions import query_transactions, put_transaction, get_transaction, delete_transaction, scan_transactions


@pytest.fixture
async def repo():
    return AsyncMock()


async def test_query_transactions(repo):
    repo.query_items.return_value = {"test": "test value"}

    result = await query_transactions(repo, "YYYY-MM")

    repo.query_items.assert_called_once_with("month", "YYYY-MM")
    assert result == {"test": "test value"}


async def test_put_transaction(repo):
    repo.put_item.return_value = {"test": "test value"}

    model = Transaction.model_validate({"type": "test", "account": "Kaspi", "amount": 95, "point": "Small"})
    result = await put_transaction(repo, model)

    repo.put_item.assert_called_once_with(model.model_dump())
    assert result == {"test": "test value"}


async def test_get_transaction(repo):
    repo.pull_item.return_value = {"test": "test value"}

    result = await get_transaction(repo, "test", "test uuid")

    repo.pull_item.assert_called_once_with({"month": "test", "transaction_id": "test uuid"})
    assert result == {"test": "test value"}


async def test_delete_transaction(repo):
    repo.delete_item.return_value = {"test": "test value"}

    result = await delete_transaction(repo, "test", "test uuid")

    repo.delete_item.assert_called_once_with({"month": "test", "transaction_id": "test uuid"})
    assert result == {"test": "test value"}


async def test_scan_transaction(repo):
    # TODO This one will be modified and will need a lot more testing.
    # TODO Opportunity for TDD?
    repo.scan_table.return_value = [{"test": "test value", "amount": 100, "type": "Transfer"}]

    model = TransactionQuery.model_validate({"type": "Transfer"})
    result = await scan_transactions(repo, model)

    repo.scan_table.assert_called_once_with({"type": "Transfer"})
    assert result == [{"test": "test value", "amount": 100, "type": "Transfer"}]
