from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.db.async_dynamo_db import AWS
from app.routers.transactions import transactions_router

load_dotenv(".env")

# TODO will need to double check at some point precise behaviour of creating tables / connections to db
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Modify resource management. Right now, table is called on ddb instance every request
    aws = AWS()
    yield
    await aws.cleanup()
"""

app = FastAPI()  # (lifespan=lifespan)
app.include_router(transactions_router)

if __name__ == "__main__":
    uvicorn.run(app, reload=True, port=8080, host='0.0.0.0')
