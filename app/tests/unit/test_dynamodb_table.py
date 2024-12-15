from unittest import TestCase
from unittest.mock import Mock

from app.db.DynamoDB import DynamoDB


class TestDynamoDB(TestCase):
    def test_put_empty_transaction(self):
        pass