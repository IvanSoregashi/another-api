import os

import boto3
from botocore.exceptions import ClientError


class DynamoDB:
    instance = None

    def __new__(cls):
        if not isinstance(cls.instance, cls):
            inst = super().__new__(cls)

            inst.__dynamo_db_resource = boto3.resource(
                service_name="dynamodb",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("REGION_NAME")
            )

            cls.instance = inst
        return cls.instance

    def get_table(self, table_name: str):
        return self.__dynamo_db_resource.Table(table_name)


class DynamoDBTable:
    def __init__(self, table_name: str, dynamo_db: DynamoDB = DynamoDB()):
        """
        Initialize a DynamoDB table interface.
        """
        self.table = dynamo_db.get_table(table_name)

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
