import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.models.transactions import TransactionQuery, Transaction

client = TestClient(app)



