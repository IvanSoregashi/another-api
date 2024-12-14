import os

import boto3


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
