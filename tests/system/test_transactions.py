import asyncio

import pytest
import httpx
import uvicorn

from app.dependencies import initialize_transaction_service
from app.main import app


@pytest.fixture()
async def test_service():
    await initialize_transaction_service(mode="test_dynamodb")


@pytest.fixture()
def run_app():
    uvicorn.run("app.main:app", reload=True, port=8080, host='0.0.0.0')


async def test_1():
    url = f"http://127.0.0.1:8080/transactions"

    async with httpx.AsyncClient() as client:
        async def req():
            resp = await client.get(url)
            assert resp.status_code == 200
            assert resp.json()

        await asyncio.gather(*[req() for _ in range(10)])
