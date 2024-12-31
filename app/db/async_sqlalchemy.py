import contextlib
from typing import AsyncIterator, Any, Type

from sqlalchemy import insert, select

from app.repository.repository import AbstractRepository
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession
from sqlalchemy.orm import DeclarativeBase


class DBError(Exception):
    pass


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(expire_on_commit=False, autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise DBError("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DBError("DatabaseSessionManager is not initialized")

        # begin here means autocommit !!!
        async with self._engine.begin() as connection:
            try:
                yield connection
            except DBError:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DBError("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except DBError:
            await session.rollback()
            raise
        finally:
            await session.close()


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


