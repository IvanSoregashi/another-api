from typing import Annotated
from fastapi import Depends

from app.core.config import settings
from app.services.transactions import TransactionService

# AWS Imports
from app.async_database.dynamo_db import AWS, DBError
from app.async_repository.dynamo_db import DynamoDBRepository

# Async Alchemy
from app.schemas.transactions import TransactionORM, Base
from app.async_database.sqlalchemy import DatabaseSessionManager, DBError
from app.async_repository.sqlalchemy_orm import SQLAlchemyORMRepository
from app.async_repository.sqlalchemy_core import SQLAlchemyCoreRepository


transaction_service: TransactionService = None
aws: AWS = None


async def dynamodb_repository():
    global aws
    aws = AWS()
    return await DynamoDBRepository.initialize(aws, "Transactions")


async def sqlorm_repository():
    session_manager = DatabaseSessionManager(settings.db.url)
    await session_manager.run_sync(Base.metadata.drop_all)
    await session_manager.run_sync(Base.metadata.create_all)
    return SQLAlchemyORMRepository(TransactionORM, session_manager)


def sqlcore_repository():
    session_manager = DatabaseSessionManager("sqlite+aiosqlite:///data.db")
    return SQLAlchemyCoreRepository("transactions", session_manager)


async def test_repository():
    session_manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    await session_manager.run_sync(Base.metadata.drop_all)
    await session_manager.run_sync(Base.metadata.create_all)
    return SQLAlchemyORMRepository(TransactionORM, session_manager)


async def test_dynamodb_repository():
    global aws
    aws = AWS()
    """ddb = await aws.get_async_resource("dynamodb")
    try:
        Table = await ddb.Table('Test_Transactions')
        await Table.delete()
        await Table.wait_until_not_exists()
    except Exception as e:
        print(e)
    await ddb.create_table(
        TableName='Test_Transactions',
        KeySchema=[
            {'AttributeName': 'month', 'KeyType': 'HASH'},
            {'AttributeName': 'transaction_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'month', 'AttributeType': 'S'},
            {'AttributeName': 'transaction_id', 'AttributeType': 'S'},
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    try:
        Table = await ddb.Table('Test_Transactions')
        await Table.wait_until_exists()
    except Exception as e:
        print(e)"""
    return await DynamoDBRepository.initialize(aws, "Test_Transactions")


async def initialize_transaction_service(mode: str = settings.mode):
    global transaction_service
    match mode:
        case "dynamodb": transaction_repository = await dynamodb_repository()
        case "sql-orm": transaction_repository = await sqlorm_repository()
        case "sql-core": transaction_repository = sqlcore_repository()
        case "test": transaction_repository = await test_repository()
        case "test_dynamodb": transaction_repository = await test_dynamodb_repository()

    transaction_service = TransactionService(transaction_repository)


async def cleanup_transaction_service():
    global aws
    print("Enter cleanup")
    if aws:
        print("Engage cleanup")
        await aws.cleanup()


def get_transaction_service() -> TransactionService:
    if transaction_service is None:
        raise RuntimeError("Database was not initialized.")
    return transaction_service


TransactionServiceDependancy = Annotated[TransactionService, Depends(get_transaction_service)]
