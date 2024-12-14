import os

import boto3
from botocore.exceptions import ClientError


class AWSConfig:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region_name = region_name or os.getenv("REGION_NAME")

    def to_dict(self):
        return {
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
            "region_name": self.region_name
        }


class DynamoDBTable:
    def __init__(self, table_name: str, config: AWSConfig = AWSConfig()):
        """
        Initialize a DynamoDB table interface.
        """
        dynamodb = boto3.resource(service_name='dynamodb', **config.to_dict())
        self.table = dynamodb.Table(table_name)

    def get_item(self, key: dict) -> dict:
        """
        Retrieve an item by its primary key.
        """
        try:
            response = self.table.get_item(Key=key)
            return response.get("Item", {})
        except ClientError as e:
            raise Exception(f"Error getting item: {e.response['Error']['Message']}")

    def put_item(self, item: dict) -> dict:
        """
        Insert or overwrite an item.
        """
        try:
            self.table.put_item(Item=item)
            return {"message": "Item saved successfully."}
        except ClientError as e:
            raise Exception(f"Error putting item: {e.response['Error']['Message']}")

    def delete_item(self, key: dict) -> dict:
        """
        Delete an item by its primary key.
        """
        try:
            self.table.delete_item(Key=key)
            return {"message": "Item deleted successfully."}
        except ClientError as e:
            raise Exception(f"Error deleting item: {e.response['Error']['Message']}")

    def scan_table(self) -> list:
        """
        Scan the table and return all items.
        """
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except ClientError as e:
            raise Exception(f"Error scanning table: {e.response['Error']['Message']}")
