from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from boto3.dynamodb.conditions import Key

from app.db.DynamoDB import DynamoDBTable#, Key


class TestDynamoDBTable(TestCase):

    def test_table_initialization_with_db_arg(self):
        dynamodb = Mock()
        dynamodb.Table.return_value = "test_table"

        table = DynamoDBTable("Test", dynamodb)

        dynamodb.Table.assert_called_with("Test")
        dynamodb.Table.assert_called_once()
        self.assertEqual(table.table, "test_table")

    @patch("app.db.DynamoDB.get_dynamodb_resource")
    def test_table_initialization_without_db_arg(self, mock_get_resource):
        dynamodb = Mock()
        dynamodb.Table.return_value = "test_table"
        mock_get_resource.return_value = dynamodb

        table = DynamoDBTable("Test")

        dynamodb.Table.assert_called_with("Test")
        dynamodb.Table.assert_called_once()
        self.assertEqual(table.table, "test_table")

    def test_get_item(self):
        dynamodb = Mock()
        mock_table = Mock()
        mock_table.get_item.return_value = {"Item": {"month": "TEST", "transaction_id": 3}}
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.get_item({"month": "TEST"})

        mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST", "transaction_id": 3})

    def test_get_item_empty_response(self):
        dynamodb = Mock()
        mock_table = Mock()
        mock_table.get_item.return_value = {"Item": {}}
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.get_item({"month": "TEST"})

        mock_table.get_item.assert_called_once_with(Key={"month": "TEST"})
        self.assertEqual(response, {})

    def test_query_item(self):
        dynamodb = Mock()
        mock_table = Mock()
        mock_table.query.return_value = {"Items": [{"month": "TEST", "transaction_id": 3}]}
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.query_items("month", "TEST")

        mock_table.query.assert_called_once_with(KeyConditionExpression=Key("month").eq("TEST"))
        self.assertEqual(response, [{"month": "TEST", "transaction_id": 3}])

    def test_put_item(self):
        dynamodb = Mock()
        mock_table = Mock()
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.put_item({"month": "TEST"})

        mock_table.put_item.assert_called_once_with(Item={"month": "TEST"})
        self.assertEqual(response, {"month": "TEST"})
