from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Query, HTTPException

from app.db.async_dynamo_db import DynamoDBTable, DynamoDBError, AWS
from app.use_cases.transaction import put_transaction, get_transaction, query_transactions, delete_transaction, \
    scan_transactions
from app.models.transaction import Transaction, TransactionQuery

load_dotenv(".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Modify resource management. Right now, table is called on ddb instance every request
    aws = AWS()
    yield
    await aws.cleanup()


app = FastAPI(lifespan=lifespan)


async def get_repo() -> DynamoDBTable:
    # TODO: Do something about this. Just not the ugly dependency injection chain.
    aws = AWS()
    return await DynamoDBTable.named(aws, "Transactions")


@app.get(
    "/transactions",
    tags=["Transactions"],
    response_model=list[Transaction],
    summary="Get all transactions, optionally filtered"
)
async def scan_all_transactions(
        filter_query: Annotated[TransactionQuery, Query()] = None,
        repo=Depends(get_repo)
) -> list[Transaction]:
    try:
        items = await scan_transactions(repo, filter_query)
        return items
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/transactions/{month}",
    tags=["Transactions"],
    response_model=list[Transaction],
    summary="Get all transactions for the month"
)
async def query_monthly_transactions(
        month: str,
        repo=Depends(get_repo)
) -> list[Transaction]:
    try:
        items = await query_transactions(repo, month)
        return items
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/transactions/{month}/{transaction_id}",
    tags=["Transactions"],
    response_model=Transaction,
    summary="Get a single transaction"
)
async def get_single_transaction(month: str, transaction_id: str, repo=Depends(get_repo)):
    try:
        item = await get_transaction(repo, month, transaction_id)
        if not item: raise HTTPException(status_code=404, detail="Item not found")
        return item
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/transactions",
    tags=["Transactions"],
    response_model=Transaction,
    summary="Report transaction"
)
async def create_transaction(transaction: Transaction, repo=Depends(get_repo)):
    try:
        item = await put_transaction(repo, transaction)
        return item
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(
    "/transactions/{month}/{transaction_id}",
    tags=["Transactions"],
    summary="Delete a single transaction",
    status_code=204
)
async def delete_single_transaction(month: str, transaction_id: str, repo=Depends(get_repo)):
    try:
        item = await delete_transaction(repo, month, transaction_id)
        return item
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, reload=True, port=8080, host='0.0.0.0')
