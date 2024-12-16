from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

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
        mock_table.get_item.return_value = {"Item": {"datetime": "TEST", "lol": 3}}
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.get_item({"datetime": "TEST"})

        mock_table.get_item.assert_called_once_with(Key={"datetime": "TEST"})
        self.assertEqual(response, {"datetime": "TEST", "lol": 3})

    def test_put_item(self):
        dynamodb = Mock()
        mock_table = Mock()
        dynamodb.Table.return_value = mock_table

        table = DynamoDBTable("Test", dynamodb)

        response = table.put_item({"datetime": "TEST"})

        mock_table.put_item.assert_called_once_with(Item={"datetime": "TEST"})
        self.assertEqual(response, {"datetime": "TEST"})
