from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from app.db.aiosqlite_sqlalchemy import SQLAlchemyORMRepository, DBError, DatabaseSessionManager, \
    SQLAlchemyCoreRepository
from app.schemas.transactions import TransactionORM

from app.models.transactions import Transaction, TransactionQuery
from app.use_cases.transactions import TransactionService

transactions_router = APIRouter(prefix="/transactions")

session_manager = DatabaseSessionManager("sqlite+aiosqlite:///data.db")
#sqlite_repository = SQLAlchemyORMRepository(TransactionORM, session_manager)
sqlite_repository = SQLAlchemyCoreRepository("transactions", session_manager)
transactions_service = TransactionService(sqlite_repository)


async def get_service() -> TransactionService:
    yield transactions_service


@transactions_router.get(
    "",
    tags=["Transactions"],
    response_model=list[Transaction],
    summary="Get all transactions, optionally filtered"
)
async def scan_all_transactions(
        filter_query: Annotated[TransactionQuery, Query()] = None,
        service: TransactionService = Depends(get_service)
) -> list[Transaction]:
    try:
        items = await service.scan(filter_query)
        return items
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactions_router.get(
    "/{month}",
    tags=["Transactions"],
    response_model=list[Transaction],
    summary="Get all transactions for the month"
)
async def query_monthly_transactions(
        month: str,
        service: TransactionService = Depends(get_service)
) -> list[Transaction]:
    try:
        items = await service.query(month)
        return items
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactions_router.get(
    "/{month}/{transaction_id}",
    tags=["Transactions"],
    response_model=Transaction,
    summary="Get a single transaction"
)
async def get_single_transaction(
        month: str,
        transaction_id: str,
        service: TransactionService = Depends(get_service)
) -> dict:
    try:
        item = await service.get(month, transaction_id)
        if not item: raise HTTPException(status_code=404, detail="Item not found")
        return item
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactions_router.post(
    "",
    tags=["Transactions"],
    response_model=Transaction,
    status_code=201,
    summary="Report transaction"
)
async def create_transaction(
        transaction: Transaction,
        service: TransactionService = Depends(get_service)
):
    try:
        item = await service.put(transaction)
        return item
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactions_router.delete(
    "/{month}/{transaction_id}",
    tags=["Transactions"],
    summary="Delete a single transaction",
    status_code=204
)
async def delete_single_transaction(
        month: str,
        transaction_id: str,
        service: TransactionService = Depends(get_service)
):
    try:
        item = await service.delete(month, transaction_id)
        return item
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))
