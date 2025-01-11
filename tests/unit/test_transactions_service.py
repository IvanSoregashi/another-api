from unittest.mock import AsyncMock

import pytest

from app.core.models import Transaction, TransactionQuery
from app.services.transactions import TransactionService


@pytest.fixture
async def repo():
    return AsyncMock()


@pytest.fixture
async def service(repo):
    return TransactionService(repo)


def test_initialization(repo):
    service = TransactionService(repo)
    assert service.transactions_repo is repo


async def test_scan_transaction(service, repo):
    # TODO This one will be modified and will need a lot more testing.
    # TODO Opportunity for TDD?
    repo.scan_table.return_value = [{"test": "test value", "amount": 100, "type": "Transfer"}]

    model = TransactionQuery.model_validate({"type": "Transfer"})

    result = await service.scan(model)

    repo.scan_table.assert_awaited_once_with({"type": "Transfer"})
    assert result == [{"test": "test value", "amount": 100, "type": "Transfer"}]


async def test_query_transactions(service, repo):
    repo.query_items.return_value = {"test": "test value"}

    result = await service.query("YYYY-MM")

    repo.query_items.assert_awaited_once_with("month", "YYYY-MM")
    assert result == {"test": "test value"}


async def test_post_transaction(service, repo):
    repo.post_item.return_value = {"test": "test value"}

    model = Transaction.model_validate({"type": "test", "account": "Kaspi", "amount": 95, "point": "Small"})
    result = await service.post(model)

    repo.post_item.assert_awaited_once_with(model.model_dump())
    assert result == {"test": "test value"}


async def test_put_transaction(service, repo):
    repo.put_item.return_value = {"test": "test value"}

    model = Transaction.model_validate({"type": "test", "account": "Kaspi", "amount": 95, "point": "Small"})
    result = await service.put(model)

    repo.put_item.assert_awaited_once_with(model.model_dump())
    assert result == {"test": "test value"}


async def test_get_transaction(service, repo):
    repo.get_item.return_value = {"test": "test value"}

    result = await service.get("test", "test uuid")

    repo.get_item.assert_awaited_once_with({"month": "test", "transaction_id": "test uuid"})
    assert result == {"test": "test value"}


async def test_delete_transaction(service, repo):
    repo.delete_item.return_value = {"test": "test value"}

    result = await service.delete("test", "test uuid")

    repo.delete_item.assert_awaited_once_with({"month": "test", "transaction_id": "test uuid"})
    assert result == {"test": "test value"}
