
import pytest
from unittest.mock import patch, call, AsyncMock, Mock

from boto3.dynamodb.conditions import Key
from app.db.async_dynamo_db import DynamoDBTable

pytestmark = pytest.mark.asyncio

"""
@pytest.fixture(scope="function")
def dynamodb_table():
    dynamodb_mock = AsyncMock()
    dynamodb_mock.Table.return_value = AsyncMock()
    return dynamodb_mock"""


class TestDynamoDBTable:
    def test_table_initialization_with_table(self):
        mock_table = Mock()
        table = DynamoDBTable(mock_table)
        assert table.table == mock_table


    @patch("app.db.async_dynamo_db.get_async_dynamodb_resource")
    async def test_table_initialization_without_db_arg(self, mock_get_resource):
        mock_get_resource.return_value = self.dynamodb

        table = await DynamoDBTable.named("Test2")

        mock_get_resource.assert_awaited_once()
        self.dynamodb.Table.assert_has_calls([call('Test'), call('Test2')])
        self.assertEqual(table.table, self.dynamodb.Table.return_value)

    async def test_get_item(self):
        self.mock_table.get_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}

        response = await self.TABLE.pull_item({"month": "TEST"})

        self.mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST", "transaction_id": 3})

    async def test_get_item_empty_response(self):
        self.mock_table.get_item.return_value = {"Item": {}}

        response = await self.TABLE.pull_item({"month": "TEST"})

        self.mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {})

    async def test_query_item(self):
        self.mock_table.query.return_value = {"Items": [{"month": "TEST", "transaction_id": 3}]}

        response = await self.TABLE.query_items("month", "TEST")

        self.mock_table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        self.assertEqual(response, [{"month": "TEST", "transaction_id": 3}])

    async def test_query_item_empty_response(self):
        self.mock_table.query.return_value = {"Items": []}

        response = await self.TABLE.query_items("month", "TEST")

        self.mock_table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        self.assertEqual(response, [])

    async def test_put_item(self):
        response = await self.TABLE.put_item({"month": "TEST"})

        self.mock_table.put_item.assert_called_once_with(Item={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST"})

    async def test_delete_item(self):
        await self.TABLE.delete_item({"month": "TEST"})
        self.mock_table.delete_item.assert_called_once_with(Key={"month": "TEST"})

    async def test_scan_empty_table(self):
        self.mock_table.scan.return_value = {"Items": []}

        response = await self.TABLE.scan_table({})

        self.mock_table.scan.assert_called_once_with()
        self.assertEqual(response, [])

    async def test_scan_full_table(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = await self.TABLE.scan_table({})

        self.mock_table.scan.assert_called_once_with()
        self.assertEqual(response, [1, 2])

    async def test_scan_table_with_one_filter(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = await self.TABLE.scan_table({"amount": 95})

        self.mock_table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95))
        self.assertEqual(response, [1, 2])

    async def test_scan_table_with_two_filters(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = await self.TABLE.scan_table({"amount": 95, "Type": "Expense"})

        self.mock_table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95) & Key("Type").eq("Expense"))
        self.assertEqual(response, [1, 2])


