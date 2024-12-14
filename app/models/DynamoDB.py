import os

import boto3

from app.models.transaction import Transaction


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

    def put_transaction(self, transaction: Transaction):
        table = self.__dynamo_db_resource.Table("Transactions")
        table.put_item(Item=transaction.model_dump())

    def get_table(self, table_name: str):
        return self.__dynamo_db_resource.Table(table_name)
