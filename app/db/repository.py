from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def put_item(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_item(self):
        raise NotImplementedError

    @abstractmethod
    async def get_item(self):
        raise NotImplementedError

    @abstractmethod
    async def query_items(self):
        raise NotImplementedError

    @abstractmethod
    async def scan_table(self):
        raise NotImplementedError
