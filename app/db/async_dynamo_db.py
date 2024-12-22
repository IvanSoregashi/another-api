import os
import contextlib
import asyncio
from functools import reduce
from typing import Self


import aioboto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, And


class DynamoDBError(Exception):
    pass


class AWS:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance
        inst = super().__new__(cls)
        inst.__init__(*args, **kwargs)
        cls.instance = inst
        return inst

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        if self.instance: return
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = region_name or os.getenv("REGION_NAME")

        if not self.aws_access_key_id or not self.aws_secret_access_key or not self.region_name:
            raise ValueError("AWS credentials and region must be provided.")

        self.resources = dict()
        self.stack = contextlib.AsyncExitStack()

    def to_dict(self):
        return {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "region_name": self.region_name
        }

    async def get_async_resource(self, resource_name):
        if self.resources.get(resource_name):
            return self.resources.get(resource_name)
        session = aioboto3.Session(**self.instance.to_dict())
        #dynamodb = await session.resource(service_name=resource_name).__aenter__()
        resource = await self.stack.enter_async_context(session.resource(resource_name))
        self.resources[resource_name] = resource
        return resource

    async def cleanup(self):
        self.resources = dict()
        await self.stack.aclose()


class DynamoDBTable:
    def __init__(self, table):
        """
        Initialize a DynamoDB table interface.
        """
        self.table = table

    @classmethod
    async def named(cls, table_name: str) -> Self:
        dynamodb = await AWS().get_async_resource("dynamodb")
        table = await dynamodb.Table(table_name)
        return cls(table)

    async def pull_item(self, key: dict) -> dict:
        """
        Retrieve an item by its primary key.
        """
        try:
            response = await self.table.get_item(Key=key)
            return response.get("Item", {})
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    async def query_items(self, key: str, value: str) -> dict:
        """
        Query items by primary key.
        """
        try:
            response = await self.table.query(KeyConditionExpression=Key(key).eq(value))
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    async def put_item(self, item: dict) -> dict:
        """
        Insert or overwrite an item.
        """
        try:
            await self.table.put_item(Item=item)
            return item
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    async def delete_item(self, key: dict) -> None:
        """
        Delete an item by its primary key.
        """
        try:
            await self.table.delete_item(Key=key)
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    async def scan_table(self, filters: dict) -> list:
        """
        Scan the table and return all items.
        """
        # Should I add Limit???
        try:
            filters = {"FilterExpression": reduce(And, ([Key(k).eq(v) for k, v in filters.items()]))} if filters else {}
            response = await self.table.scan(**filters)
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")


async def main():
    stack = contextlib.AsyncExitStack()
    session = aioboto3.Session(**AWSConfig().to_dict())

    sqs = await stack.enter_async_context(session.resource(service_name="dynamodb"))
    #... pass sqs object around, into other async functions etc..

    # before you exit, clean up
    await stack.aclose()


if __name__ == '__main__':
    aws1 = AWS(aws_access_key_id="test_id", aws_secret_access_key="test_key", region_name="test_region")
    print(f"AWS 1 ID: {id(aws1)}")

    aws2 = AWS()  # Notice we don't need to provide credentials again
    print(f"AWS 2 ID: {id(aws2)}")

    print(aws1 is aws2)  # Output: True
