from sqlalchemy import text

from app.db.async_sqlalchemy import DatabaseSessionManager
from app.repository.repository import AbstractRepository


class SQLAlchemyCoreRepository(AbstractRepository):
    def __init__(self, table: str, session_manager: DatabaseSessionManager):
        self.table = table
        self._session_manager = session_manager

    async def scan_table(self, filters: dict) -> list:
        # TODO make use of filters.
        async with self._session_manager.connect() as connection:
            # self.table is not user input
            query = text(f"SELECT * FROM {self.table};")
            # query = query.bindparams(table=self.table)
            result = await connection.execute(query)
            return result.all()

    async def query_items(self, key, value) -> list:
        async with self._session_manager.connect() as connection:
            # self.table and key are not user input
            query = text(f"SELECT * FROM {self.table} WHERE {key}=:value;")
            # value is user input
            query = query.bindparams(value=value)
            result = await connection.execute(query)
            return result.all()

    async def post_item(self, item: dict) -> dict:
        async with self._session_manager.connect() as connection:
            statement = text(
                f"""INSERT INTO {self.table} 
                (transaction_id, month, datetime, type, account, currency, amount, category, point, item, comment) 
                VALUES
                ( :transaction_id, :month, :datetime, 
                :type, :account, :currency, :amount, 
                :category, :point, :item, :comment )
                RETURNING *;"""
            )
            statement = statement.bindparams(**item)
            result = await connection.execute(statement)
            await connection.commit()
            return result.one_or_none()

    async def put_item(self, item: dict) -> dict:
        async with self._session_manager.connect() as connection:
            statement = text(
                f"""UPDATE {self.table}
                SET
                    month = :month,
                    datetime = :datetime,
                    type = :type,
                    account = :account,
                    currency = :currency,
                    amount = :amount,
                    category = :category,
                    point = :point,
                    item = :item,
                    comment = :comment
                WHERE
                    transaction_id = :transaction_id
                RETURNING *;"""
            )
            statement = statement.bindparams(**item)
            result = await connection.execute(statement)
            await connection.commit()
            return result.one_or_none()

    async def get_item(self, keys: dict) -> dict:
        async with self._session_manager.connect() as connection:
            # self.table and key are not user input
            query = text(f"SELECT * FROM {self.table} WHERE transaction_id=:transaction_id AND month=:month;")
            # value is user input
            query = query.bindparams(**keys)
            result = await connection.execute(query)
            return result.one_or_none()

    async def delete_item(self, keys: dict) -> None:
        async with self._session_manager.connect() as connection:
            # self.table and key are not user input
            statement = text(f"DELETE FROM {self.table} WHERE transaction_id=:transaction_id AND month=:month;")
            # value is user input
            statement = statement.bindparams(**keys)
            result = await connection.execute(statement)
            return result
