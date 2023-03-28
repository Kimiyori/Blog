from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorClientSession,
)
from bson import ObjectId

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
    def __init__(self, session: Any) -> None:
        self.session = session

    @abstractmethod
    async def add(self, entity: Any) -> Any:
        ...


class MongoDbRepository(AbstractRepository[T]):
    def __init__(
        self,
        client: AsyncIOMotorClient,
        session: AsyncIOMotorClientSession,
        database_name: str,
    ) -> None:
        self.client, self.session = client, session
        self.database = getattr(self.client, database_name)
        self.collection: AsyncIOMotorCollection

    async def add(self, entity: dict[str, Any]) -> ObjectId:
        inserted = await self.collection.insert_one(entity)
        id: ObjectId = inserted.inserted_id
        return id

    async def count(self, entity: dict[str, Any]) -> int:
        count: int = await self.collection.count_documents(entity, session=self.session)
        return count
