import pytest
from unittest.mock import AsyncMock, Mock

from boto3.dynamodb.conditions import Key
from app.repository.async_dynamo_db import DynamoDBRepository


@pytest.fixture(scope="function")
def mock_repo():
    repo = DynamoDBRepository(AsyncMock())
    return repo


class TestDynamoDBTable:
    def test_table_initialization_with_table(self):
        mock_table = Mock()
        repo = DynamoDBRepository(mock_table)
        assert repo.table is mock_table

    async def test_table_initialization_with_named_method(self):
        aws = AsyncMock()
        table = aws.get_dynamo_db_table.return_value = AsyncMock()

        repo = await DynamoDBRepository.initialize(aws, "Test")

        aws.get_dynamo_db_table.assert_awaited_once_with("Test")
        assert repo.table is table

    async def test_get_item(self, mock_repo):
        mock_repo.table.get_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}

        response = await mock_repo.get_item({"month": "TEST"})

        mock_repo.table.get_item.assert_awaited_once_with(Key={"month": "TEST"})
        assert response == {"month": "TEST", "transaction_id": 3}

    async def test_get_item_empty_response(self, mock_repo):
        mock_repo.table.get_item.return_value = {"Item": {}}

        response = await mock_repo.get_item({"month": "TEST"})

        mock_repo.table.get_item.assert_awaited_once_with(Key={"month": "TEST"})
        assert response == {}

    async def test_query_item(self, mock_repo):
        mock_repo.table.query.return_value = {"Items": [{"month": "TEST", "transaction_id": 3}]}

        response = await mock_repo.query_items("month", "TEST")

        mock_repo.table.query.assert_awaited_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        assert response == [{"month": "TEST", "transaction_id": 3}]

    async def test_query_item_empty_response(self, mock_repo):
        mock_repo.table.query.return_value = {"Items": []}

        response = await mock_repo.query_items("month", "TEST")

        mock_repo.table.query.assert_awaited_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        assert response == []

    async def test_post_item(self, mock_repo):
        response = await mock_repo.post_item({"month": "TEST"})

        mock_repo.table.put_item.assert_awaited_once_with(Item={"month": "TEST"})
        assert response == {"month": "TEST"}

    async def test_put_item(self, mock_repo):
        response = await mock_repo.put_item({"month": "TEST"})

        mock_repo.table.put_item.assert_awaited_once_with(Item={"month": "TEST"})
        assert response == {"month": "TEST"}

    async def test_delete_item(self, mock_repo):
        await mock_repo.delete_item({"month": "TEST"})
        mock_repo.table.delete_item.assert_awaited_once_with(Key={"month": "TEST"})

    async def test_scan_empty_table(self, mock_repo):
        mock_repo.table.scan.return_value = {"Items": []}

        response = await mock_repo.scan_table({})

        mock_repo.table.scan.assert_awaited_once_with()
        assert response == []

    async def test_scan_full_table(self, mock_repo):
        mock_repo.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_repo.scan_table({})

        mock_repo.table.scan.assert_awaited_once_with()
        assert response == [1, 2]

    async def test_scan_table_with_one_filter(self, mock_repo):
        mock_repo.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_repo.scan_table({"amount": 95})

        mock_repo.table.scan.assert_awaited_once_with(FilterExpression=Key("amount").eq(95))
        assert response == [1, 2]

    async def test_scan_table_with_two_filters(self, mock_repo):
        mock_repo.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_repo.scan_table({"amount": 95, "Type": "Expense"})

        mock_repo.table.scan.assert_awaited_once_with(FilterExpression=Key("amount").eq(95) & Key("Type").eq("Expense"))
        assert response == [1, 2]
