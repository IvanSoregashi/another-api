from functools import reduce

from boto3.dynamodb.conditions import Key, And
from botocore.exceptions import ClientError

from app.db.async_dynamo_db import DBError, AWS
from app.repository.repository import AbstractRepository


class DynamoDBRepository(AbstractRepository):
    def __init__(self, table):
        """
        Initialize a DynamoDB table interface.
        """
        self.table = table

    @classmethod
    async def initialize(cls, aws_object: AWS, table_name):
        """
        Async Initialization for the table.
        """
        table = await aws_object.get_dynamo_db_table(table_name)
        return cls(table)

    async def scan_table(self, filters: dict) -> list:
        """
        Scan the table and return all items.
        """
        # TODO add limit
        try:
            filters = {"FilterExpression": reduce(And, ([Key(k).eq(v) for k, v in filters.items()]))} if filters else {}
            response = await self.table.scan(**filters)
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")

    async def query_items(self, key, value) -> list:
        """
        Query items by primary key.
        """
        try:
            response = await self.table.query(KeyConditionExpression=Key(key).eq(value))
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")

    async def post_item(self, item: dict) -> dict:
        """
        Insert or overwrite an item.
        """
        try:
            await self.table.put_item(Item=item)
            return item
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")

    async def put_item(self, item: dict) -> dict:
        """
        Insert or overwrite an item.
        """
        try:
            await self.table.put_item(Item=item)
            return item
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")

    async def get_item(self, keys: dict) -> dict:
        """
        Retrieve an item by its primary key.
        """
        try:
            response = await self.table.get_item(Key=keys)
            return response.get("Item", {})
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")

    async def delete_item(self, keys: dict) -> None:
        """
        Delete an item by its primary key.
        """
        try:
            await self.table.delete_item(Key=keys)
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DBError(f"Error putting item: {error_message}")
