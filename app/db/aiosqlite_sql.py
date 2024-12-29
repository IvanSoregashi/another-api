from typing import Self

import aiosql

from app.repository.repository import AbstractRepository
import aiosqlite

from app.models.transactions import Transaction


class DBError(Exception):
    pass


class SQLiteRepository(AbstractRepository):
    SQL_QUERIES = """
    -- name: get-all-transactions
    -- Get all the transactions from the database
    SELECT * FROM transactions;
    """

    def __init__(self, db: aiosqlite.Connection):
        self.db = db
        self.queries = aiosql.from_str(self.SQL_QUERIES, "aiosqlite")

    @classmethod
    async def with_file(cls, file: str) -> Self:
        async with aiosqlite.connect(file) as db:
            db.row_factory = aiosqlite.Row
            yield cls(db)
        # db = await aiosqlite.connect(file)
        # db.row_factory = aiosqlite.Row
        # yield cls(db)

    async def scan_table(self, filters: dict) -> list:
        results = await self.queries.get_all_transactions(self.db)
        return [Transaction.model_validate(result) for result in results]

    async def query_items(self, key, value) -> list:
        raise NotImplementedError

    async def put_item(self, item: dict) -> dict:
        raise NotImplementedError

    async def get_item(self, keys: dict) -> dict:
        raise NotImplementedError

    async def delete_item(self, keys: dict) -> None:
        raise NotImplementedError
