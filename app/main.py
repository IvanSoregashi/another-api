import uvicorn
from fastapi import FastAPI

from app.db.DynamoDB import DynamoDB
from models.transaction import Transaction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/transaction", response_model=Transaction)
async def create_book(transaction: Transaction):
    DynamoDB().put_transaction(transaction)
    print(transaction)
    return transaction

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')
