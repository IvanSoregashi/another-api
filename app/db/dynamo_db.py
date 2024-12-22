import os
from functools import lru_cache, reduce
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, And


class DynamoDBError(Exception):
    pass


class AWSConfig:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = region_name or os.getenv("REGION_NAME")

        if not self.aws_access_key_id or not self.aws_secret_access_key or not self.region_name:
            raise ValueError("AWS credentials and region must be provided.")

    def to_dict(self):
        return {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "region_name": self.region_name
        }


@lru_cache
def get_dynamodb_resource(config: AWSConfig = None):
    config = config or AWSConfig()
    return boto3.resource(service_name="dynamodb", **config.to_dict())


class DynamoDBTable:
    def __init__(self, table_name: str, dynamodb=None):
        """
        Initialize a DynamoDB table interface.
        """
        dynamodb = dynamodb or get_dynamodb_resource()
        self.table = dynamodb.Table(table_name)

    def pull_item(self, key: dict) -> dict:
        """
        Retrieve an item by its primary key.
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item", {})
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    def query_items(self, key: str, value: str) -> dict:
        """
        Query items by primary key.
        """
        try:
            response = self.table.query(KeyConditionExpression=Key(key).eq(value))
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    def put_item(self, item: dict) -> dict:
        """
        Insert or overwrite an item.
        """
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    def delete_item(self, key: dict) -> None:
        """
        Delete an item by its primary key.
        """
        try:
            self.table.delete_item(Key=key)
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

    def scan_table(self, filters: dict) -> list:
        """
        Scan the table and return all items.
        """
        # Should I add Limit???
        try:
            filters = {"FilterExpression": reduce(And, ([Key(k).eq(v) for k, v in filters.items()]))} if filters else {}
            response = self.table.scan(**filters)
            return response.get("Items", [])
        except ClientError as e:
            error_message = e.response["Error"]["Message"]
            raise DynamoDBError(f"Error putting item: {error_message}")

