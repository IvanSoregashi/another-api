# These are failed cases. Need to understand why.
# from unittest.mock import AsyncMock, patch
# from fastapi.testclient import TestClient
# from app.main import app, get_repo
# from app.use_cases import transaction


"""
client = TestClient(app)
test_repo = AsyncMock()
app.dependency_overrides[get_repo] = lambda: test_repo
"""

"""
# TODO: Understand why this doesn't work.
@patch("app.use_cases.transaction.scan_transactions")
def test_all_transactions(mock_scan_transactions):
    mock_scan_transactions.return_value = []

    response = client.get("/transactions", params={})

    mock_scan_transactions.assert_awaited_once_with(test_repo, {})
    assert response.json() == []
"""

"""
# TODO: Understand why this doesn't work either.
def test_all_transactions(monkeypatch):
    async def mock_scan(repo, filters):
        return [{
            "month": "2024-12",
            "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
            "datetime": "2024-12-25T05:06:04.288542+00:00",
            "type": "Transfer",
            "account": "Kaspi",
            "currency": "KZT",
            "amount": "95",
            "category": "Groceries",
            "point": "Small",
            "item": None,
            "comment": None
        }]

    monkeypatch.setattr(transaction, "scan_transactions", mock_scan)

    response = client.get("/transactions", params={})

    assert response.status_code == 200
    assert response.json() == [{
        "month": "2024-12",
        "transaction_id": "f1bf8fed-8cb5-4403-a3a1-7b2df262182b",
        "datetime": "2024-12-25T05:06:04.288542+00:00",
        "type": "Transfer",
        "account": "Kaspi",
        "currency": "KZT",
        "amount": "95",
        "category": "Groceries",
        "point": "Small",
        "item": None,
        "comment": None
    }]
"""