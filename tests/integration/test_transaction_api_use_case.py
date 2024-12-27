from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from app.main import app, get_repo

client = TestClient(app)


@pytest.fixture
def test_repo():
    test_repo = AsyncMock()
    app.dependency_overrides[get_repo] = lambda: test_repo
    return test_repo


def test_scan_all_transactions(test_repo):
    test_repo.scan_table.return_value = [{
        "month": "2024-12",
        "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "type": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": 100,
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }]

    response = client.get("/transactions", params={})

    test_repo.scan_table.assert_awaited_once_with({})
    assert response.status_code == 200
    assert response.json() == [{
        "month": "2024-12",
        "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "type": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": "100",
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }]


def test_scan_all_transactions_empty_response(test_repo):
    test_repo.scan_table.return_value = []

    response = client.get("/transactions", params={})

    test_repo.scan_table.assert_awaited_once_with({})
    assert response.status_code == 200
    assert response.json() == []


def test_scan_all_transactions_with_type_filter(test_repo):
    test_repo.scan_table.return_value = []

    response = client.get("/transactions", params={"type": "Transfer"})

    test_repo.scan_table.assert_awaited_once_with({"type": "Transfer"})
    assert response.status_code == 200
    assert response.json() == []


def test_scan_all_transactions_with_wrong_filter(test_repo):
    test_repo.scan_table.return_value = []

    response = client.get("/transactions", params={"sdf": "Transfer"})

    test_repo.scan_table.assert_awaited_once_with({})
    assert response.status_code == 200
    assert response.json() == []


def test_query_monthly_transactions_empty_response(test_repo):
    test_repo.query_items.return_value = []

    response = client.get("/transactions/1900-01")

    test_repo.query_items.assert_awaited_once_with("month", "1900-01")
    assert response.status_code == 200
    assert response.json() == []


def test_query_monthly_transactions_double(test_repo):
    test_repo.query_items.return_value = [
        {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": 100,
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }, {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": 100,
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }
    ]

    response = client.get("/transactions/1900-01")

    test_repo.query_items.assert_awaited_once_with("month", "1900-01")
    assert response.status_code == 200
    assert response.json() == [
        {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": "100",
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        },
        {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": "100",
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }
    ]

# TODO Query Filter Query Support


def test_get_transaction_found(test_repo):
    test_repo.pull_item.return_value = {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": 100,
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }

    response = client.get("/transactions/1900-01/f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    test_repo.pull_item.assert_awaited_once_with(
        {"month": "1900-01",
         "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b"}
    )

    assert response.status_code == 200
    assert response.json() == {
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": "100",
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }


def test_get_transaction_not_found(test_repo):
    test_repo.pull_item.return_value = {}

    response = client.get("/transactions/1900-01/f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    test_repo.pull_item.assert_awaited_once_with(
        {"month": "1900-01",
         "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_correct_transaction(test_repo):
    data = {
        "month": "2024-12",
        "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "type": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": 100,
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }

    test_repo.put_item.return_value = data

    response = client.post("/transactions", json=data)

    test_repo.put_item.assert_awaited_once_with(data)

    assert response.status_code == 200
    assert response.json() == {
        "month": "2024-12",
        "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "type": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": "100",
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }


def test_create_incorrect_transaction(test_repo):
    data = {
        "month": "2024-12",
        "transactddionid": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "tydpe": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": 100,
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }

    test_repo.put_item.return_value = data

    response = client.post("/transactions", json=data)

    test_repo.put_item.assert_not_awaited()

    assert response.status_code == 422
#    assert response.json() == {}


def test_delete_transaction(test_repo):
    test_repo.delete_item.return_value = None

    response = client.delete("/transactions/1900-01/f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    test_repo.delete_item.assert_awaited_once_with(
        {"month": "1900-01",
         "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b"}
    )

    assert response.status_code == 204
    assert response.content == b''

