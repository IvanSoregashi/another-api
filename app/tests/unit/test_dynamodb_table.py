from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from boto3.dynamodb.conditions import Key

from app.db.DynamoDB import DynamoDBTable#, Key


class TestDynamoDBTable(TestCase):
    def setUp(self):
        self.dynamodb = Mock()
        self.mock_table = self.dynamodb.Table.return_value = Mock()
        self.TABLE = DynamoDBTable("Test", self.dynamodb)

    def test_table_initialization_with_db_arg(self):
        table = DynamoDBTable("Test", self.dynamodb)

        self.dynamodb.Table.assert_called_with("Test")
        self.dynamodb.Table.assert_called_once()
        self.assertEqual(table.table, self.dynamodb.Table.return_value)

    @patch("app.db.DynamoDB.get_dynamodb_resource")
    def test_table_initialization_without_db_arg(self, mock_get_resource):
        mock_get_resource.return_value = self.dynamodb

        table = DynamoDBTable("Test")

        self.dynamodb.Table.assert_called_with("Test")
        self.dynamodb.Table.assert_called_once()
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
        self.mock_table.delete_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}

        response = self.TABLE.delete_item({"month": "TEST"})

        self.mock_table.delete_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST", "transaction_id": 3})