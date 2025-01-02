from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_transaction_service
from app.models.transactions import TransactionQuery, Transaction

client = TestClient(app)


@pytest.fixture
def test_service():
    test_service = AsyncMock()
    app.dependency_overrides[get_transaction_service] = lambda: test_service
    return test_service


def test_scan_all_transactions(test_service):
    test_service.scan.return_value = [{
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

    model = TransactionQuery.model_validate({})

    test_service.scan.assert_awaited_once_with(model)
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


def test_scan_all_transactions_empty_response(test_service):
    test_service.scan.return_value = []

    response = client.get("/transactions", params={})

    model = TransactionQuery.model_validate({})

    test_service.scan.assert_awaited_once_with(model)
    assert response.status_code == 200
    assert response.json() == []


def test_scan_all_transactions_with_type_filter(test_service):
    test_service.scan.return_value = []

    response = client.get("/transactions", params={"type": "Transfer"})

    model = TransactionQuery.model_validate({"type": "Transfer"})

    test_service.scan.assert_awaited_once_with(model)
    assert response.status_code == 200
    assert response.json() == []


def test_scan_all_transactions_with_wrong_filter(test_service):
    test_service.scan.return_value = []

    response = client.get("/transactions", params={"sdf": "Transfer"})

    model = TransactionQuery.model_validate({})

    test_service.scan.assert_awaited_once_with(model)
    assert response.status_code == 200
    assert response.json() == []


def test_query_monthly_transactions_empty_response(test_service):
    test_service.query.return_value = []

    response = client.get("/transactions/1900-01")

    test_service.query.assert_awaited_once_with("1900-01")
    assert response.status_code == 200
    assert response.json() == []


def test_query_monthly_transactions_double(test_service):
    test_service.query.return_value = [
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

    test_service.query.assert_awaited_once_with("1900-01")
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


def test_get_transaction_found(test_service):
    test_service.get.return_value = {
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

    test_service.get.assert_awaited_once_with("1900-01", "f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

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


def test_get_transaction_not_found(test_service):
    test_service.get.return_value = {}

    response = client.get("/transactions/1900-01/f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    test_service.get.assert_awaited_once_with("1900-01", "f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_correct_transaction(test_service):
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

    test_service.put.return_value = data

    response = client.post("/transactions", json=data)

    model = Transaction.model_validate(data)

    test_service.put.assert_awaited_once_with(model)

    assert response.status_code == 201
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


def test_create_incorrect_transaction(test_service):
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

    test_service.put.return_value = data

    response = client.post("/transactions", json=data)

    test_service.put.assert_not_awaited()

    assert response.status_code == 422
#    assert response.json() == {}


def test_delete_transaction(test_service):
    test_service.delete.return_value = None

    response = client.delete("/transactions/1900-01/f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    test_service.delete.assert_awaited_once_with("1900-01", "f1bf8fed-8cb5-4403-a3a1-7b2df262182b")

    assert response.status_code == 204
    assert response.content == b''

