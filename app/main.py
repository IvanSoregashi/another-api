from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from app.dependencies import initialize_transaction_service, cleanup_transaction_service

from app.routers.transactions import router as transactions_router
from app.routers.auths import router as auth_router


# TODO will need to double check at some point precise behaviour of creating tables / connections to async_database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Modify resource management. Right now, table is called on ddb instance every request
    await initialize_transaction_service("test_dynamodb")
    yield
    await cleanup_transaction_service()


app = FastAPI(lifespan=lifespan)

app.include_router(transactions_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8080, host='0.0.0.0')
