from unittest.mock import AsyncMock

import pytest

from app.models.transaction import Transaction
from app.use_cases.transaction import query_transactions, put_transaction, get_transaction, delete_transaction, scan_transactions


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
    repo.scan_table.return_value = [{"test": "test value", "amount": 100}]

    result = await scan_transactions(repo, {"amount": 100})

    repo.scan_table.assert_called_once_with({"amount": 100})
    assert result == [{"test": "test value", "amount": 100}]
