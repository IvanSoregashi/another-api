from typing import Annotated
from fastapi import Depends

from app.services.transactions import TransactionService

# AWS Imports
from app.db.async_dynamo_db import AWS, DBError
from app.async_repository.async_dynamo_db import DynamoDBRepository

# Async Alchemy
from app.schemas.transactions import TransactionORM
from app.db.async_sqlalchemy import DatabaseSessionManager, DBError
from app.async_repository.sqlalchemy_orm import SQLAlchemyORMRepository
from app.async_repository.sqlalchemy_core import SQLAlchemyCoreRepository

from dotenv import load_dotenv
load_dotenv("../.env")

transaction_service: TransactionService = None
aws: AWS = None


async def initialize_transaction_service(database: str):
    load_dotenv(".env")
    global transaction_service
    match database:
        case "dynamodb":
            global aws
            aws = AWS()
            transaction_repository = await DynamoDBRepository.initialize(aws, "Transactions")
        case "sql-orm":
            session_manager = DatabaseSessionManager("sqlite+aiosqlite:///data.db")
            transaction_repository = SQLAlchemyORMRepository(TransactionORM, session_manager)
        case "sql-core":
            session_manager = DatabaseSessionManager("sqlite+aiosqlite:///data.db")
            transaction_repository = SQLAlchemyCoreRepository("transactions", session_manager)

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
