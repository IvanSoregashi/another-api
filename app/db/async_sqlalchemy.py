import contextlib
from typing import AsyncIterator, Any
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession


class DBError(Exception):
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
