from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from app.db.DynamoDB import DynamoDBTable


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
