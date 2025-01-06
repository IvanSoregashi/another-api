from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from app.dependencies import initialize_transaction_service, cleanup_transaction_service
from app.routers.transactions import transactions_router


# TODO will need to double check at some point precise behaviour of creating tables / connections to db
@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: Modify resource management. Right now, table is called on ddb instance every request
    await initialize_transaction_service("sql-orm")
    yield
    await cleanup_transaction_service()


app = FastAPI(lifespan=lifespan)

app.include_router(transactions_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8080, host='0.0.0.0')
