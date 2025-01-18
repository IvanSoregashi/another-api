from typing import Type

from sqlalchemy import select, insert, update

from app.async_database.sqlalchemy import DatabaseSessionManager
from app.schemas.sqlalchemy_base import Base
from app.async_repository.repository import AbstractRepository


class SQLAlchemyORMRepository(AbstractRepository):
    """NOT CONSIDERING TABLES WITHOUT PRIMARY KEY"""
    def __init__(self, model: Type[Base], session_manager: DatabaseSessionManager):
        self._model = model
        self._session_manager = session_manager
        primary_key_names = [pk.name for pk in self._model.__mapper__.primary_key]
        if len(primary_key_names) != 1:
            raise ValueError(f"Model '{self._model.__name__}' does not have, ot have more than one primary key.")
        self.pk = primary_key_names[0]

    async def scan_table(self, filters: dict) -> list:
        # TODO make use of filters.
        async with self._session_manager.session() as session:
            query = select(self._model)
            result = await session.execute(query)
            return result.scalars().all()

    async def query_items(self, key, value) -> list:
        async with self._session_manager.session() as session:
            query = select(self._model).filter_by(**{key: value})
            result = await session.execute(query)
            return result.scalars().all()

    async def post_item(self, item: dict) -> dict:
        async with self._session_manager.session() as session:
            statement = insert(self._model).values(**item).returning(self._model)
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one_or_none()

    async def put_item(self, item: dict) -> dict:
        if self.pk not in item:
            raise ValueError(f"Missing primary key value '{self.pk}' in 'item' dictionary.")
        async with self._session_manager.session() as session:
            where_clause = getattr(self._model, self.pk) == item[self.pk]
            statement = update(self._model).where(where_clause).values(**item).returning(self._model)
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one_or_none()

    async def get_item(self, keys: dict) -> dict:
        async with self._session_manager.session() as session:
            result = await session.get(self._model, keys[self.pk])
            return result

    async def delete_item(self, keys: dict) -> None:
        async with self._session_manager.session() as session:
            result = await session.get(self._model, keys[self.pk])
            if result:
                await session.delete(result)
                await session.commit()
            return result
