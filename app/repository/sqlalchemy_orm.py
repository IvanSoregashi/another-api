from typing import Type

from sqlalchemy import select, insert

from app.db.async_sqlalchemy import DatabaseSessionManager
from app.schemas.sqlalchemy_base import Base
from app.repository.repository import AbstractRepository


class SQLAlchemyORMRepository(AbstractRepository):
    def __init__(self, model: Type[Base], session_manager: DatabaseSessionManager):
        self._model = model
        self._session_manager = session_manager

    async def scan_table(self, filters: dict) -> list:
        async with self._session_manager.session() as session:
            query = select(self._model)
            result = await session.execute(query)
            return result.scalars().all()

    async def query_items(self, key, value) -> list:
        async with self._session_manager.session() as session:
            query = select(self._model).filter_by(**{key: value})
            result = await session.execute(query)
            return result.scalars().all()

    async def put_item(self, item: dict) -> dict:
        async with self._session_manager.session() as session:
            statement = insert(self._model).values(**item).returning(self._model)
            result = await session.execute(statement)
            await session.commit()
            return result.scalar()

    async def get_item(self, keys: dict) -> dict:
        async with self._session_manager.session() as session:
            result = await session.get(self._model, keys["transaction_id"])
            return result

    async def delete_item(self, keys: dict) -> None:
        async with self._session_manager.session() as session:
            result = await session.get(self._model, keys["transaction_id"])
            print(result)
            if result:
                await session.delete(result)
                await session.commit()
            return result
