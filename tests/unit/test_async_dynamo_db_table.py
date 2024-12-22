import pytest
from unittest.mock import patch, call, AsyncMock, Mock

from boto3.dynamodb.conditions import Key
from app.db.async_dynamo_db import DynamoDBTable


@pytest.fixture(scope="function")
def mock_table():
    table = DynamoDBTable(AsyncMock())
    return table


class TestDynamoDBTable:
    def test_table_initialization_with_table(self):
        mock_table = Mock()
        table = DynamoDBTable(mock_table)
        assert table.table == mock_table

    async def test_table_initialization_with_named_method(self):
        aws = AsyncMock()
        dynamodb = aws.get_async_resource.return_value = AsyncMock()
        dynamodb.Table.return_value = "aws_table_test"

        table = await DynamoDBTable.named(aws, "Test")

        aws.get_async_resource.assert_called_once_with("dynamodb")
        dynamodb.Table.assert_called_once_with("Test")
        assert table.table == "aws_table_test"

    async def test_get_item(self, mock_table):
        mock_table.table.get_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}

        response = await mock_table.pull_item({"month": "TEST"})

        mock_table.table.get_item.assert_called_once_with(Key={"month": "TEST"})
        assert response == {"month": "TEST", "transaction_id": 3}

    async def test_get_item_empty_response(self, mock_table):
        mock_table.table.get_item.return_value = {"Item": {}}

        response = await mock_table.pull_item({"month": "TEST"})

        mock_table.table.get_item.assert_called_once_with(Key={"month": "TEST"})
        assert response == {}

    async def test_query_item(self, mock_table):
        mock_table.table.query.return_value = {"Items": [{"month": "TEST", "transaction_id": 3}]}

        response = await mock_table.query_items("month", "TEST")

        mock_table.table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        assert response == [{"month": "TEST", "transaction_id": 3}]

    async def test_query_item_empty_response(self, mock_table):
        mock_table.table.query.return_value = {"Items": []}

        response = await mock_table.query_items("month", "TEST")

        mock_table.table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        assert response == []

    async def test_put_item(self, mock_table):
        response = await mock_table.put_item({"month": "TEST"})

        mock_table.table.put_item.assert_called_once_with(Item={"month": "TEST"})
        assert response == {"month": "TEST"}

    async def test_delete_item(self, mock_table):
        await mock_table.delete_item({"month": "TEST"})
        mock_table.table.delete_item.assert_called_once_with(Key={"month": "TEST"})

    async def test_scan_empty_table(self, mock_table):
        mock_table.table.scan.return_value = {"Items": []}

        response = await mock_table.scan_table({})

        mock_table.table.scan.assert_called_once_with()
        assert response == []

    async def test_scan_full_table(self, mock_table):
        mock_table.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_table.scan_table({})

        mock_table.table.scan.assert_called_once_with()
        assert response == [1, 2]

    async def test_scan_table_with_one_filter(self, mock_table):
        mock_table.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_table.scan_table({"amount": 95})

        mock_table.table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95))
        assert response == [1, 2]

    async def test_scan_table_with_two_filters(self, mock_table):
        mock_table.table.scan.return_value = {"Items": [1, 2]}

        response = await mock_table.scan_table({"amount": 95, "Type": "Expense"})

        mock_table.table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95) & Key("Type").eq("Expense"))
        assert response == [1, 2]
