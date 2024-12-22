from unittest import TestCase
from unittest.mock import patch, Mock, call

from boto3.dynamodb.conditions import Key

from app.db.dynamo_db import DynamoDBTable


class TestDynamoDBTable(TestCase):
    def setUp(self):
        self.dynamodb = Mock()
        self.mock_table = self.dynamodb.Table.return_value = Mock()
        self.TABLE = DynamoDBTable("Test", self.dynamodb)

    def test_table_initialization_with_db_arg(self):
        self.dynamodb.Table.assert_called_with("Test")
        self.dynamodb.Table.assert_called_once()
        self.assertEqual(self.TABLE.table, self.mock_table)

    @patch("app.db.dynamo_db.get_dynamodb_resource")
    def test_table_initialization_without_db_arg(self, mock_get_resource):
        mock_get_resource.return_value = self.dynamodb

        table = DynamoDBTable("Test2")

        self.dynamodb.Table.assert_has_calls([call('Test'), call('Test2')])
        self.assertEqual(table.table, self.dynamodb.Table.return_value)

    def test_get_item(self):
        self.mock_table.get_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}

        response = self.TABLE.pull_item({"month": "TEST"})

        self.mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST", "transaction_id": 3})

    def test_get_item_empty_response(self):
        self.mock_table.get_item.return_value = {"Item": {}}

        response = self.TABLE.pull_item({"month": "TEST"})

        self.mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {})

    def test_query_item(self):
        self.mock_table.query.return_value = {"Items": [{"month": "TEST", "transaction_id": 3}]}

        response = self.TABLE.query_items("month", "TEST")

        self.mock_table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        self.assertEqual(response, [{"month": "TEST", "transaction_id": 3}])

    def test_query_item_empty_response(self):
        self.mock_table.query.return_value = {"Items": []}

        response = self.TABLE.query_items("month", "TEST")

        self.mock_table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        self.assertEqual(response, [])

    def test_put_item(self):
        response = self.TABLE.put_item({"month": "TEST"})

        self.mock_table.put_item.assert_called_once_with(Item={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST"})

    def test_delete_item(self):
        self.TABLE.delete_item({"month": "TEST"})
        self.mock_table.delete_item.assert_called_once_with(Key={"month": "TEST"})

    def test_scan_empty_table(self):
        self.mock_table.scan.return_value = {"Items": []}

        response = self.TABLE.scan_table({})

        self.mock_table.scan.assert_called_once_with()
        self.assertEqual(response, [])

    def test_scan_full_table(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = self.TABLE.scan_table({})

        self.mock_table.scan.assert_called_once_with()
        self.assertEqual(response, [1, 2])

    def test_scan_table_with_one_filter(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = self.TABLE.scan_table({"amount": 95})

        self.mock_table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95))
        self.assertEqual(response, [1, 2])

    def test_scan_table_with_two_filters(self):
        self.mock_table.scan.return_value = {"Items": [1, 2]}

        response = self.TABLE.scan_table({"amount": 95, "Type": "Expense"})

        self.mock_table.scan.assert_called_once_with(FilterExpression=Key("amount").eq(95) & Key("Type").eq("Expense"))
        self.assertEqual(response, [1, 2])
