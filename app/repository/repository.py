from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def scan_table(self, filters: dict) -> list:
        raise NotImplementedError

    @abstractmethod
    async def query_items(self, key, value) -> list:
        raise NotImplementedError

    @abstractmethod
    async def post_item(self, item: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def put_item(self, item: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def get_item(self, keys: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self, keys: dict) -> None:
        raise NotImplementedError

