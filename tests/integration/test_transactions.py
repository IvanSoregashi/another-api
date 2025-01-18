import pytest

from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from app.dependencies import initialize_transaction_service
from app.main import app

client = TestClient(app)


@pytest.fixture()
async def test_service():
    await initialize_transaction_service(mode="test")

@pytest.mark.anyio
def test_happy_path(test_service):
    transaction = 'fd5e2abe-7a46-4da2-b449-67c59d507ffd'
    month = '2025-01'
    payload = {
        'transaction_id': transaction, 'month': month,
        'datetime': '2025-01-18T04:06:42.339096+00:00', 'type': 'Transfer', 'account': 'Kaspi',
        'currency': 'KZT',
        'amount': 95, 'category': 'Groceries', 'point': 'Small', 'item': 'jjj', 'comment': None}
    payload2 = {
        'transaction_id': transaction, 'month': month,
        'datetime': '2025-01-18T04:06:42.339096+00:00', 'type': 'Income', 'account': 'Kaspi', 'currency': 'KZT',
        'amount': 999, 'category': 'Groceries', 'point': 'Small', 'item': 'jjj', 'comment': "New Comment"}

    response = client.get("/transactions")
    assert response.status_code == 200
    #assert response.json() == []

    response = client.post("/transactions", json=payload)
    assert response.status_code == 201
    payload['amount'] = '95.0'
    assert response.json() == payload

    response = client.get("/transactions")
    assert response.status_code == 200
    #assert response.json() == [payload]

    response = client.get(f"/transactions/{month}")
    assert response.status_code == 200
    #assert response.json() == [payload]

    response = client.get(f"/transactions/{month}/{transaction}")
    assert response.status_code == 200
    assert response.json() == payload

    response = client.put("/transactions", json=payload2)
    assert response.status_code == 201
    payload2['amount'] = '999.0'
    assert response.json() == payload2

    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == [payload2]

    response = client.get(f"/transactions/{month}")
    assert response.status_code == 200
    assert response.json() == [payload2]

    response = client.get(f"/transactions/{month}/{transaction}")
    assert response.status_code == 200
    assert response.json() == payload2

    response = client.delete(f"/transactions/{month}/{transaction}")
    assert response.status_code == 204
    assert response.content == b''

    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(f"/transactions/{month}")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get(f"/transactions/{month}/{transaction}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Item not found'}


@pytest.mark.anyio
def test_post(test_service):
    transaction = 'fd5e2abe-7a46-4da2-b449-67c59d507ffd'
    month = '2025-01'
    payload = {
        'transaction_id': transaction, 'month': month,
        'datetime': '2025-01-18T04:06:42.339096+00:00', 'type': 'Transfer', 'account': 'Kaspi',
        'currency': 'KZT',
        'amount': 95, 'category': 'Groceries', 'point': 'Small', 'item': 'jjj', 'comment': None}

    response = client.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/transactions")
    assert response.status_code == 200
    #payload['amount'] = '95'
    #assert response.json() == payload


@pytest.mark.anyio
async def test_234(test_service):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.get("/transactions")
    assert response.status_code == 200
    assert response.json() == []