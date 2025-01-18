import os
import contextlib
from typing import Self
from app.core.config import settings


import aioboto3
# from botocore.exceptions import ClientError


class DBError(Exception):
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
        self.aws_access_key_id = aws_access_key_id or settings.aws.aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key or settings.aws.aws_secret_access_key
        self.region_name = region_name or settings.aws.region_name

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
            return self.resources[resource_name]
        session = aioboto3.Session(**self.instance.to_dict())
        resource = await self.stack.enter_async_context(session.resource(resource_name))
        self.resources[resource_name] = resource
        return resource

    async def get_dynamo_db_table(self, table_name: str) -> Self:
        dynamodb = await self.get_async_resource("dynamodb")
        table = await dynamodb.Table(table_name)
        return table

    async def cleanup(self):
        self.resources = dict()
        await self.stack.aclose()

