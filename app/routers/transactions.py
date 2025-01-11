from typing import Annotated
from fastapi import APIRouter, HTTPException, Query

from app.dependencies import TransactionServiceDependancy, DBError
from app.core.models.transactions import Transaction, TransactionQuery

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions"])


@transactions_router.get(
    "",
    response_model=list[Transaction],
    summary="Get all transactions, optionally filtered"
)
async def scan_all_transactions(
        filter_query: Annotated[TransactionQuery, Query()],
        service: TransactionServiceDependancy
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
        service: TransactionServiceDependancy,
        month: str,
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
        service: TransactionServiceDependancy,
        month: str,
        transaction_id: str,
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
        service: TransactionServiceDependancy,
        transaction: Transaction,
):
    try:
        item = await service.post(transaction)
        return item
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@transactions_router.put(
    "",
    tags=["Transactions"],
    response_model=Transaction,
    status_code=201,
    summary="Report transaction"
)
async def update_transaction(
        service: TransactionServiceDependancy,
        transaction: Transaction,
):
    try:
        item = await service.put(transaction)
        if not item:
            raise HTTPException(status_code=500, detail="Could not complete update operation")
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
        service: TransactionServiceDependancy,
        month: str,
        transaction_id: str,
):
    try:
        item = await service.delete(month, transaction_id)
        return item
    except DBError as e:
        raise HTTPException(status_code=500, detail=str(e))
