from typing import Annotated
from fastapi import Depends

from app.use_cases.transactions import TransactionService

# AWS Imports
from app.db.async_dynamo_db import AWS, DBError
from app.repository.dynamo_db import DynamoDBRepository

# Async Alchemy
from app.schemas.transactions import TransactionORM
from app.db.async_sqlalchemy import DatabaseSessionManager, DBError
from app.repository.sqlalchemy_orm import SQLAlchemyORMRepository
from app.repository.sqlalchemy_core import SQLAlchemyCoreRepository

from dotenv import load_dotenv
load_dotenv(".env")

transaction_service: TransactionService = None
aws: AWS = None


async def initialize_transaction_service():
    global transaction_service
    global aws
    # aws = AWS()
    # transaction_repository = await DynamoDBRepository.initialize(aws, "Transactions")

    session_manager = DatabaseSessionManager("sqlite+aiosqlite:///data.db")
    transaction_repository = SQLAlchemyORMRepository(TransactionORM, session_manager)
    # transaction_repository = SQLAlchemyCoreRepository("transactions", session_manager)

    transaction_service = TransactionService(transaction_repository)


async def cleanup_transaction_service():
    global aws
    if aws:
        await aws.cleanup()


def get_transaction_service() -> TransactionService:
    if transaction_service is None:
        raise RuntimeError("Database was not initialized.")
    return transaction_service


TransactionServiceDependancy = Annotated[TransactionService, Depends(get_transaction_service)]
