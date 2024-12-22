import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException

from app.db.async_dynamo_db import DynamoDBTable, DynamoDBError
from app.use_cases.transaction import put_transaction, get_transaction
from app.models.transaction import Transaction

load_dotenv(".env")

app = FastAPI()


async def get_repo() -> DynamoDBTable:
    return await DynamoDBTable.named("Transactions")


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
