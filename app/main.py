from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException

from app.db.async_dynamo_db import DynamoDBTable, DynamoDBError, AWS
from app.use_cases.transaction import put_transaction, get_transaction
from app.models.transaction import Transaction

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


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: Transaction, repo=Depends(get_repo)):
    try:
        item = await put_transaction(repo, transaction)
        return item
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transactions/{date}")
async def get_transactions(date: str, repo=Depends(get_repo)):
    try:
        items = get_transaction(repo, date)
        return items
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')
