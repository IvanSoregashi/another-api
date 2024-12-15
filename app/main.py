import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException

from app.db.DynamoDB import DynamoDBTable, DynamoDBError
from app.use_cases.transaction import put_transaction
from app.models.transaction import Transaction

load_dotenv(".env")

app = FastAPI()
async def get_repo(): return DynamoDBTable("Transactions")


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/transaction", response_model=Transaction)
async def create_transaction(transaction: Transaction, repo=Depends(get_repo)):
    try:
        item = put_transaction(repo, transaction)
        return item
    except DynamoDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')
